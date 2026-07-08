<!-- Team PRs go from your tool/<tool> branch INTO develop (never into main). -->

## Tool
<!-- e.g. AutoDock Vina (branch tool/autodock-vina) -->

## What this PR contains
- [ ] Step 1 — preprocessing (`PREPROCESSING.yaml` + steps.md + preprocess.sh)
- [ ] Step 2 — docking (config + run)
- [ ] `results/DOCKING_RESULT.json`
- [ ] Final poses in `results/poses/`

## Checklist (required)
- [ ] Base branch is **`develop`** (not `main`)
- [ ] I changed only my own `tools/<tool>/` folder
- [ ] I did **not** edit `input/canonical/`, `scripts/`, or another team's folder
- [ ] `python scripts/compare_results/validate_results.py tools/<tool>/results/DOCKING_RESULT.json` passes (exit 0)
- [ ] All ligands in `ligand_metadata.csv` were attempted; failures documented (`status: failed` + reason)
- [ ] `input_commit_hash` = the frozen `input-v1` hash
- [ ] `status/status.yaml` updated

## Notes for reviewers
<!-- anything Ramin/Elnaz should know when reviewing -->
