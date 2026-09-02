# CB-Dock3 — docking workspace

Branch: `tool/cb-dock` · Owners: [Samruddhi, Marwan] · Licence: free_web

Self-contained workspace for docking the canonical PAH panel into the canonical PahP receptor with
**CB-Dock3**. Work in two steps, in this order:

## Step 1 — `preprocessing/`
State **exactly** what preparation CB-Dock3 needs and do it. Fill
[`preprocessing/PREPROCESSING.yaml`](preprocessing/PREPROCESSING.yaml) (the structured, comparable
manifest), narrate it in [`preprocessing/steps.md`](preprocessing/steps.md), and make it reproducible in
[`preprocessing/preprocess.sh`](preprocessing/preprocess.sh). Write the prepared files into `inputs/`.

## Step 2 — `docking/`
Run the actual docking from the prepared inputs. See [`docking/DOCKING.md`](docking/DOCKING.md) and
[`docking/run_docking.sh`](docking/run_docking.sh). Native output → `outputs/`. Tool parameters →
[`configurations/config.yaml`](configurations/config.yaml).

## Deliverable
`results/DOCKING_RESULT.json` — **the one standardized file** that feeds the final comparison and plots.
Copy the repo-root template, fill it, validate it, commit it, and commit your final poses to
`results/poses/`. Keep [`status/status.yaml`](status/status.yaml) up to date.

## Folder map
| Folder | What goes here | Committed? |
|--------|----------------|-----------|
| `inputs/` | canonical inputs converted to CB-Dock3 formats | **yes** (committed so it can be reviewed) |
| `preprocessing/` | manifest + narrative + script | **yes** |
| `docking/` | docking protocol + script | **yes** |
| `configurations/` | tool parameters | **yes** |
| `outputs/` | raw/native output & logs | **yes** (committed so it can be reviewed) |
| `results/` | `DOCKING_RESULT.json` + `poses/` | **yes** |
| `status/` | progress + blockers | **yes** |
| `requirements.txt` | this tool's Python deps (managed by Ramin & Elnaz) | **yes** |
| `.gitignore` | tool-specific scratch to ignore (managed by Ramin & Elnaz) | **yes** |

## Rules
- Read inputs only from `input/canonical/`. Never edit canonical inputs.
- Touch only this folder (`tools/cb-dock/`) — not another tool's workspace.
- Compare **ranks**, never raw scores across tools.

## Current CB-Dock3 run notes

- All seven ligands were run against PahP and PahS (14 web jobs total).
- Each output folder contains five cavity poses, five complexes, and `CurPockets_info.txt`.
- The individual ligand SDF files exactly match the records in the canonical SDF.
- The run used structure-based blind docking, CurPocket (five cavities), and AutoDock Vina 1.2.0.
- Final submission is still blocked because `input-v1` has not been frozen and the source/preparation command
  for the two receptor models is not recorded.
- Do not commit the duplicate `*_fixed.pdb` files under `input/canonical/`; keep tool-specific prepared files
  under `tools/cb-dock/inputs/` and ask a coordinator to update canonical input.
- See [`commands.md`](commands.md) for the local post-processing commands.
