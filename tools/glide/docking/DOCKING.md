# Docking — Glide (Schrodinger)

**Goal of this step:** dock the prepared ligands into the prepared PahP receptor and record results.
Everything that is *not* input preparation lives here. Preprocessing must be finished first (see
[`../preprocessing/steps.md`](../preprocessing/steps.md)).

## Inputs (from step 1)
- Prepared receptor + ligands in [`../inputs/`](../inputs/)
- Parameters in [`../configurations/config.yaml`](../configurations/config.yaml)

## Run
```bash
export SCHRODINGER=/path/to/schrodinger        # e.g. "C:/Program Files/Schrodinger2026-1"
bash ../preprocessing/preprocess.sh            # receptor + ligands + receptor grid
bash run_docking.sh                            # docking, then collect_results.py
```
`run_docking.sh` writes the Glide input file and native output to [`../outputs/`](../outputs/), then calls
[`collect_results.py`](collect_results.py) to build the standardized result and the final poses.

Schrodinger job control refuses to register output files outside the launch directory, so both scripts
launch from `tools/glide/` and move the job `.log` files into `../outputs/` afterwards. If no job server
is running, start one once with `$SCHRODINGER/jsc local-server-start`.

## Protocol
- **Search box / mode:** defined box. `GRID_CENTER` and `OUTERBOX` come from the canonical
  `binding_site.yaml` whenever it is filled in; it is still a PLACEHOLDER, so this run uses the
  **shared provisional box** — the fpocket 4.2.2 Pocket 4 box the AutoDock Vina team proposed
  (`GRID_CENTER 70.83, 71.96, 59.18`, `OUTERBOX 21.3, 19.6, 27.3`). `INNERBOX` is **8 Å**: it bounds
  only the ligand centroid, and Glide requires `outer ≥ inner + longest ligand` on every axis — the
  shortest axis is 19.6 Å and benzo[a]pyrene is 11.46 Å, so 8 is the largest legal value. Glide has
  **no blind-docking mode**, so a defined box is mandatory.
- **Precision:** `PRECISION SP`. On this installation `glide -docking-keywords` reports
  `PRECISION = option('SP','HTVS')` — **XP is not available**, so SP is the only production choice.
  It is also the defensible one: on 190 protein–fragment complexes SP-based protocols performed best and
  XP gave similar cross-docking results at higher cost (Sandor, Kiss & Keseru, *JCIM* 2010, 50:1165).
- **Sampling:** `DOCKING_METHOD confgen` (flexible ligand, Glide default). Five poses kept per ligand
  (`POSES_PER_LIG 5`), post-docking minimization on (`POSTDOCK True`, `POSTDOCK_NPOSE 5`).
- **Scoring:** `EPIK_PENALTIES False` and `POSTDOCKSTRAIN False`, so the reported *docking score* equals
  GlideScore with no penalty terms folded in. Force field `OPLS_2005`, matching grid and receptor prep.
- **Random seed:** **Glide exposes none** — there is no seed keyword in `glide -docking-keywords`.
  `CANONICALIZE True` is the documented substitute: it discards input coordinates and rebuilds each
  ligand from connectivity and stereochemistry, removing the run's dependence on input geometry.
  `random_seed` is therefore recorded as `null`, not invented.
- **Score direction:** `lower_is_better`. The Glide manual states plainly that "favorable scores are
  negative, and the lower (more negative) the better"; Schrodinger's own default sort is ascending on
  `r_i_docking_score`.

## Which number is reported
Glide emits several per-pose properties. The one that goes into `DOCKING_RESULT.json` is the
**docking score** (`r_i_docking_score`), in **kcal/mol** — the value Glide itself ranks compounds by.
`r_i_glide_emodel` ranks poses *within* one ligand and is deliberately not used for cross-ligand ranking.
With Epik penalties and strain correction off, docking score ≡ GlideScore.

`WRITE_CSV True` makes Glide write `glide_dock.csv` listing **every** input ligand, including ones that
produced no pose — that is what lets failures be reported honestly instead of silently dropped.

## Output of this step
1. Native results + logs → `../outputs/` (`glide_dock.in`, `glide_dock.csv`, `glide_dock_lib.sdf`, `.log`)
2. Final chosen poses → `../results/poses/` named `PahP__<ligand>__glide__v1.sdf`
3. The standardized `../results/DOCKING_RESULT.json` — built by `collect_results.py`, then validated with
   `python scripts/compare_results/validate_results.py tools/glide/results/DOCKING_RESULT.json`

## Interpreting the result (before anyone reads the ranking)
The six PAHs are pure hydrocarbons, so GlideScore's lipophilic term — a pairwise sum over lipophilic
carbon atoms — scales roughly with heavy-atom count. "Bigger PAH scores better" is therefore the expected
*default* output of the scoring function, not evidence of tighter binding; scoring functions are
documented to correlate with heavy-atom count across many targets (Jacobsson & Karlen, *JCIM* 2006,
46:1334). Two free internal checks come with this exact ligand set:

- **anthracene vs phenanthrene** (both C14H10) and **pyrene vs fluoranthene** (both C16H10) are isomer
  pairs with identical heavy-atom counts, so any score difference within a pair is size-independent.
- The experimental SPR affinities published for this protein (*iScience* 2023, 26:107912) do **not** rank
  by ring count — naphthalene binds tightest, anthracene weakest. A Glide ranking that runs strictly
  from benzo[a]pyrene down to naphthalene is tracking size, and should be reported as such.

`glucose_NEGCTRL` is a plumbing check (does the pipeline run, does a polar polyol score worse), not
evidence of specificity: it is mismatched to the PAHs on nearly every physicochemical axis, so its score
gap is confounded and cannot be read as pocket complementarity.

## What actually happened (run of 2026-09-02)

All seven canonical ligands docked; no failures. Every best pose sits **0.95–2.72 Å from the grid
centre**, i.e. inside the intended pocket — and in the same place CB-Dock3's blind docking put them.

| ligand | GlideScore (kcal/mol) | rank | ligand efficiency | pose offset from centre |
|---|---|---|---|---|
| anthracene | −6.114 | 1 | −0.437 | 1.20 Å |
| glucose_NEGCTRL | −6.040 | 2 | −0.503 | 0.95 Å |
| fluoranthene | −6.030 | 3 | −0.377 | 2.72 Å |
| benzo_a_pyrene | −6.008 | 4 | −0.300 | 1.96 Å |
| phenanthrene | −5.938 | 5 | −0.424 | 1.52 Å |
| pyrene | −5.883 | 6 | −0.368 | 2.04 Å |
| naphthalene | −5.471 | 7 | **−0.547** | 1.59 Å |

Total 14.6 s CPU. Docking was run **twice** from the identical grid and returned identical scores for
all seven ligands, so the pipeline is deterministic even though Glide exposes no random seed.

### The negative control ranks 2nd — why that is a finding, not a fault

Every ligand is in the same pocket, so this is not a placement problem. The score components explain it:
the PAHs score through lipophilic contact (−2.3 to −2.9) and vdW (−17 to −24) with **zero** H-bond and
near-zero Coulomb, while glucose scores a weak lipophilic −1.0 but gains **H-bond −0.79 and Coulomb
−8.87**. The pocket is only 62% hydrophobic: alongside the five aromatics it presents Ser242, Ser243,
Gln246, His250 and Lys273, and a polyol has real hydrogen-bonding to do there.

The honest reading is that glucose is a *plumbing and property* control, not a specificity control. It
is mismatched to the PAHs on nearly every physicochemical axis, so a score gap in either direction is
confounded and says little about pocket selectivity.

### How much of the ranking is just ligand size?

| | Glide SP | CB-Dock3 (same site) |
|---|---|---|
| r(score vs heavy-atom count), 6 PAHs | **−0.68** | **−1.00** |
| Spearman vs published SPR affinity (n=4) | −1.00 raw · **+0.20** by ligand efficiency | −0.20 raw |

CB-Dock's ranking is almost perfectly explained by ligand size. Glide is less size-driven but still does
not reproduce the experimental order: its raw ranking is inverted against the four ligands with
published SPR affinities for this protein (*iScience* 2023, 26:107912), whereas size-normalised **ligand
efficiency correctly puts naphthalene first**, matching the experimental result that naphthalene binds
tightest. With n = 4 these coefficients are extremely noisy and no significance is claimed.

Neither tool reproduces the experimental affinity order — which is the documented, expected behaviour of
docking scoring functions. Compare **ranks** across tools, never raw scores.
