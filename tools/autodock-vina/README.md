# AutoDock Vina — docking workspace

Branch: `tool/autodock-vina` · Owners: [Ana, Divyashree] · Licence: free

Self-contained workspace for docking the canonical PAH panel into the canonical PahP receptor with
**AutoDock Vina**. Work in two steps, in this order:

## Step 1 — `preprocessing/`
State **exactly** what preparation AutoDock Vina needs and do it. Fill
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
| `inputs/` | canonical inputs converted to AutoDock Vina formats | **yes** (committed so it can be reviewed) |
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
- Touch only this folder (`tools/autodock-vina/`) — not another tool's workspace.
- Compare **ranks**, never raw scores across tools.
