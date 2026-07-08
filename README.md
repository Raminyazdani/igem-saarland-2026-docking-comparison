# iGEM Saarland 2026 — PAH Docking Comparison

A **fair, reproducible comparison of docking tools** for the team's PAH biosensor. Every tool docks the
**same PAH ligands** into the **same receptor** from the **same frozen input**, in **two explicit steps**
(preprocessing, then docking), and returns **one standardized result file**. Python packages then merge the
results — and the preprocessing recipes — into tables and plots.

> **New here?**
> - **Team member** assigned a tool → read **[`START_HERE.md`](START_HERE.md)**. Questions → **Elnaz** (coordinator).
> - **Setting up the GitHub repo** (Ramin & Elnaz, technical) → read **[`SETUP_GITHUB.md`](SETUP_GITHUB.md)**.
> - Branch & PR rules → **[`CONTRIBUTING.md`](CONTRIBUTING.md)**.

## The science in one paragraph
The biosensor targets **PahP**, a **periplasmic PAH-binding protein** (~317 aa) that directly binds the
polycyclic aromatic hydrocarbon — so PahP is the **primary docking target**. **PahS** (~686 aa,
outer-membrane sensor) is a **secondary** target (blind docking only). We dock a panel of PAHs — **pyrene**
(primary) plus phenanthrene, benzo[a]pyrene, naphthalene, anthracene, and fluoranthene — with **glucose** as
a negative control. Other constructs (CFP/YFP, GCaMP6f, MBP-mScarlet-G3BP1, pRS416/pET backbones) are
**reference only**, not docking receptors.

## How it works (branch → two steps → result → compare)
- `main` = stable/citable; `develop` = integration. **Nobody pushes to either directly.**
- **One branch + one workspace folder per tool:** `tool/<tool>` ↔ `tools/<tool>/`. Teams deliver by
  **Pull Request into `develop`**; only **Ramin/Elnaz** merge `develop → main`
  (see [`CONTRIBUTING.md`](CONTRIBUTING.md)).
- Each team works in its own `tools/<tool>/` folder in **two steps**:
  1. **`preprocessing/`** — state exactly what prep the tool needs, and do it (recorded in a structured,
     comparable manifest).
  2. **`docking/`** — the actual docking run.
- Each team commits exactly one `tools/<tool>/results/DOCKING_RESULT.json` — the single file the comparison
  is built from — plus final poses.
- Two analysis packages: `scripts/compare_results/` (the docking results) and
  `scripts/compare_preprocessing/` (the preprocessing recipes + a team status dashboard).

```
  tool/<tool>  ──PR──►  develop  ──PR (Ramin/Elnaz only)──►  main
```

## Two comparisons, one goal
Because preprocessing is separated from docking and recorded in the same structured form for every tool, we
can compare not just the **results** but the **preprocessing** itself — and, as a stretch goal, **design one
shared preprocessing that works for all tools** and re-dock from that single common starting point. See
[`tools/README.md`](tools/README.md) and [`scripts/compare_preprocessing/README.md`](scripts/compare_preprocessing/README.md).

## ⚠️ Scores are NOT comparable across tools
Vina kcal/mol, GOLD ChemPLP, GlideScore, Uni-Mol confidence — different quantities on different scales. We
never compare raw scores across tools; we compare **rank within each tool**, then a **cross-tool consensus
rank**. The schema and scripts enforce this.

## Repository layout
```
input/
  raw/                # reference only — never docked (constructs/, final_plasmids/, literature/, slides/, notes/)
  canonical/          # SHARED, FROZEN starting point — identical for all tools
    targets/  PahP/ + PahS/  (sequence.fasta, structure.pdb*, binding_site.yaml*)  + target_metadata.csv
    ligands/  ligands.smi, ligands.sdf, ligand_metadata.csv
    docking_config.yaml   # single source of truth
tools/                # ONE self-contained workspace per tool
  _TEMPLATE/          # copy this to add a new tool
  <tool>/
    inputs/           # canonical inputs converted to the tool's formats (committed for review)
    preprocessing/    # PREPROCESSING.yaml (comparable manifest) + steps.md + preprocess.sh
    docking/          # DOCKING.md + run_docking.sh
    configurations/   # config.yaml (box, seed, exhaustiveness, ...)
    outputs/          # raw/native output & logs (committed for review)
    results/          # DOCKING_RESULT.json  <-- the single standardized file  + poses/
    status/           # status.yaml (progress + blockers)
results/
  DOCKING_RESULT.template.json   DOCKING_RESULT.example.json   # shared references to copy
scripts/
  compare_results/        # validate / combine / tables / plots + JSON schema
  compare_preprocessing/  # compare recipes + status dashboard
reports/tables/  reports/figures/   # generated outputs
TEAM_INSTRUCTIONS.md
```
`*` = **placeholder** — `structure.pdb` and `binding_site.yaml` are TODO until an AlphaFold model exists.

## Status (2026-07-08)
- Canonical **ligands** ready (7 molecules, real 3D SDF). Canonical **sequences** ready (PahP 317 aa, PahS 686 aa).
- Six tool workspaces scaffolded under `tools/` (preprocessing + docking templates ready to fill).
- **BLOCKED:** no experimental structure → an **AlphaFold model + binding box** must be added per target
  before docking. Until then `input_version` stays `v0-draft` and **`input-v1` is not frozen**.
- Commercial-tool licences (Glide / GOLD / Discovery Studio): **to confirm** (see `docking_config.yaml`).

## Quick start (analysis)
```bash
pip install -r requirements.txt     # root analysis deps (same as scripts/compare_results/requirements.txt)

# docking results -> tables + figures
bash scripts/compare_results/collect_from_branches.sh          # gather each tool/* branch's result
python scripts/compare_results/compare.py reports/collected    # validate -> combine -> tables -> plots

# preprocessing recipes + team status
python scripts/compare_preprocessing/compare_preprocessing.py  # -> preprocessing_comparison / _consensus
python scripts/compare_preprocessing/status_overview.py        # -> status_overview (team dashboard)
```
See [`TEAM_INSTRUCTIONS.md`](TEAM_INSTRUCTIONS.md) for the per-team workflow.

## License
See [`LICENSE`](LICENSE) — **TODO: Ramin/Elnaz to choose** (MIT or CC-BY suggested).
