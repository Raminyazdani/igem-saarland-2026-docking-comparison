# START HERE — team member guide

Welcome! This repo runs a **fair comparison of docking tools** for our PAH biosensor. You've been assigned
**one tool**. Your job: dock the shared PAH panel into the shared PahP receptor with your tool, in two
steps, and hand back one standardized result. This page is the map; follow it top to bottom.

---

## 0. The one rule
> **You work only inside your own folder `tools/<your-tool>/`, on your own branch `tool/<your-tool>`, and
> you deliver changes by opening a Pull Request into `develop`.** Never push to `main` or `develop`, and
> never touch `input/canonical/` or another team's folder.

Branch picture:
```
  tool/autodock-vina ┐
  tool/gold          │
  tool/glide         ├──PR──►  develop  ──(only Ramin/Elnaz merge)──►  main
  tool/cb-dock       │        (integration)                            (stable)
  tool/uni-mol       │
  tool/discovery-studio ┘
```

---

## 1. Install what you need (once)
- **Git** — https://git-scm.com/downloads
- **Python 3.10+** — https://www.python.org/downloads/
- A **GitHub account** (send your username to Ramin/Elnaz so they can add you).

## 2. Get the code and switch to YOUR branch
```bash
git clone <REPO_URL>
cd igem-saarland-2026-docking-comparison
git checkout tool/<your-tool>        # e.g. tool/autodock-vina — this branch was created for you
git pull origin develop              # start from the latest shared state
```
Find your exact branch/folder name in [`input/canonical/docking_config.yaml`](input/canonical/docking_config.yaml).

## 3. Do the work — TWO steps, in order
Everything lives in **`tools/<your-tool>/`**. Read that folder's `README.md` first.

**Step 1 — preprocessing** (`tools/<your-tool>/preprocessing/`)
- Say *exactly* what preparation your tool needs and do it.
- Fill **`PREPROCESSING.yaml`** (keep the keys identical to other tools — this is compared across tools),
  narrate it in `steps.md`, and script it in `preprocess.sh`. Prepared files go in `inputs/`.

**Step 2 — docking** (`tools/<your-tool>/docking/`)
- Install your tool's deps: `pip install -r tools/<your-tool>/requirements.txt` (this file is maintained by
  Ramin & Elnaz — ask them if a package is missing; don't edit it or your folder's `.gitignore` yourself).
- Run the docking from your prepared inputs. Parameters go in `configurations/config.yaml`.
- Native output → `outputs/`. Final chosen poses → `results/poses/`.

Detailed docking rules (fairness, seeds, failures, score direction) are in
[`TEAM_INSTRUCTIONS.md`](TEAM_INSTRUCTIONS.md) — **read it before docking.**

## 4. Produce the one required file
```bash
cp results/DOCKING_RESULT.template.json tools/<your-tool>/results/DOCKING_RESULT.json
# fill it (worked example: results/DOCKING_RESULT.example.json)
pip install -r scripts/compare_results/requirements.txt
python scripts/compare_results/validate_results.py tools/<your-tool>/results/DOCKING_RESULT.json
```
It must print `1/1 file(s) passed` (exit 0) before you commit. Update `status/status.yaml` as you go.

## 5. Commit, push, open a Pull Request
```bash
git add tools/<your-tool>/
git commit -m "tool/<your-tool>: preprocessing + docking + result"
git push origin tool/<your-tool>
```
Then on GitHub: **open a Pull Request from `tool/<your-tool>` into `develop`** (not into main). Fill in the
PR checklist. **Ramin or Elnaz** reviews and merges it. See [`CONTRIBUTING.md`](CONTRIBUTING.md)
for the full branch/PR rules.

## 6. Keep going / keep in sync
Before starting a new work session, refresh your branch with the latest shared state:
```bash
git checkout tool/<your-tool>
git pull origin develop        # bring in others' merged changes (and any input re-freeze)
```

---

## Where to look
| I want to… | Go to |
|------------|-------|
| Understand the whole project | [`README.md`](README.md) |
| Know the docking rules for my result | [`TEAM_INSTRUCTIONS.md`](TEAM_INSTRUCTIONS.md) |
| Know the branch / PR / permission rules | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Understand my tool's folders | `tools/<your-tool>/README.md` |
| See a filled result example | [`results/DOCKING_RESULT.example.json`](results/DOCKING_RESULT.example.json) |

Stuck? Ask **Elnaz** (team coordinator). For Git / GitHub problems, ask **Ramin or Elnaz**.
