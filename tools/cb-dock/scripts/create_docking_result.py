import argparse
import csv
import json
import re

from cb_dock_config import (
    DEFAULT_CONFIG,
    REPO_ROOT,
    TOOL_DIR,
    load_config,
    result_docking_parameters,
)

SUMMARY_FILE = TOOL_DIR / "results" / "cb_dock_best_cavities.csv"
LIGAND_METADATA_FILE = (
    REPO_ROOT / "input" / "canonical" / "ligands" / "ligand_metadata.csv"
)
POSES_DIR = TOOL_DIR / "results" / "poses"
RESULT_FILE = TOOL_DIR / "results" / "DOCKING_RESULT.json"


def load_pubchem_ids() -> dict[str, str]:
    with LIGAND_METADATA_FILE.open(encoding="utf-8") as file:
        reader = csv.DictReader(file)

        return {
            row["ligand_id"]: row["pubchem_cid"]
            for row in reader
        }


def load_results(config: dict) -> list[dict]:
    pubchem_ids = load_pubchem_ids()
    results = []

    with SUMMARY_FILE.open(encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            target = row["target_id"]
            ligand = row["ligand_id"]
            cavity = row["best_cavity"]

            pose_file = (
                POSES_DIR
                / f"{target}__{ligand}__{config['tool_slug']}__v1.pdb"
            )

            if not pose_file.exists():
                raise FileNotFoundError(
                    f"Selected pose not found: {pose_file}"
                )

            if ligand not in pubchem_ids:
                raise ValueError(
                    f"PubChem CID not found for ligand: {ligand}"
                )

            results.append(
                {
                    "target_id": target,
                    "ligand_id": ligand,
                    "pubchem_cid": pubchem_ids[ligand],
                    "docking_score": float(row["docking_score"]),
                    "score_unit": config["score_unit"],
                    "rank_within_tool": int(
                        row["rank_within_tool"]
                    ),
                    "pose_file": pose_file.relative_to(REPO_ROOT).as_posix(),
                    "runtime_sec": None,
                    "status": "ok",
                    "failure_reason": None,
                    "notes": (
                        f"Best structure-based CB-Dock cavity: "
                        f"{cavity}"
                    ),
                }
            )

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the standardized CB-Dock3 result JSON."
    )
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG),
        help="Path to the CB-Dock3 YAML configuration.",
    )
    parser.add_argument(
        "--input-commit-hash",
        help="Short or full commit hash of the frozen input-v1 tag.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    input_commit_hash = args.input_commit_hash or config.get("input_commit_hash")

    if not input_commit_hash or not re.fullmatch(
        r"[0-9a-fA-F]{7,40}", str(input_commit_hash)
    ):
        raise SystemExit(
            "A valid input-v1 git hash is required. Pass "
            "--input-commit-hash after the coordinators freeze input-v1; "
            "do not use the current branch hash."
        )

    results = load_results(config)
    expected_pairs = {
        (target, ligand)
        for target in config["targets"]
        for ligand in load_pubchem_ids()
    }
    actual_pairs = {
        (result["target_id"], result["ligand_id"])
        for result in results
    }
    missing_pairs = sorted(expected_pairs - actual_pairs)
    extra_pairs = sorted(actual_pairs - expected_pairs)
    if missing_pairs or extra_pairs:
        raise ValueError(
            f"Unexpected target-ligand coverage; missing={missing_pairs}, "
            f"extra={extra_pairs}"
        )

    docking_result = {
        "schema_version": "1.0",
        "tool_name": config["tool"],
        "branch": config["branch"],
        "team_members": [
            "Samruddhi",
            "Marwan",
        ],
        "software_version": config["software_version"],
        "date_completed": str(config["date_completed"]),
        "input_commit_hash": input_commit_hash,
        "score_direction": config["score_direction"],
        "receptor_prep_method": (
            "OpenMM-written PahP/PahS PDB files uploaded to CB-Dock3; "
            "original model provenance and exact preparation command are "
            "not yet recorded."
        ),
        "ligand_prep_method": (
            "Individual ligand records extracted from the canonical "
            "ligands.sdf and uploaded directly to CB-Dock3."
        ),
        "docking_parameters": result_docking_parameters(config),
        "hardware": config["hardware"],
        "runtime_total_sec": config["runtime_total_sec"],
        "results": results,
        "failed_cases": [],
        "warnings": config.get("warnings", []),
        "notes": (
            "Primary results use CB-Dock3 structure-based blind docking. "
            "For each target-ligand pair, the CurPocket cavity with the "
            "lowest AutoDock Vina score was selected. Template-based "
            "docking results, where available, were not used for ranking."
        ),
    }

    RESULT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with RESULT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            docking_result,
            file,
            indent=2,
        )
        file.write("\n")

    print(f"Created: {RESULT_FILE}")
    print(f"Results: {len(results)}")


if __name__ == "__main__":
    main()
