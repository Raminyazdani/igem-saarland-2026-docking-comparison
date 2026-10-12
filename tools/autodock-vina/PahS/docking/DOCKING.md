# Docking — AutoDock Vina (PahS)

**Goal of this step:** dock the prepared ligands into the prepared PahS receptor and record results.
PahP is the primary target and is handled one level up in [`../../docking/`](../../docking/).

## Inputs (from step 1)
- Prepared receptor + ligands in [`../inputs/`](../inputs/), prepared with Meeko 0.7.1
- Parameters in [`../configurations/config.yaml`](../configurations/config.yaml)

## Run
[`run_docking.sh`](run_docking.sh). Native output written to [`../outputs/`](../outputs/).

## Protocol
- Search box / mode: **blind**, whole receptor — center [73.8275, 71.3505, 76.722],
  size [65, 70, 93] angstrom
- Exhaustiveness / #poses / scoring function: 32 / 9 / vina
- Random seed: 42
- Score direction: lower_is_better

Blind mode is specified for PahS in the repo-root `docking_config.yaml`, and the pocket prediction supports
it: fpocket finds 60 pockets on PahS and none survives a sweep of the ranking weights (pocket 36 first in
28/66 combinations, pocket 32 in 27, pocket 58 in 10, pocket 20 in 1). A defined box would have encoded an
arbitrary choice.

## Two campaigns

A blind search over the whole receptor, and per-pocket focused runs kept in
[`../outputs/`](../outputs/) (pocket 36 for six ligands, `_out_p36`; pocket 12 for naphthalene, `_out_p12`).
For the five aromatics the two agree to within 0.11 kcal/mol — well inside Vina's resolution — which
indicates the blind search converges on pocket 36 without being told to. They differ for naphthalene
(−6.578 blind vs −5.223 in pocket 12) because its focused run targeted a pocket the blind search did not
favour for that ligand.

**The blind run is the reported deliverable.** `../results/poses/` and `../results/DOCKING_RESULT.json` both
come from it. The focused runs are retained as a cross-check, not as results.

## Output of this step
1. Native results + logs → `../outputs/`
2. Final chosen poses → `../results/poses/` named `PahS_<ligand>_autodock-vina_v1.<ext>`
3. The standardized `../results/DOCKING_RESULT.json` — filled, validated, committed.
