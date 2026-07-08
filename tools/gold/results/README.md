# `results/` — the single standardized deliverable

This folder holds **the one file** the whole comparison depends on:

- **`DOCKING_RESULT.json`** — the standardized result with the comparison values and keys (per-ligand
  `docking_score`, `score_unit`, `rank_within_tool`, `score_direction`, `pose_file`, `status`). This is what
  the final tables and plots are built from.
- **`poses/`** — your final chosen poses, committed, named `PahP__<ligand>__<tool>__v1.<ext>`.

## How to produce `DOCKING_RESULT.json`
```bash
cp ../../../results/DOCKING_RESULT.template.json ./DOCKING_RESULT.json   # from repo-root template
# fill it in (see ../../../results/DOCKING_RESULT.example.json for a worked example)
python ../../../scripts/compare_results/validate_results.py ./DOCKING_RESULT.json   # must pass (exit 0)
```
Commit `DOCKING_RESULT.json` and everything in `poses/`. Bulky native output stays in `../outputs/`
(committed too, so it can be reviewed).
