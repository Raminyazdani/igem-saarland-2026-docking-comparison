# Docking — AutoDock Vina

**Goal of this step:** dock the prepared ligands into the prepared PahP receptor and record results.
Everything that is *not* input preparation lives here. Preprocessing must be finished first (see
[`../preprocessing/steps.md`](../preprocessing/steps.md)).

## Inputs (from step 1)
- Prepared receptor + ligands in [`../inputs/`](../inputs/)
- Parameters in [`../configurations/config.yaml`](../configurations/config.yaml)

## Run
Use [`run_docking.sh`](run_docking.sh). Native output written to [`../outputs/`](../outputs/).

## Protocol
- Search box / mode: defined, center [70.83, 71.96, 59.18], size [21.3, 19.6, 27.3] angstrom (fpocket Pocket 4, see ../preprocessing/steps.md)
- Exhaustiveness / #poses / scoring function: 16 / 9 / vina
- Random seed: 42
- Score direction: lower_is_better

## Output of this step
1. Native results + logs → `../outputs/`
2. Final chosen poses → `../results/poses/` named `PahP__<ligand>__autodock-vina__v1.<ext>`
3. The standardized `../results/DOCKING_RESULT.json` — filled, validated, committed.

## Scope
PahP + pyrene only in this run. Remaining canonical ligands and PahS not yet attempted.
