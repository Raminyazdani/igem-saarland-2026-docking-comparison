# MM-GBSA results — PahP + PAHs

100 ns GROMACS MD (GPU, 310 K, TIP3P, neutralised with 8 Cl⁻ counterions and no added salt), MM-GBSA via gmx_MMPBSA 1.6.5 (igb=5, 150 mM *implicit* salt). PB was attempted but did not complete; GB only. Note the ionic-strength mismatch between the explicit MD (~29 mM from counterions alone) and the implicit rescoring (150 mM); unlikely to matter for neutral hydrophobic ligands, but it is a real inconsistency between the two stages.

Three independent replicates per ligand. **Which replicate a number comes from determines what it means** — see `../analysis/` for the stability evidence.

## The values to use

Replicate 2, the one run in which both ligands stayed in pocket 4 for the full 100 ns, giving the only well-sampled same-site comparison. 500 frames each, 0–100 ns.

| | pyrene | phenanthrene |
|---|---|---|
| ΔVDWAALS | -32.94 | -24.06 |
| ΔEEL | -5.82 | -3.47 |
| ΔGGAS | -38.75 | -27.52 |
| ΔGSOLV | +10.32 | +8.82 |
| **ΔTOTAL** | **-28.43 ± 3.73** | **-18.71 ± 3.06** |
| SEM | 0.17 | 0.14 |

Raw output: `rep2/pyrene_FINAL_RESULTS.dat` and `rep2/phenanthrene_FINAL_RESULTS.dat`, committed here.

Pyrene is 9.7 kcal/mol more favourable, and the separation survives even a pessimistic correction for frame correlation (~9σ at an assumed effective sample of 20). Binding is van der Waals dominated in both cases, with the ratio tracking ring count — 4 rings bury more than 3.

This **agrees with the Vina ranking** (-8.02 vs -7.45) and with the residence-time ordering across replicates (73% vs 43% of simulated time in contact with pocket 4). The earlier report that the methods disagreed was an artefact of comparing different sites on under-sampled frames.

## Superseded values

| run / window | pyrene | phenanthrene | why it does not describe pocket 4 |
|---|---|---|---|
| rep 1, 29.8–99.8 ns (original) | -13.88 ± 4.21 | -18.12 ± 4.41 | both ligands had already left; the two describe *different* post-migration sites |
| rep 1, pocket 4 while occupied | -16.64 ± 5.46 (2–13 ns) | -17.38 ± 4.09 (1–7 ns) | only 56 and 31 frames, of a dissociating state |
| rep 1, final site, 50–100 ns | -14.95 ± 1.89 | -19.82 ± 3.03 | a different site for each ligand |

These are kept in `../analysis/windows/` for the record. The Kd derived from the original pair — pyrene ~0.16 nM, phenanthrene ~0.17 pM — are **withdrawn**.

Note what the rep-1 windows did to the comparison: at 56 and 31 frames the two ligands came out 0.74 kcal/mol apart against a combined SEM of ~1.03, i.e. indistinguishable, and the conclusion drawn was that MM-GBSA could not resolve them. With 500 frames of a bound complex they are 9.7 kcal/mol apart. The method was never the problem; the sampling was.

## Do not derive a Kd

RT·ln on -28.43 kcal/mol gives roughly 10⁻²¹ M. MM-GBSA omits configurational entropy and treats desolvation crudely, and the overestimate grows with burial — so the deeper the ligand sits, the worse the absolute number. These ΔG are comparative only.

## Caveats

- MM-GBSA was run on replicate 2 only. The bound portions of replicates 1 and 3 are too short to rescore meaningfully.
- Phenanthrene's replicate 2 shifts into the adjacent THR254/PHE256/LEU258/LYS262 subsite while keeping contact with the pocket-4 lining throughout. Its value is for a slightly displaced pose within the same pocket.
- The per-residue decomposition (`idecomp = 2`) returned zero for every protein residue with the whole interaction energy on the ligand; its SDs are propagation artifacts. Discarded.
- A single wet-lab affinity measurement would resolve more than further computation.
