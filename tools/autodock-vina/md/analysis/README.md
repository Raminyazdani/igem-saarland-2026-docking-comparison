# MD stability analysis — PahP / pyrene, phenanthrene

Tests whether the Vina docked pose in pocket 4 is retained during 100 ns of explicit-solvent MD, and recomputes MM-GBSA over windows where each ligand is in one defined site.

## Files

| file | contents |
|---|---|
| `md_analysis.sh` | builds the pocket-4 index group, runs `gmx mindist`, dumps contact lists at 0/10/25/50/75/100 ns |
| `plot_mindist.py` | produces `pocket4_dissociation.png` from the `.xvg` traces |
| `pyr_p4.xvg`, `phn_p4.xvg` | minimum distance, ligand to pocket-4 lining, 10001 frames over 100 ns |
| `pocket4_dissociation.png` | the figure |
| `pyrene_75ns.pdb`, `phenanthrene_75ns.pdb` | snapshots at 75 ns, protein + ligand |
| `pyrene_75ns_out/`, `phenanthrene_75ns_out/` | fpocket run on those snapshots |
| `windows/rerun_mmgbsa.sh` | the four defined-site MM-GBSA reruns |
| `windows/*_gb_p4.{dat,in}` | MM-GBSA over pocket 4 while the ligand is still in it |
| `windows/*_gb_site.{dat,in}` | MM-GBSA over each ligand's final site, 50–100 ns |

Reproduce from `md.tpr` + `md.xtc`:

```
./md_analysis.sh jobs/pyrene_run PYR
./md_analysis.sh jobs/phenanthrene_run PHN
python plot_mindist.py pocket4_dissociation.png pyrene=pyr_p4.xvg phenanthrene=phn_p4.xvg
./windows/rerun_mmgbsa.sh
```

Pocket-4 lining used for the distance: residues 123, 250, 270, 271, 272, 274, 306 (129 atoms). Contact threshold 0.5 nm.

## Results

| | pyrene | phenanthrene |
|---|---|---|
| in contact with pocket 4 | 19.8% of run | 8.0% of run |
| last contact | 23.3 ns | 8.0 ns |
| mean distance, final 50 ns | 1.49 nm | 2.00 nm |
| final site | LEU10, ILE40, THR41, LEU44, SER45, PRO48, GLN51 | ILE136, LEU139, SER140, LEU142, PHE143, ASP194, ILE195, PRO223, ILE225, ILE237, ALA284, LEU289, HID290, PHE291, PRO292 |

Both ligands start in pocket 4 — the 0 ns contact lists reproduce the fpocket lining almost residue for residue — and both leave. Pyrene loosens from ~13 ns with repeated returns before departing at 23.3 ns and settling from ~37 ns; phenanthrene leaves in one step at 8.0 ns. Neither returns. Both settle 1.5–2 nm away, in hydrophobic regions adjacent to pocket 4.

## MM-GBSA over defined-site windows

`md_fit.xtc` is 501 frames at 200 ps, so frame *n* is (*n*−1) × 200 ps.

| window | frames | pyrene | phenanthrene |
|---|---|---|---|
| pocket 4, ligand still bound | 11–66 / 6–36 | −16.64 ± 5.46 | −17.38 ± 4.09 |
| final site | 251–500 (50–100 ns) | −14.95 ± 1.89 | −19.82 ± 3.03 |

**At pocket 4 the two ligands are indistinguishable** — 0.74 kcal/mol apart against a combined SEM of ~1.03, about 0.7σ, and optimistic since consecutive frames are correlated. MM-GBSA cannot rank these ligands at a common site.

**For pyrene, MM-GBSA contradicts the trajectory.** It scores pocket 4 (−16.64) above the site pyrene settled into and held for the remaining 60 ns (−14.95). It omits configurational entropy and treats desolvation crudely, so a buried aromatic pocket scores well on enthalpy while the real free-energy balance sends the ligand elsewhere. For phenanthrene the two agree (−17.38 vs −19.82), which makes pyrene the informative case.

## Consequences for the original MM-GBSA results

The original run used `startframe = 150` (pyrene) and `25` (phenanthrene) on the same trajectory, i.e. **29.8–99.8 ns** and **4.8–99.8 ns**. Both ligands had left pocket 4 by then, so those ΔG describe each ligand's post-migration site, and they describe *different* sites, so they were never comparable to each other. The derived Kd — pyrene ~0.16 nM, phenanthrene ~0.17 pM — are withdrawn.

The per-residue decomposition (`idecomp = 2`) returned zero contribution for every protein residue with the full interaction energy assigned to the ligand; its standard deviations are propagation artifacts (√2 × per-term SD). Discarded.

## Site detection

Matching each final site against the fpocket run on the starting structure, and again on the 75 ns snapshots:

- pyrene's site — best overlap 2/7 (pocket 15). Not a detected cavity.
- phenanthrene's site — 7/15 with pocket 17, a further 5/15 with pocket 23, in both the starting and 75 ns structures.

No cryptic pocket opened during the simulation. Phenanthrene's site spans two separately-detected pockets, so a per-pocket ranking cannot score it as a unit: detection divides the site before the ranking sees it, and neither half ranks well on its own (pocket 17 scored 0.317, 8th of 13).

## Caveats

- Single 100 ns replicate per ligand, no repeats with different seeds. The dissociation is suggestive, not established.
- Residence times are compared between two single runs; no error bars.
- The pocket-4 windows are short (56 and 31 frames), hence the wide SDs.
- Pocket-4 identification from docking is unaffected by any of this — fpocket geometry, the weight sweep and the contact-based pose assignment are all static-structure results.
