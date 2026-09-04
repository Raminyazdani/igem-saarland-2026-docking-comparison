# Reproducing the Glide result

Everything in `results/` can be regenerated from `input/canonical/` with two scripts. This page is the
short version; the reasoning behind each choice is in [`preprocessing/steps.md`](preprocessing/steps.md)
and [`docking/DOCKING.md`](docking/DOCKING.md).

## 1. What you need

| | |
|---|---|
| **Schrödinger Suite** | 2026-1 (Glide v11.0), **with a licence**. Not pip-installable. |
| **Python** | CPython 3.8+ on PATH. Standard library only — see `requirements.txt`. |
| **Shell** | bash. Git Bash works on Windows; the scripts detect the `.exe` launchers themselves. |

Check the licence and the job server before starting — these are the two things that actually stop a run:

```bash
export SCHRODINGER="/path/to/schrodinger"      # e.g. "/c/Program Files/Schrodinger2026-1"
"$SCHRODINGER/licadmin" debug-sources          # must list a local entitlement or a licence server
"$SCHRODINGER/jsc" local-server-start          # Glide refuses to launch without a job server
```

If `licadmin` prints two empty lists, every step below fails at the first structure read with
`(SLM) -1: Could not find a valid license file`. That is a licence problem, not a workflow problem.

## 2. Run it

```bash
cd tools/glide
bash preprocessing/preprocess.sh     # receptor prep, ligand prep, receptor grid   (~3 min)
bash docking/run_docking.sh          # Glide SP docking + result extraction        (~1 min)
```

`run_docking.sh` calls `docking/collect_results.py` itself, so `results/DOCKING_RESULT.json` and
`results/poses/` are written at the end of the second command.

Then validate, exactly as CI does:

```bash
pip install -r requirements.txt      # repo root: jsonschema, pyyaml, pandas, ...
python scripts/compare_results/validate_results.py tools/glide/results/DOCKING_RESULT.json
```

Expected: `1/1 file(s) passed`, exit code 0.

## 3. What you should get

7 ligands, 0 failures, and these scores (kcal/mol, lower is better):

```
anthracene -6.114 · glucose_NEGCTRL -6.040 · fluoranthene -6.030 · benzo_a_pyrene -6.008
phenanthrene -5.938 · pyrene -5.883 · naphthalene -5.471
```

Every best pose lands 0.95–2.72 Å from the grid centre. Total docking cost ≈ 15 s CPU.

## 4. Is it deterministic?

**Glide exposes no random seed** — there is no seed keyword in `glide -docking-keywords`. Reproducibility
therefore rests on pinning the inputs, not on a seed. `CANONICALIZE True` is the documented substitute:
it discards the input coordinates and rebuilds each ligand from connectivity and stereochemistry, so the
run does not depend on the input geometry.

This was **tested, not assumed**. Docking was run twice from the identical grid:

```bash
cp outputs/glide_dock.csv /tmp/run1.csv
bash docking/run_docking.sh
# compare the best score per ligand between /tmp/run1.csv and outputs/glide_dock.csv
```

All seven scores came back identical. So: same Schrödinger release + same prepared inputs ⇒ same numbers.
Across a *different* Schrödinger release, assume nothing.

## 5. Where the numbers come from

- **Reported score** — `r_i_docking_score` from `outputs/glide_dock.csv`, kcal/mol, lower is better.
  With `EPIK_PENALTIES False` and `POSTDOCKSTRAIN False` it equals GlideScore exactly.
- **Ranking** — ascending by that score, which is also Glide's own default sort.
- **Poses** — `outputs/glide_dock_lib.sdf` is sorted globally best-first, so the first record for each
  ligand is its best pose; that is what lands in `results/poses/`.
- **Failures** — `outputs/glide_dock_skip.csv` carries Glide's own message per ligand. `WRITE_CSV` and
  `KEEPSKIPPED` are on precisely so a ligand can never be silently dropped. This run had none.

Nothing is retyped by hand: `collect_results.py` copies values straight from the native CSV.

## 6. If you change the binding box

The box is read from `input/canonical/targets/PahP/binding_site.yaml` whenever it is defined, and only
falls back to `configurations/config.yaml` while the canonical file is still a placeholder. When
`input-v1` freezes a box, just rerun both scripts — no edits needed.

One Glide-specific constraint to respect: `OUTERBOX ≥ INNERBOX + 11.46 Å` on **every** axis (11.46 Å is
benzo[a]pyrene, the longest canonical ligand). `preprocess.sh` enforces this per axis and stops rather
than building a grid that would clip the largest ligand. That is why `INNERBOX` is 8 here and not the
usual 10 — the shared box is only 19.6 Å on its shortest axis.

**Validate any new centre against free volume before trusting it.** A box centre that sits inside protein
density will still produce a grid and still produce scores — they will just be meaningless. That happened
once in this workspace and is documented in `preprocessing/steps.md`.

## 7. Regenerating the report and diagram

`REPORT.pdf` was rendered from `REPORT.html` with headless Edge; `workflow.svg` is hand-authored and
opens in any browser:

```bash
msedge --headless --disable-gpu --print-to-pdf=REPORT.pdf --no-pdf-header-footer REPORT.html
```

Neither is needed to reproduce the science — they are read-only summaries of it.
