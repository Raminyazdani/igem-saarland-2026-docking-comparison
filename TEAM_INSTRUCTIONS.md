# TEAM_INSTRUCTIONS — read before you dock (5 min)

## 1. Goal
Dock the same PAHs into the same **PahP** receptor with **your** tool, in **two explicit steps**
(preprocessing → docking), and hand back **one** standardized `results/DOCKING_RESULT.json` so we can
compare all tools fairly. (PahS is optional/secondary — see §9.)

## 2. Get your branch + workspace
```bash
git clone <repo-url> && cd igem-saarland-2026-docking-comparison
git checkout tool/<your-tool>        # e.g. tool/autodock-vina, tool/glide, tool/cb-dock
git pull --tags origin main          # get the frozen canonical input
git rev-parse --short input-v1       # copy this hash -> input_commit_hash in your result file
```
Your whole workspace is **`tools/<your-tool>/`**. Work only there.

## 3. Use ONLY the shared input
Everything you start from lives in `input/canonical/`:
- receptor: `targets/PahP/structure.pdb` (+ `targets/PahP/binding_site.yaml`)
- ligands: `ligands/ligands.sdf` (+ `ligands/ligand_metadata.csv`)
- config: `docking_config.yaml`

## 4. Do NOT modify
- Anything in `input/canonical/`. If you think something is wrong, tell **Elnaz** (coordinator) — it is
  fixed on `main` and re-frozen for everyone. Never edit canonical input on a tool branch.
- Any other tool's workspace (`tools/<other-tool>/`).

## 5. Step 1 — preprocessing (`tools/<your-tool>/preprocessing/`)
State **exactly** what preparation your tool needs and do it. This step is kept separate on purpose so we
can later compare all tools' recipes and try to converge on one shared preprocessing.
- Fill **`preprocessing/PREPROCESSING.yaml`** — the structured manifest. **Keep the keys identical** to the
  other tools (it is read side-by-side by `scripts/compare_preprocessing/`).
- Narrate it in `preprocessing/steps.md`; make it reproducible in `preprocessing/preprocess.sh`.
- Write the prepared receptor/ligand files into `inputs/` (committed — coordinators review everything).
- Change as little as possible from canonical; record any forced deviation (and why) under
  `assumptions_and_deviations`.

## 6. Step 2 — docking (`tools/<your-tool>/docking/`)
Run the docking from your prepared inputs. Put parameters in `configurations/config.yaml`
(box, seed, exhaustiveness, `score_direction`). Native output + logs → `outputs/` (committed for review).

Your tool's Python dependencies are in **`tools/<your-tool>/requirements.txt`** — install with
`pip install -r tools/<your-tool>/requirements.txt`. That file **and** your folder's `.gitignore` are
**managed by Ramin & Elnaz** — don't edit them; if you need a package added, ask a coordinator.
Final chosen poses → `results/poses/` named **`PahP__<ligand>__<tool>__v1.<ext>`**.

## 7. Produce the mandatory result file (the ONE file we compare)
Copy the repo-root template into your workspace, fill it, validate before committing:
```bash
cp results/DOCKING_RESULT.template.json tools/<your-tool>/results/DOCKING_RESULT.json
# fill it (see results/DOCKING_RESULT.example.json for a worked example)
pip install -r scripts/compare_results/requirements.txt
python scripts/compare_results/validate_results.py tools/<your-tool>/results/DOCKING_RESULT.json  # exit 0
git add tools/<your-tool>/ && git commit -m "tool/<tool>: preprocessing + docking + result" && git push origin tool/<your-tool>
```
Keep `status/status.yaml` updated as you progress.

## 8. Report failures — never silently drop a ligand
If a ligand won't dock: give it a `results` row with `"status": "failed"` + a non-null `"failure_reason"`,
and add its id to `"failed_cases"`.

## 9. Fairness rules
- Identical receptor, identical ligand SDF, identical box for everyone.
- Fixed random seed where the tool allows it; record it in `configurations/config.yaml` and `docking_parameters`.
- `score_direction`: **`lower_is_better`** for Vina/Glide, **`higher_is_better`** for GOLD (confirm yours).
- Each result row carries its own `target_id` (`PahP` or `PahS`); one file can hold both. Do PahP at minimum
  (PahS in v1 is a project decision — **TODO**).
- **Never** compare your raw score to another tool's raw score — we only compare **ranks**.

## 10. Final checklist
- [ ] Pulled and used `input-v1` (recorded its short hash as `input_commit_hash`)
- [ ] Worked only in `tools/<my-tool>/` — nothing in `input/canonical/` or another tool's folder
- [ ] Filled `preprocessing/PREPROCESSING.yaml` (step 1) before docking (step 2)
- [ ] Attempted every ligand in `ligand_metadata.csv`; documented all failures
- [ ] `validate_results.py` passes with exit 0
- [ ] Final poses committed under `tools/<my-tool>/results/poses/`
- [ ] `status/status.yaml` up to date

Questions → **Elnaz** (team coordinator). For Git / GitHub issues → Ramin or Elnaz.
