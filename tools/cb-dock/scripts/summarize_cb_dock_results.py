import argparse
import csv

from cb_dock_config import DEFAULT_CONFIG, TOOL_DIR, load_config


def get_best_cavity(file_path, score_direction: str) -> dict:
    with file_path.open(encoding="utf-8") as file:
        lines = file.readlines()

    cavities = []

    # Skip header
    for line in lines[1:]:
        if not line.strip():
            continue

        columns = line.strip().split(maxsplit=9)
        if len(columns) < 9:
            raise ValueError(f"Malformed cavity row in {file_path}: {line!r}")

        cavities.append(
            {
                "cavity": f"C{columns[0]}",
                "volume": columns[1],
                "center_x": columns[2],
                "center_y": columns[3],
                "center_z": columns[4],
                "size_x": columns[5],
                "size_y": columns[6],
                "size_z": columns[7],
                "score": float(columns[8]),
                "contact_residues": columns[9] if len(columns) > 9 else "",
            }
        )

    if not cavities:
        raise ValueError(f"No cavity rows found in {file_path}")

    selector = min if score_direction == "lower_is_better" else max
    return selector(cavities, key=lambda cavity: cavity["score"])


def add_ranks(results: list[dict], score_direction: str) -> None:
    targets = {result["target_id"] for result in results}

    for target in targets:
        target_results = [
            result
            for result in results
            if result["target_id"] == target
        ]

        target_results.sort(
            key=lambda result: result["docking_score"],
            reverse=score_direction == "higher_is_better",
        )

        previous_score = None
        previous_rank = None

        for index, result in enumerate(target_results, start=1):
            score = result["docking_score"]

            # Give identical scores the same rank.
            if score == previous_score:
                rank = previous_rank
            else:
                rank = index

            result["rank_within_tool"] = rank

            previous_score = score
            previous_rank = rank


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize CB-Dock3 cavity tables and rank ligands."
    )
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG),
        help="Path to the CB-Dock3 YAML configuration.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    outputs_dir = TOOL_DIR / "outputs"
    result_file = TOOL_DIR / "results" / "cb_dock_best_cavities.csv"
    results = []

    for folder in sorted(outputs_dir.iterdir()):
        if not folder.is_dir():
            continue

        curpockets_file = folder / "CurPockets_info.txt"

        if not curpockets_file.exists():
            print(f"Skipping {folder.name}: CurPockets_info.txt not found")
            continue

        if "_" not in folder.name:
            print(f"Skipping {folder.name}: expected <target>_<ligand>")
            continue

        target, ligand = folder.name.split("_", 1)
        if target not in config["targets"]:
            print(f"Skipping {folder.name}: target not listed in config")
            continue

        best = get_best_cavity(
            curpockets_file,
            score_direction=config["score_direction"],
        )

        results.append(
            {
                "target_id": target,
                "ligand_id": ligand,
                "best_cavity": best["cavity"],
                "docking_score": best["score"],
                "score_unit": config["score_unit"],
                "rank_within_tool": None,
                "cavity_volume": best["volume"],
                "center_x": best["center_x"],
                "center_y": best["center_y"],
                "center_z": best["center_z"],
                "size_x": best["size_x"],
                "size_y": best["size_y"],
                "size_z": best["size_z"],
                "contact_residues": best["contact_residues"],
            }
        )

    if not results:
        raise RuntimeError(f"No CB-Dock3 outputs found under {outputs_dir}")

    add_ranks(results, score_direction=config["score_direction"])

    # Keep output easy to read:
    # PahP first, then PahS, ranked best to worst.
    results.sort(
        key=lambda result: (
            result["target_id"],
            result["rank_within_tool"],
            result["ligand_id"],
        )
    )

    for result in results:
        print(
            f"{result['target_id']} + {result['ligand_id']}: "
            f"{result['best_cavity']} "
            f"({result['docking_score']} {result['score_unit']}) "
            f"rank {result['rank_within_tool']}"
        )

    result_file.parent.mkdir(parents=True, exist_ok=True)

    with result_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys(),
        )

        writer.writeheader()
        writer.writerows(results)

    print()
    print(f"Saved {len(results)} results to {result_file}")


if __name__ == "__main__":
    main()
