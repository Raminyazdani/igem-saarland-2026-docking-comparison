# MM-GBSA results — PahP + PAHs

100 ns GROMACS MD (GPU, 310 K, TIP3P, neutralised with 8 Cl- counterions and no added salt), MM-GBSA via gmx_MMPBSA 1.6.5 (igb=5, 150 mM *implicit* salt). PB was attempted but did not complete; GB only. Note the ionic-strength mismatch between the explicit MD (~29 mM from counterions alone) and the implicit rescoring (150 mM); it is unlikely to matter for neutral hydrophobic ligands, but it is a real inconsistency between the two stages.

**These ΔG values do not describe pocket 4.** Both ligands dissociate from the docked site early in the run, and the MM-GBSA windows lie almost entirely after that. See `../analysis/` for the evidence.

| Ligand | Rings | Vina (kcal/mol) | MM-GBSA ΔG (kcal/mol) | Frames | Site the ΔG describes |
|---|---|---|---|---|---|
| pyrene | 4 | -8.02 | -13.88 ± 4.21 | 351 (30–100 ns) | LEU10/ILE40–GLN51 surface patch |
| phenanthrene | 3 | -7.45 | -18.12 ± 4.41 | 476 (5–100 ns) | ILE136–PRO292 buried cavity |

Binding is dominated by van der Waals in both cases (ΔEEL ≈ -1.5 to -1.9 kcal/mol); phenanthrene has the more favourable vdW term (-21.7 vs -17.3) despite being smaller.

## Dissociation from pocket 4

Minimum distance from each ligand to the pocket-4 lining over the full trajectory:

| | pyrene | phenanthrene |
|---|---|---|
| in contact with pocket 4 (<0.5 nm) | 19.8% of run | 8.0% of run |
| last contact | 23.3 ns | 8.0 ns |
| mean distance, final 50 ns | 1.49 nm | 2.00 nm |

Both start in pocket 4 — the 0 ns contact lists reproduce the fpocket lining almost residue for residue — and neither returns after leaving. Pyrene loosens from ~13 ns with repeated returns before departing at 23.3 ns; phenanthrene leaves in a single step at 8.0 ns. Both settle 1.5–2 nm away in adjacent hydrophobic regions.

Pyrene's MM-GBSA window begins at 30 ns, entirely post-dissociation. Phenanthrene's begins at 5 ns, so roughly 3 of its 95 ns are in-pocket.

## Recomputed over defined-site windows

`md/analysis/windows/` holds four reruns on windows where each ligand is in one site:

| window | pyrene | phenanthrene |
|---|---|---|
| pocket 4, ligand still bound | -16.64 ± 5.46 (frames 11–66, 2–13 ns) | -17.38 ± 4.09 (frames 6–36, 1–7 ns) |
| final site, 50–100 ns | -14.95 ± 1.89 | -19.82 ± 3.03 |

At pocket 4 the two are indistinguishable: 0.74 kcal/mol apart against a combined SEM of ~1.03, and consecutive frames are correlated so the effective sample is smaller than 56 and 31. MM-GBSA cannot rank these ligands at a common site.

For pyrene, MM-GBSA scores pocket 4 (-16.64) above the site it settled into from ~37 ns and held for the remaining 60 ns (-14.95) — the method contradicts the trajectory. For phenanthrene the two agree. Reproduce with `windows/rerun_mmgbsa.sh`.

## What this changes

- **The derived Kd values are withdrawn.** Previously quoted as pyrene ~0.16 nM and phenanthrene ~0.17 pM, they were computed from ΔG values that describe post-migration sites.
- **The Vina/MM-GBSA ranking disagreement was not real.** The two original values came from different sites; recomputed at a common site the two ligands are statistically indistinguishable, so MM-GBSA never inverted the Vina order — it simply cannot resolve these ligands.
- **The per-residue decomposition is discarded.** `idecomp = 2` returned zero contribution for every protein residue, with the full interaction energy assigned to the ligand; its standard deviations are propagation artifacts.
- **The earlier statement that both ligands "moved 2.4–3.0 Å from their docked poses and remained stable thereafter" is superseded.** The actual displacement is 15–20 Å. The `*_ligand_rmsd.xvg` traces do not measure displacement in the protein frame and should be re-derived or dropped.

## What survives

The ranking by **residence time in pocket 4** — pyrene ~2.5× longer than phenanthrene — matches the Vina ordering (-8.02 vs -7.45 kcal/mol), and is the only MD-derived measure that separates the two ligands. The docking-stage results are unaffected: fpocket geometry, the weight-sensitivity sweep and the contact-based blind-docking check are all static-structure analyses.

## Caveats

- Single replicate per ligand, no repeats with different seeds. The dissociation is suggestive, not established.
- Residence times are compared between two single runs, with no error bars.
- MM-GBSA omits configurational entropy, so absolute ΔG overestimates affinity regardless of which site it describes.
- A single wet-lab affinity measurement would resolve more than further computation.
