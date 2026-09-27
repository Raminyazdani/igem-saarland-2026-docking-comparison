# MM-GBSA results — PahP + PAHs

100 ns GROMACS MD (GPU, 310 K), MM-GBSA via gmx_MMPBSA 1.6.5 (igb=5, 150 mM salt).
PB was attempted but did not complete; GB only.

| Ligand | Rings | Vina (kcal/mol) | MM-GBSA dG (kcal/mol) | Frames |
|---|---|---|---|---|
| pyrene | 4 | -8.02 | -13.88 +/- 4.21 | 351 (30-100 ns) |
| phenanthrene | 3 | -7.45 | -18.12 +/- 4.41 | 476 (5-100 ns) |

Binding is dominated by van der Waals in both cases (dEEL approx -1.5 to -1.9 kcal/mol);
phenanthrene has the more favourable vdW term (-21.7 vs -17.3) despite being smaller.

## Notes
- MM-GBSA and Vina disagree on the ranking of pyrene vs phenanthrene.
- Both ligands moved 2.4-3.0 A from their docked poses within the first 10-30 ns
  (see *_ligand_rmsd.xvg) and remained stable thereafter, so MD and docking describe
  different geometries. Pyrene's analysis excludes the first 30 ns for this reason.
- Single replica per ligand; SDs overlap, so the difference is not statistically clean.
- MM-GBSA omits configurational entropy, so absolute dG overestimates affinity.
  Derived Kd values (pyrene ~1.6 nM, phenanthrene ~1.4 pM) are relative indicators,
  not measurements.
- A single wet-lab affinity measurement would resolve the disagreement more
  effectively than further computation.
