import argparse
import csv
import shutil

from cb_dock_config import DEFAULT_CONFIG, TOOL_DIR, load_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy the configured best CB-Dock3 pose for each pair."
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
    summary_file = TOOL_DIR / "results" / "cb_dock_best_cavities.csv"
    outputs_dir = TOOL_DIR / "outputs"
    poses_dir = TOOL_DIR / "results" / "poses"
    complexes_dir = TOOL_DIR / "results" / "complexes"
    tool_slug = config["tool_slug"]

    poses_dir.mkdir(parents=True, exist_ok=True)
    complexes_dir.mkdir(parents=True, exist_ok=True)
    missing = []
    copied = 0

    with summary_file.open(encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            target = row["target_id"]
            ligand = row["ligand_id"]
            cavity = row["best_cavity"]

            run_folder = outputs_dir / f"{target}_{ligand}"

            source_pose = (
                run_folder
                / "poses"
                / f"{target}_{ligand}_pose_{cavity}.pdb"
            )

            source_complex = (
                run_folder
                / "complexes"
                / f"{target}_{ligand}_Complex_{cavity}.pdb"
            )

            destination_pose = (
                poses_dir
                / f"{target}__{ligand}__{tool_slug}__v1.pdb"
            )

            destination_complex = (
                complexes_dir
                / f"{target}__{ligand}__{tool_slug}__v1__complex.pdb"
            )

            if not source_pose.exists():
                print(f"[MISSING POSE] {source_pose}")
                missing.append(source_pose)
                continue

            if not source_complex.exists():
                print(f"[MISSING COMPLEX] {source_complex}")
                missing.append(source_complex)
                continue

            shutil.copy2(
                source_pose,
                destination_pose,
            )

            shutil.copy2(
                source_complex,
                destination_complex,
            )
            copied += 1

            print(
                f"[OK] {target} + {ligand}: "
                f"{cavity} -> "
                f"{destination_pose.name}, "
                f"{destination_complex.name}"
            )

    if missing:
        raise SystemExit(f"Missing {len(missing)} selected source file(s).")

    print(f"Collected {copied} selected pose/complex pair(s).")


if __name__ == "__main__":
    main()
