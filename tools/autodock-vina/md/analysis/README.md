# MD stability analysis — PahP / pyrene, phenanthrene

Tests whether the Vina docked pose in pocket 4 survives 100 ns of explicit-solvent MD, across three independent replicates per ligand, and rescores MM-GBSA where the ligand is in a defined site.

## Result

Three replicates per ligand from the same equilibrated structure, each with velocities regenerated from a Maxwell distribution at 310 K under a different seed.

| | rep 1 | rep 2 | rep 3 |
|---|---|---|---|
| **pyrene** — in contact (<0.5 nm) | 19.8% | 100.0% | 100.0% |
| last contact | 23.3 ns | 100 ns | 100 ns |
| mean distance, 50–100 ns | 1.49 nm | 0.23 nm | 0.22 nm |
| **phenanthrene** — in contact | 8.0% | 99.7% | 21.1% |
| last contact | 8.0 ns | 100 ns | 21.1 ns |
| mean distance, 50–100 ns | 2.00 nm | 0.25 nm | 1.92 nm |

**The docked pose is metastable, and pyrene holds it more reliably.** Pyrene retains it for the full 100 ns in 2 of 3 runs, phenanthrene in 1 of 3; averaged over all simulated time, pyrene is in contact 73% against phenanthrene's 43%. Where a ligand leaves, it leaves once and does not return, settling 1.5–2 nm away in an adjacent hydrophobic region.

Per-run detail. Rep 1 pyrene loosens from ~13 ns with repeated returns, departs at 23.3 ns, transits the surface (ASP167/LYS168/LYS169 at 25 ns) and settles from ~37 ns at LEU10, ILE40, THR41, LEU44, SER45, PRO48, GLN51. Rep 1 phenanthrene leaves in one step at 8.0 ns into a buried cavity: ILE136, LEU139, SER140, LEU142, PHE143, ASP194, ILE195, PRO223, ILE225, ILE237, ALA284, LEU289, HID290, PHE291, PRO292. Rep 3 phenanthrene leaves at 21.1 ns. In the runs that stay bound, pyrene's contact list remains on the pocket-4 lining throughout and gains VAL124, LEU125, HID102, LEU244 as it settles deeper; phenanthrene shifts into the adjacent THR254/PHE256/LEU258/LYS262 subsite without losing contact with PHE123, LEU247, HID250, VAL270 or TYR274.

With roughly a coin-flip chance of retention per run, a single 100 ns trajectory could have supported either "the pose is stable" or "docking failed" with equal apparent confidence. Replication is what distinguishes the two.

Note that rep 1 differs from reps 2 and 3 in more than the seed: it continued from `npt.gro` with velocities carried over, while reps 2 and 3 regenerate them. Both sample the same ensemble, so the split is most likely stochastic, but it is not a pure seed comparison.

Figure: `pocket4_replicates.png`.

## Files

| file | contents |
|---|---|
| `md_analysis.sh` | builds the pocket-4 index group, runs `gmx mindist`, prints contact fraction, last contact and tail mean |
| `replicate_md.sh` | independent replicate — fresh velocities from a new seed, started from `npt.gro`, not a continuation |
| `plot_replicates.py` | produces `pocket4_replicates.png` from the six `.xvg` traces |
| `pyrene_rep1_mindist.xvg` … `pyrene_rep3_mindist.xvg` | pyrene to pocket-4 lining, 10001 frames over 100 ns |
| `phenanthrene_rep1_mindist.xvg` … `phenanthrene_rep3_mindist.xvg` | same for phenanthrene |
| `pocket4_replicates.png` | the figure |
| `fig_pocket4_docked.png` | docked pose in pocket 4 |
| `fig_pyrene_migration.png` | **rep 1 only** — pyrene's docked and 75 ns positions. Does not represent reps 2 and 3, where it never moves. |
| `fig_phenanthrene_finalsite.png` | **rep 1 only** — phenanthrene's 75 ns site |
| `pyrene_75ns.pdb`, `phenanthrene_75ns.pdb` | rep 1 snapshots at 75 ns, protein + ligand |
| `pyrene_75ns_out/`, `phenanthrene_75ns_out/` | fpocket on those snapshots |
| `figures.pml`, `figures_v2.pml` | PyMOL scene definitions |
| `windows/` | MM-GBSA over defined-site windows of rep 1, plus `rerun_mmgbsa.sh` |

Reproduce, from the jobs directory on the compute host:

```
bash md_analysis.sh jobs/pyrene_run PYR
bash md_analysis.sh jobs/pyrene_run/rep2 PYR
bash md_analysis.sh jobs/pyrene_run/rep3 PYR
bash md_analysis.sh jobs/phenanthrene_run PHN
bash md_analysis.sh jobs/phenanthrene_run/rep2 PHN
bash md_analysis.sh jobs/phenanthrene_run/rep3 PHN
python plot_replicates.py pocket4_replicates.png
```

Pocket-4 lining used for the distance: residues 123, 250, 270, 271, 272, 274, 306 (129 atoms). Contact threshold 0.5 nm.

## MM-GBSA

Replicate 2, 0–100 ns, 500 frames, both ligands in the pocket throughout — **the values to use**:

| | pyrene | phenanthrene |
|---|---|---|
| ΔTOTAL | -28.43 ± 3.73 (SEM 0.17) | -18.71 ± 3.06 (SEM 0.14) |

Replicate 2 is the only run in which both ligands stayed bound for the full 100 ns, which is what makes it the one usable same-site comparison. Raw output in `../results/rep2/`.

Rep 1 windows, kept in `windows/` for the record and **superseded**:

| window | frames | pyrene | phenanthrene |
|---|---|---|---|
| pocket 4 while occupied | 11–66 / 6–36 | -16.64 ± 5.46 | -17.38 ± 4.09 |
| final site, 50–100 ns | 251–500 | -14.95 ± 1.89 | -19.82 ± 3.03 |

`md_fit.xtc` is 501 frames at 200 ps, so frame *n* is (*n*−1) × 200 ps. The original rep-1 analysis used `startframe = 150` (pyrene) and `25` (phenanthrene), i.e. 29.8–99.8 ns and 4.8–99.8 ns — after dissociation in both cases.

## Site detection, rep 1 destinations

- pyrene's site — best overlap 2/7 (pocket 15). Not a detected cavity.
- phenanthrene's site — 7/15 with pocket 17, a further 5/15 with pocket 23, in both the starting structure and the 75 ns snapshot.

No cryptic pocket opened. Phenanthrene's rep-1 destination spans two separately-detected pockets, so a per-pocket ranking cannot score it as a unit — detection divides the site before the ranking sees it, and neither half ranks well alone (pocket 17 scored 0.317, 8th of 13).

## Caveats

- Three replicates per ligand. Enough to establish that the pose is metastable and to order the two ligands; not enough for a retention probability with a meaningful confidence interval.
- Pocket-4 identification from docking is unaffected by any of this — fpocket geometry, the weight sweep and the contact-based pose assignment are static-structure results.
