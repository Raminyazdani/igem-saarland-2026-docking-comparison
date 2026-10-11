# MD stability analysis — PahP / pyrene, phenanthrene

Tests whether the Vina docked pose in pocket 4 is retained during 100 ns of explicit-solvent MD.

## Files

| file | contents |
|---|---|
| `md_analysis.sh` | builds the pocket-4 index group, runs `gmx mindist`, dumps contact lists at 0/10/25/50/75/100 ns |
| `plot_mindist.py` | produces `pocket4_dissociation.png` from the `.xvg` traces |
| `pyr_p4.xvg`, `phn_p4.xvg` | minimum distance, ligand to pocket-4 lining, 10001 frames over 100 ns |
| `pocket4_dissociation.png` | the figure |
| `pyrene_75ns.pdb`, `phenanthrene_75ns.pdb` | snapshots at 75 ns, protein + ligand |
| `pyrene_75ns_out/`, `phenanthrene_75ns_out/` | fpocket run on those snapshots |

Reproduce from `md.tpr` + `md.xtc`:

```
./md_analysis.sh jobs/pyrene_run PYR
./md_analysis.sh jobs/phenanthrene_run PHN
python plot_mindist.py pocket4_dissociation.png pyrene=pyr_p4.xvg phenanthrene=phn_p4.xvg
```

Pocket-4 lining used for the distance: residues 123, 250, 270, 271, 272, 274, 306 (129 atoms). Contact threshold 0.5 nm.

## Results

| | pyrene | phenanthrene |
|---|---|---|
| in contact with pocket 4 | 19.8% of run | 8.0% of run |
| last contact | 23.3 ns | 8.0 ns |
| mean distance, final 50 ns | 1.49 nm | 2.00 nm |
| final site | LEU10, ILE40, THR41, LEU44, SER45, PRO48, GLN51 | ILE136, LEU139, SER140, LEU142, PHE143, ASP194, ILE195, PRO223, ILE225, ILE237, ALA284, LEU289, HID290, PHE291, PRO292 |

Both ligands start in pocket 4 — the 0 ns contact lists reproduce the fpocket lining almost residue for residue — and both leave. Pyrene loosens from ~13 ns with repeated returns before departing at 23.3 ns; phenanthrene leaves in one step at 8.0 ns. Neither returns. Both settle 1.5–2 nm away, in hydrophobic regions adjacent to pocket 4.

## Consequences for the MM-GBSA results

`mmpbsa_gb.in` used `startframe = 150, endframe = 500` on a 501-frame, 200 ps/frame trajectory, i.e. **29.8–99.8 ns**. Both ligands had already left pocket 4 by then, so the reported ΔG describes each ligand's post-migration site, and the two ligands are at different sites. The derived Kd is withdrawn, and the Vina/MM-GBSA ranking disagreement is explained: the two methods scored different sites.

The MM-GBSA per-residue decomposition (`idecomp = 2`) returned zero contribution for every protein residue with the full interaction energy assigned to the ligand; its reported standard deviations are propagation artifacts. Discarded.

## Site detection

Matching each final site against the fpocket run on the starting structure, and again on the 75 ns snapshots:

- pyrene's site — best overlap 2/7 (pocket 15). Not a detected cavity.
- phenanthrene's site — 7/15 with pocket 17, a further 5/15 with pocket 23, in both the starting and 75 ns structures.

No cryptic pocket opened during the simulation. Phenanthrene's site spans two separately-detected pockets, so a per-pocket ranking cannot score it as a unit: the detection step divides the site before the ranking sees it, and neither half ranks well on its own (pocket 17 scored 0.317, 8th of 13).

## Caveats

- Single 100 ns replicate per ligand, no repeats with different seeds. The dissociation is suggestive, not established.
- Residence times are compared between two single runs; no error bars.
- Pocket-4 identification from docking is unaffected by this — fpocket geometry, the weight sweep and the contact-based pose assignment are all static-structure results.
