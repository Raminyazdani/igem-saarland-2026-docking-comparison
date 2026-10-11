# AutoDock Vina — PahP / PahS docking and MD

Branch: `tool/autodock-vina` · Divyashree (PahP, MD) · Ana (PahS docking)

AutoDock Vina 1.2.7 docking of the canonical PAH panel into PahP and PahS, with 100 ns explicit-solvent MD and MM-GBSA rescoring for pyrene and phenanthrene.

## Key findings

**Pocket 4 is PahP's best site by every static criterion.** fpocket found 17 pockets; ranked on a hydrophobicity / apolar-SASA / aromatic-count composite (not fpocket's druggability score, which is calibrated for oral drugs), pocket 4 ranks first in 59 of 66 weight combinations (89%). Blind docking agrees: 14 of the top 20 poses land there, best -7.98 kcal/mol. Lining includes four aromatics — PHE123, TYR271, TYR274, PHE306.

**PahS has no robust pocket.** The weight sweep splits four ways: pocket 36 in 28 of 66 combinations (42%), pocket 32 in 27 (41%), pocket 58 in 10 (15%), pocket 20 in 1 (2%). Justifies the blind-docking mode mandated by `docking_config.yaml`.

**Neither PAH stays in pocket 4 under MD.**

| | pyrene | phenanthrene |
|---|---|---|
| in contact with pocket 4 (<0.5 nm) | 19.8% of 100 ns | 8.0% of 100 ns |
| last contact | 23.3 ns | 8.0 ns |
| mean distance, final 50 ns | 1.49 nm | 2.00 nm |
| ends at | LEU10/ILE40–GLN51 surface patch | ILE136–PRO292 buried cavity |

Both start where docking placed them, both leave, neither returns. Pyrene loosens from ~13 ns and departs at 23.3 ns; phenanthrene leaves in one step at 8.0 ns. Figure: `md/analysis/pocket4_dissociation.png`.

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

**The MM-GBSA free energies describe the wrong sites, so the derived Kd values are withdrawn.**

| Ligand | Vina | MM-GBSA ΔG | Frames | Site the ΔG describes |
|---|---|---|---|---|
| pyrene | -8.02 | -13.88 ± 4.21 | 351 (30–100 ns) | surface patch |
| phenanthrene | -7.45 | -18.12 ± 4.41 | 476 (5–100 ns) | buried cavity |

Pyrene's window is entirely post-dissociation; ~3 of phenanthrene's 95 ns are in-pocket. The withdrawn values were pyrene ~0.16 nM and phenanthrene ~0.17 pM.

**Recomputed over windows where each ligand is in a defined site** (`md/analysis/windows/`):

| window | pyrene | phenanthrene |
|---|---|---|
| pocket 4, ligand still bound | -16.64 ± 5.46 (2–13 ns) | -17.38 ± 4.09 (1–7 ns) |
| final site, 50–100 ns | -14.95 ± 1.89 | -19.82 ± 3.03 |

**At pocket 4 the two ligands are indistinguishable.** The difference is 0.74 kcal/mol against a combined SEM of ~1.03 — about 0.7σ, and optimistic at that, since consecutive MD frames are correlated. MM-GBSA cannot rank these two at a common site, so the earlier "MM-GBSA ranks phenanthrene above pyrene" was never a real inversion of the Vina order: it was noise plus two values taken from different sites.

**MM-GBSA also contradicts the trajectory for pyrene.** It scores pocket 4 (-16.64) as more favourable than the site pyrene settled into from ~37 ns and held for the remaining 60 ns of the run (-14.95). A method that ranks a site above the one the ligand demonstrably prefers is reporting its own limitations — MM-GBSA omits configurational entropy and treats desolvation crudely, so a buried aromatic pocket scores well on enthalpy while the real free-energy balance sends the ligand elsewhere. For phenanthrene the two agree (-17.38 at pocket 4 vs -19.82 at its final site), which makes pyrene the informative case.

**Residence time is the only MD measure that separates the two ligands.** Pyrene holds pocket 4 ~2.5× longer than phenanthrene, matching the Vina order (-8.02 vs -7.45). MM-GBSA at a common site cannot separate them at all.

**A per-pocket ranking cannot find phenanthrene's site.** It overlaps pocket 17 by 7/15 residues and pocket 23 by 5/15, in both the starting structure and a 75 ns snapshot. No cryptic pocket opened — the site straddles two detected pockets, so detection splits it before ranking sees it, and neither half ranks well alone (pocket 17: 0.317, 8th of 13). Pyrene's site matches nothing (best 2/7).

**Limits.** One 100 ns replicate per ligand, no seed repeats, no error bars on residence times. A ligand scoring -8.02 kcal/mol (≈2 μM) should have a residence time of microseconds, not nanoseconds — so either the pose is worse than the score implies, or pocket 4 is not a real PAH site on this structure. One wet-lab affinity measurement would settle more than further computation.

## Pipeline

| Step | Where | Entry point |
|---|---|---|
| preprocessing | `preprocessing/` | `preprocess.sh` — reads `input/canonical/`, writes `inputs/`, reproduces committed inputs byte-for-byte |
| pocket prediction | `preprocessing/pocket_prediction/` | `rank_pockets.py <fpocket_dir>`, `check_blind_docking.py` |
| docking | `docking/` | `dock_ligand.py <ligand>` — pocket-4 box, center 70.83/71.96/59.18, size 21.3/19.6/27.3 |
| MD + MM-GBSA | `md/` | GROMACS 2026.3, ff14SB/GAFF2/TIP3P, 310 K; gmx_MMPBSA 1.6.5, igb=5 (PB did not complete) |
| stability analysis | `md/analysis/` | `md_analysis.sh <run_dir> <resname>`, `plot_mindist.py` |
| ODE models | `md/models/` | `model1_binding.py`, `model2_reporter.py`, `model3_competition.py` — all on one illustrative Kd ladder |

## Discarded

- **Per-residue decomposition** (`idecomp = 2`): zero contribution for every protein residue, full interaction energy on the ligand, SDs are propagation artifacts (√2 × per-term SD). Input file was correct; the RRES/LRES partition does not attribute cross terms to the protein side.
- **MM-GBSA as a ligand-ranking method here.** Even on correct frames at a common site it cannot distinguish pyrene from phenanthrene, and for pyrene it contradicts the trajectory. Reported for completeness, not used to rank.
- **Ligand RMSD traces** (`*_ligand_rmsd.xvg`): the earlier "moved 2.4–3.0 Å and remained stable" is superseded — actual displacement is 15–20 Å. Not measured in the protein frame.

## Known inconsistency

PahP ligands prepared with Open Babel 3.1.0, PahS ligands with Meeko 0.7.1. Not harmonised: PAHs have no rotatable bonds so Meeko's advantage does not apply, redoing PahP would invalidate the MD, and the ligands leave the pocket regardless.

## Rules

- Read inputs only from `input/canonical/`. Never edit canonical inputs.
- Touch only `tools/autodock-vina/`.
- Compare **ranks**, never raw scores across tools.
