# Docking — CB-Dock3

**Goal of this step:** dock the prepared ligands into the prepared PahP receptor and record results.
Everything that is *not* input preparation lives here. Preprocessing must be finished first (see
[`../preprocessing/steps.md`](../preprocessing/steps.md)).

## Inputs (from step 1)
- Prepared receptor + ligands in [`../inputs/`](../inputs/)
- Parameters in [`../configurations/config.yaml`](../configurations/config.yaml)

## Run
Use [`run_docking.sh`](run_docking.sh) (or record the exact GUI/web steps here if the tool can't be
scripted). Write native output to [`../outputs/`](../outputs/).

## Protocol (fill this in)
- Search box / mode: _TODO_ (from `config.yaml`)
- Exhaustiveness / #poses / scoring function: _TODO_
- Random seed: _TODO_ (fix it if the tool allows, for reproducibility)
- Score direction: _TODO_ (`lower_is_better` or `higher_is_better` for CB-Dock3)

## Output of this step
1. Native results + logs → `../outputs/`
2. Final chosen poses → `../results/poses/` named `PahP__<ligand>__cb-dock__v1.<ext>`
3. The standardized `../results/DOCKING_RESULT.json` (the single comparison file) — fill, validate, commit.
