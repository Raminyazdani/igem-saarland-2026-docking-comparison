# MD stability analysis — PahP / pyrene, phenanthrene

Tests whether the Vina docked pose in pocket 4 is retained during 100 ns of explicit-solvent MD, across independent replicates, and rescores MM-GBSA over windows where the ligand is in a defined site.

## Result

Two replicates per ligand, same equilibrated structure, differing only in the initial velocity seed.

| | pyrene run 1 | pyrene run 2 | phenanthrene run 1 | phenanthrene run 2 |
|---|---|---|---|---|
| in contact with pocket 4 (<0.5 nm) | 19.8% | 100.0% | 8.0% | 99.7% |
| last contact | 23.3 ns | 100 ns | 8.0 ns | 100 ns |
| mean distance, final 50 ns | 1.49 nm | 0.23 nm | 2.00 nm | 0.25 nm |
| maximum excursion | 4.11 nm | 0.70 nm | 3.24 nm | 0.70 nm |

**Run 1:** both ligands start in pocket 4 — the 0 ns contact lists reproduce the fpocket lining almost residue for residue — and both leave. Pyrene loosens from ~13 ns with repeated returns, departs at 23.3 ns, transits the surface (ASP167/LYS168/LYS169 at 25 ns) and settles from ~37 ns at LEU10, ILE40, THR41, LEU44, SER45, PRO48, GLN51. Phenanthrene leaves in one step at 8.0 ns and settles in a buried cavity: ILE136, LEU139, SER140, LEU142, PHE143, ASP194, ILE195, PRO223, ILE225, ILE237, ALA284, LEU289, HID290, PHE291, PRO292.

**Run 2:** neither leaves. Pyrene's contact list stays on the pocket-4 lining at every timepoint and gains VAL124, LEU125, HID102, LEU244 as it settles deeper. Phenanthrene shifts into the adjacent THR254/PHE256/LEU258/LYS262 subsite but never loses contact with PHE123, LEU247, HID250, VAL270 or TYR274.

**So the docked pose is metastable on this timescale.** A single 100 ns run would have supported either "the pose is stable" or "docking failed" with equal apparent confidence.

Figure: `pocket4_replicates.png`.

## Files

| file | contents |
|---|---|
| `md_analysis.sh` | builds the pocket-4 index group, runs `gmx mindist`, dumps contact lists at 0/10/25/50/75/100 ns |
| `replicate_md.sh` | independent replicate — fresh velocities from a new seed, started from `npt.gro`, not a continuation |
| `plot_replicates.py` | produces `pocket4_replicates.png` from the four `.xvg` traces |
| `pyr_p4.xvg`, `phn_p4.xvg` | run 1, ligand to pocket-4 lining, 10001 frames over 100 ns |
| `pyr_p4_rep2.xvg`, `phn_p4_rep2.xvg` | run 2, same measurement |
| `pocket4_replicates.png` | the figure |
| `fig_pocket4_docked.png` | docked pose in pocket 4 |
| `fig_pyrene_migration.png` | **run 1 only** — pyrene's docked and 75 ns positions. Does not represent run 2, where it never moves. |
| `fig_phenanthrene_finalsite.png` | **run 1 only** — phenanthrene's 75 ns site |
| `pyrene_75ns.pdb`, `phenanthrene_75ns.pdb` | run 1 snapshots at 75 ns, protein + ligand |
| `pyrene_75ns_out/`, `phenanthrene_75ns_out/` | fpocket on those snapshots |
| `figures.pml`, `figures_v2.pml` | PyMOL scene definitions |
| `windows/` | MM-GBSA over defined-site windows of run 1, plus `rerun_mmgbsa.sh` |

Reproduce from `md.tpr` + `md.xtc`:

```
./md_analysis.sh jobs/pyrene_run PYR
./md_analysis.sh jobs/pyrene_run/rep2 PYR
python plot_replicates.py pocket4_replicates.png \
  "pyrene|run 1=pyr_p4.xvg" "pyrene|run 2=pyr_p4_rep2.xvg" \
  "phenanthrene|run 1=phn_p4.xvg" "phenanthrene|run 2=phn_p4_rep2.xvg"
```

Pocket-4 lining used for the distance: residues 123, 250, 270, 271, 272, 274, 306 (129 atoms). Contact threshold 0.5 nm.

## MM-GBSA

Run 2, 0–100 ns, 500 frames, ligand in the pocket throughout — **the values to use**:

| | pyrene | phenanthrene |
|---|---|---|
| ΔTOTAL | -28.43 ± 3.73 (SEM 0.17) | -18.71 ± 3.06 (SEM 0.14) |

Run 1 windows, kept in `windows/` for the record and **superseded**:

| window | frames | pyrene | phenanthrene |
|---|---|---|---|
| pocket 4 while occupied | 11–66 / 6–36 | -16.64 ± 5.46 | -17.38 ± 4.09 |
| final site, 50–100 ns | 251–500 | -14.95 ± 1.89 | -19.82 ± 3.03 |

`md_fit.xtc` is 501 frames at 200 ps, so frame *n* is (*n*−1) × 200 ps. The original run-1 analysis used `startframe = 150` (pyrene) and `25` (phenanthrene), i.e. 29.8–99.8 ns and 4.8–99.8 ns — after dissociation in both cases.

## Site detection, run 1 destinations

- pyrene's site — best overlap 2/7 (pocket 15). Not a detected cavity.
- phenanthrene's site — 7/15 with pocket 17, a further 5/15 with pocket 23, in both the starting structure and the 75 ns snapshot.

No cryptic pocket opened. Phenanthrene's run-1 destination spans two separately-detected pockets, so a per-pocket ranking cannot score it as a unit — detection divides the site before the ranking sees it, and neither half ranks well alone (pocket 17 scored 0.317, 8th of 13).

## Caveats

- Two replicates per ligand; a third is running.
- Pocket-4 identification from docking is unaffected by any of this — fpocket geometry, the weight sweep and the contact-based pose assignment are static-structure results.
