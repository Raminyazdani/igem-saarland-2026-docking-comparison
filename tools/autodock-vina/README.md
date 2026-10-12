# AutoDock Vina — PahP / PahS docking and MD

Branch: `tool/autodock-vina` · Divyashree (PahP, MD, models) · Ana (PahS docking)

AutoDock Vina 1.2.7 docking of the canonical PAH panel into PahP and PahS, with 100 ns explicit-solvent MD and MM-GBSA rescoring for pyrene and phenanthrene. Two independent MD replicates per ligand.

## Key findings

**Pocket 4 is PahP's best site by every static criterion.** fpocket found 17 pockets; ranked on a hydrophobicity / apolar-SASA / aromatic-count composite (not fpocket's druggability score, which is calibrated for oral drugs), pocket 4 ranks first in 59 of 66 weight combinations (89%). Blind docking agrees: 14 of the top 20 poses land there, best -7.98 kcal/mol. Lining includes four aromatics — PHE123, TYR271, TYR274, PHE306.

**PahS has no robust pocket.** The weight sweep splits four ways: pocket 36 in 28 of 66 combinations (42%), pocket 32 in 27 (41%), pocket 58 in 10 (15%), pocket 20 in 1 (2%). Justifies the blind-docking mode mandated by `docking_config.yaml`.

**Docking scores track ring count across the whole panel.**

| ligand | rings | Vina (kcal/mol) |
|---|---|---|
| benzo[a]pyrene | 5 | -9.520 |
| fluoranthene | 4 | -8.095 |
| pyrene | 4 | -8.021 |
| phenanthrene | 3 | -7.448 |
| anthracene | 3 | -7.363 |
| naphthalene | 2 | -6.053 |
| glucose (negative control) | 0 | -5.383 |

The two 4-ring isomers are separated by 0.074 kcal/mol and the two 3-ring isomers by 0.085 — both far inside Vina's ~1 kcal/mol resolution, so those pairs are ties. The non-aromatic control ranks last, as it should.

**The docked pose is metastable: two replicates, opposite outcomes.** Each ligand was run twice for 100 ns from the same equilibrated structure, differing only in the initial velocity seed.

| | pyrene run 1 | pyrene run 2 | phenanthrene run 1 | phenanthrene run 2 |
|---|---|---|---|---|
| in contact with pocket 4 (<0.5 nm) | 19.8% | **100.0%** | 8.0% | **99.7%** |
| last contact | 23.3 ns | 100 ns | 8.0 ns | 100 ns |
| mean distance, final 50 ns | 1.49 nm | 0.23 nm | 2.00 nm | 0.25 nm |

In run 1 both ligands left pocket 4 and never returned — pyrene loosening from ~13 ns and departing at 23.3 ns, phenanthrene leaving in a single step at 8.0 ns — each settling 1.5–2 nm away in an adjacent hydrophobic region. In run 2 both stayed for the full 100 ns. Figure: `md/analysis/pocket4_replicates.png`.

A single 100 ns trajectory would have supported either conclusion with equal confidence. That is the central methodological result here.

**Where the ligand stays bound, binding is strong and the two ligands separate cleanly.** MM-GBSA over the whole of run 2, 500 frames per ligand, both in the pocket throughout:

| | pyrene | phenanthrene |
|---|---|---|
| ΔTOTAL | **-28.43 ± 3.73** | **-18.71 ± 3.06** |
| SEM | 0.17 | 0.14 |
| ΔVDWAALS | -32.94 | -24.06 |
| ΔEEL | -5.82 | -3.47 |

Pyrene is 9.7 kcal/mol more favourable. Allowing generously for frame correlation — an effective sample of 20 independent points rather than 500 — the separation is still around 9σ.

**This agrees with Vina, and dissolves the earlier "methods disagree" result.** Vina ranks pyrene above phenanthrene (-8.02 vs -7.45) and so does MM-GBSA once both are measured in the same pocket with the ligand actually in it. The apparent conflict in the first analysis came from comparing two different binding sites, computed on frames after each ligand had already left.

**Docking found the right pocket but not the best pose.** Pyrene's van der Waals term roughly doubles between the docked pose and the relaxed one — -17.33 kcal/mol over the 2–13 ns window of run 1 against -32.94 over run 2 — as the ligand settles deeper and picks up VAL124, LEU125, HID102 and LEU244 beyond the original fpocket lining. The Vina pose was in the right place and a substantially worse geometry than MD finds.

**Superseded results.** The earlier MM-GBSA values (pyrene -13.88 ± 4.21 over 29.8–99.8 ns, phenanthrene -18.12 ± 4.41 over 4.8–99.8 ns) were computed on run 1 over windows that postdate dissociation; they describe each ligand's post-migration site, and the two describe *different* sites. The Kd derived from them — pyrene ~0.16 nM, phenanthrene ~0.17 pM — are withdrawn. A ranking by residence time in pocket 4, reported earlier, was a single-run artefact and does not survive the replicate.

**Limits.**
- Two replicates per ligand, which is enough to show the outcome is seed-dependent and not enough to say how often each outcome occurs. A third replicate is running.
- No Kd should be derived from any of these ΔG. MM-GBSA omits configurational entropy, so -28.43 would imply ~10⁻²¹ M, and the error grows with burial. The values are comparative only.
- Phenanthrene's run 2 shifts into the adjacent THR254/PHE256/LEU258/LYS262 subsite while keeping contact with the pocket-4 lining throughout, so its -18.71 is a slightly displaced pose within the same pocket rather than the identical sub-site pyrene occupies.
- Both ligands were simulated once per replicate at a single concentration in a single protonation state.

## Pipeline

| Step | Where | Entry point |
|---|---|---|
| preprocessing | `preprocessing/` | `preprocess.sh` — reads `input/canonical/`, writes `inputs/`, reproduces committed inputs byte-for-byte |
| pocket prediction | `preprocessing/pocket_prediction/` | `rank_pockets.py <fpocket_dir>`, `check_blind_docking.py` |
| docking | `docking/` | `dock_ligand.py <ligand>` reads the box from `configurations/config.yaml`; `run_docking.sh` loops it over the panel |
| MD | `md/` | `jobs/run_md.sh <ligand>` — GROMACS 2026.3, ff14SB/GAFF2/TIP3P, 310 K, 8 Cl⁻ counterions, no added salt |
| replicates | `md/analysis/` | `replicate_md.sh` — fresh velocities from a new seed, started from `npt.gro` |
| MM-GBSA | — | gmx_MMPBSA 1.6.5, igb=5, 150 mM implicit salt (PB did not complete) |
| stability analysis | `md/analysis/` | `md_analysis.sh <run_dir> <resname>`, `plot_replicates.py` |
| ODE models | `md/models/` | `model1_binding.py`, `model2_reporter.py`, `model3_competition.py` — all on one illustrative Kd ladder |

## Discarded

- **Per-residue decomposition** (`idecomp = 2`): zero contribution for every protein residue, full interaction energy on the ligand, SDs are propagation artifacts (√2 × per-term SD). Input file was correct; the RRES/LRES partition does not attribute cross terms to the protein side.
- **Ligand RMSD traces** (`*_ligand_rmsd.xvg`): did not measure displacement in the protein frame; removed from the repo, superseded by the mindist traces in `md/analysis/`.
- **Residence-time ranking**: a single-run artefact, not reproduced in replicate 2.

## Known inconsistency

PahP ligands prepared with Open Babel 3.1.0, PahS ligands with Meeko 0.7.1. Not harmonised: PAHs have no rotatable bonds so Meeko's advantage does not apply, and redoing PahP would invalidate the MD.

## Rules

- Read inputs only from `input/canonical/`. Never edit canonical inputs.
- Touch only `tools/autodock-vina/`.
- Compare **ranks**, never raw scores across tools.
