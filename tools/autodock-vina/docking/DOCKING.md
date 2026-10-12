# Docking — AutoDock Vina (PahP)

**Goal of this step:** dock the prepared ligands into the prepared PahP receptor and record results.
Everything that is *not* input preparation lives here. Preprocessing must be finished first (see
[`../preprocessing/steps.md`](../preprocessing/steps.md)).

## Inputs (from step 1)
- Prepared receptor + ligands in [`../inputs/`](../inputs/)
- Parameters in [`../configurations/config.yaml`](../configurations/config.yaml)

## Run
[`dock_ligand.py <ligand>`](dock_ligand.py) docks one ligand, reading the box and sampling settings from
`config.yaml` so the script and the manifest cannot drift apart. [`run_docking.sh`](run_docking.sh) loops it
over every ligand in the canonical metadata. Native output is written to [`../outputs/`](../outputs/).

## Protocol
- Search box / mode: defined, center [70.83, 71.96, 59.18], size [21.3, 19.6, 27.3] angstrom
  (fpocket Pocket 4, see [`../preprocessing/steps.md`](../preprocessing/steps.md))
- Exhaustiveness / #poses / scoring function: 16 / 9 / vina
- Random seed: 42
- Score direction: lower_is_better

## Output of this step
1. Native results + logs → `../outputs/`
2. Final chosen poses → `../results/poses/` named `PahP__<ligand>__autodock-vina__v1.<ext>`
3. The standardized `../results/DOCKING_RESULT.json` — filled, validated, committed.

## Scope
All 7 canonical ligands docked into PahP (6 PAHs plus the glucose negative control). PahS was docked
separately and lives in [`../PahS/`](../PahS/). Pyrene and phenanthrene were taken forward to 100 ns MD and
MM-GBSA — see [`../md/`](../md/); note that the MD result qualifies how far the docked pose can be trusted.
