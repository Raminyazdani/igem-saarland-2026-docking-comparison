from __future__ import annotations

import argparse
import re
import time
from pathlib import Path
from urllib.parse import urljoin

from playwright.sync_api import (
    BrowserContext,
    Frame,
    Locator,
    Page,
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)


# ---------------------------------------------------------------------------
# General helpers
# ---------------------------------------------------------------------------


def clean_name(value: str) -> str:
    """Convert a protein/ligand name into a safe filename component."""
    return re.sub(r"[^A-Za-z0-9_-]+", "_", value).strip("_")


def cavity_sort_key(cavity: str) -> int:
    """Convert C1, C2, ... into sortable integers."""
    return int(cavity.removeprefix("C"))


def cavity_from_href(href: str) -> str | None:
    """
    Extract a CB-Dock cavity ID from filenames such as:

        PahP_fixed:pyrene_out_4.-8.0.pdb
        PahP_fixed:pyrene_out_4.-8.0.complex.pdb

    Returns:
        "C4"
    """
    match = re.search(r"_out_(\d+)\.", href)

    if match is None:
        return None

    return f"C{match.group(1)}"


def download_file(
    context: BrowserContext,
    url: str,
    output_path: Path,
    max_attempts: int = 5,
) -> None:
    """
    Download a CB-Dock file with retries.

    CB-Dock occasionally resets connections while transferring larger
    complex PDB files, so retry transient failures automatically.
    """

    last_error: Exception | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            print(
                f"  Download attempt {attempt}/{max_attempts}"
            )

            response = context.request.get(
                url,
                timeout=60_000,
            )

            if not response.ok:
                raise RuntimeError(
                    f"HTTP {response.status}"
                )

            data = response.body()

            if not data:
                raise RuntimeError(
                    "Downloaded file was empty."
                )

            output_path.write_bytes(data)

            return

        except Exception as exc:
            last_error = exc

            if attempt == max_attempts:
                break

            print(
                f"  Temporary download failure: {exc}"
            )
            print("  Retrying...")

            time.sleep(2 * attempt)

    raise RuntimeError(
        f"Failed to download after {max_attempts} attempts:\n"
        f"{url}\n"
        f"Last error: {last_error}"
    )

# ---------------------------------------------------------------------------
# Frame discovery
# ---------------------------------------------------------------------------

def find_frame_with_selector(
    page: Page,
    selector: str,
    timeout_sec: int = 60, ) -> Frame:
    """
    Search the main page and all iframes until a selector is found.

    CB-Dock3 places important result content inside iframes, so searching
    only page.locator(...) is insufficient.
    """
    deadline = time.time() + timeout_sec

    while time.time() < deadline:
        for frame in page.frames:
            try:
                if frame.locator(selector).count() > 0:
                    return frame
            except Exception:
                # A frame can disappear/reload while we inspect it.
                continue

        page.wait_for_timeout(500)

    frame_urls = "\n".join(
        f"  - {frame.url or '<empty URL>'}"
        for frame in page.frames
    )

    raise RuntimeError(
        f"Could not find selector within {timeout_sec} seconds:\n"
        f"  {selector}\n\n"
        f"Frames detected:\n"
        f"{frame_urls}"
    )


def wait_for_results(page: Page) -> Frame:
    """
    Wait for the actual completed CB-Dock result table.

    The CurPockets link is a reliable marker because it exists only after
    results have been generated.
    """
    print("Waiting for CB-Dock results...")

    results_frame = find_frame_with_selector(
        page,
        'a[href*="conf_after_dock.txt"]',
        timeout_sec=120,
    )

    print("Results detected.")
    print(f"Results frame: {results_frame.url}")
    print()

    return results_frame


# ---------------------------------------------------------------------------
# Docking result downloads
# ---------------------------------------------------------------------------


def download_docking_files(
    results_frame: Frame,
    context: BrowserContext,
    poses_dir: Path,
    complexes_dir: Path,
    prefix: str,
) -> set[str]:
    """
    Download ligand poses into poses/ and protein-ligand complexes
    into complexes/.
    """

    links = results_frame.locator("a[href]")

    cavities: set[str] = set()
    downloaded_files: set[str] = set()

    print("Scanning CB-Dock result links...")

    for index in range(links.count()):
        link = links.nth(index)

        href = link.get_attribute("href")

        if not href:
            continue

        cavity = cavity_from_href(href)

        if cavity is None:
            continue

        href_lower = href.lower()

        if not href_lower.endswith(".pdb"):
            continue

        cavities.add(cavity)

        if href_lower.endswith(".complex.pdb"):
            filename = f"{prefix}_Complex_{cavity}.pdb"
            output_path = complexes_dir / filename
        else:
            filename = f"{prefix}_pose_{cavity}.pdb"
            output_path = poses_dir / filename

        if filename in downloaded_files:
            continue

        absolute_url = urljoin(
            results_frame.url,
            href,
        )

        print(f"Downloading: {filename}")

        download_file(
            context=context,
            url=absolute_url,
            output_path=output_path,
        )

        downloaded_files.add(filename)

    if not cavities:
        raise RuntimeError(
            "No CB-Dock cavity PDB links were found."
        )

    print()
    print(
        "Detected cavities:",
        ", ".join(
            sorted(cavities, key=cavity_sort_key)
        ),
    )
    print()

    return cavities

def download_curpockets(
    results_frame: Frame,
    context: BrowserContext,
    output_dir: Path,
) -> None:
    """Download conf_after_dock.txt as CurPockets_info.txt."""
    link = results_frame.locator(
        'a[href*="conf_after_dock.txt"]'
    ).first

    href = link.get_attribute("href")

    if not href:
        raise RuntimeError(
            "The CurPockets link exists but its href is empty."
        )

    absolute_url = urljoin(
        results_frame.url,
        href,
    )

    output_path = output_dir / "CurPockets_info.txt"

    print("Downloading: CurPockets_info.txt")

    download_file(
        context=context,
        url=absolute_url,
        output_path=output_path,
    )

    print()


# ---------------------------------------------------------------------------
# Result table helpers
# ---------------------------------------------------------------------------


def find_cavity_row(
    results_frame: Frame,
    cavity: str,
) -> Locator | None:
    """
    Find the result-table row corresponding to a specific cavity.

    Example cavity:
        C4
    """
    rows = results_frame.locator("tr")

    pattern = re.compile(
        rf"\b{re.escape(cavity)}\b"
    )

    for index in range(rows.count()):
        row = rows.nth(index)

        try:
            text = row.inner_text().strip()
        except Exception:
            continue

        if not pattern.search(text):
            continue

        if row.get_by_text(
            "View",
            exact=True,
        ).count() > 0:
            return row

    return None


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate_outputs(
    output_dir: Path,
    poses_dir: Path,
    complexes_dir: Path,
    prefix: str,
    cavities: set[str],
) -> bool:
    """Verify that all expected CB-Dock output files exist."""

    expected_paths: list[Path] = [
        output_dir / "CurPockets_info.txt",
    ]

    for cavity in sorted(
        cavities,
        key=cavity_sort_key,
    ):
        expected_paths.extend(
            [
                poses_dir
                / f"{prefix}_pose_{cavity}.pdb",

                complexes_dir
                / f"{prefix}_Complex_{cavity}.pdb",
            ]
        )

    print("=" * 70)
    print("OUTPUT CHECK")
    print("=" * 70)

    missing: list[Path] = []

    for path in expected_paths:
        if (
            path.exists()
            and path.is_file()
            and path.stat().st_size > 0
        ):
            print(f"[OK]      {path}")

        else:
            print(f"[MISSING] {path}")
            missing.append(path)

    print("=" * 70)

    if missing:
        print(
            f"{len(missing)} expected file(s) are missing."
        )
        return False

    print(
        f"Success: all {len(expected_paths)} expected files were created."
    )

    return True

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Download all CB-Dock3 outputs for one "
            "protein-ligand docking result."
        )
    )

    parser.add_argument(
        "--result-url",
        required=True,
        help=(
            "Full CB-Dock3 result-page URL currently visible "
            "in the browser."
        ),
    )

    parser.add_argument(
        "--protein",
        required=True,
        help="Protein/target name, e.g. PahP.",
    )

    parser.add_argument(
        "--ligand",
        required=True,
        help="Ligand name, e.g. pyrene.",
    )

    parser.add_argument(
        "--output-root",
        required=True,
        help=(
            "Parent directory. A <protein>_<ligand> folder "
            "will be created inside it."
        ),
    )

    return parser.parse_args()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    args = parse_args()

    protein = clean_name(args.protein)
    ligand = clean_name(args.ligand)

    prefix = f"{protein}_{ligand}"

    output_dir = (
        Path(args.output_root)
        / prefix
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )
    poses_dir = output_dir / "poses"
    complexes_dir = output_dir / "complexes"

    poses_dir.mkdir(parents=True, exist_ok=True)
    complexes_dir.mkdir(parents=True, exist_ok=True)

    print()
    print(f"Protein:       {protein}")
    print(f"Ligand:        {ligand}")
    print(f"Output folder: {output_dir}")
    print()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
        )

        context = browser.new_context(
            accept_downloads=True,
            viewport={
                "width": 1600,
                "height": 1000,
            },
        )

        page = context.new_page()

        print("Opening CB-Dock result page...")

        page.goto(
            args.result_url,
            wait_until="domcontentloaded",
            timeout=120_000,
        )

        # ---------------------------------------------------------------
        # Find the iframe containing the completed docking result table.
        # ---------------------------------------------------------------

        results_frame = wait_for_results(page)

        # ---------------------------------------------------------------
        # Download all C1-C5 PDB poses and complexes.
        # ---------------------------------------------------------------

        cavities = download_docking_files(
            results_frame=results_frame,
            context=context,
            poses_dir=poses_dir,
            complexes_dir=complexes_dir,
            prefix=prefix,
        )

        # ---------------------------------------------------------------
        # Download CurPockets_info.txt.
        # ---------------------------------------------------------------

        download_curpockets(
            results_frame=results_frame,
            context=context,
            output_dir=output_dir,
        )

        # ---------------------------------------------------------------
        # Check final output.
        # ---------------------------------------------------------------

        success = validate_outputs(
            output_dir=output_dir,
            poses_dir=poses_dir,
            complexes_dir=complexes_dir,
            prefix=prefix,
            cavities=cavities,
        )

        browser.close()

    if not success:
        raise SystemExit(1)


if __name__ == "__main__":
    main()