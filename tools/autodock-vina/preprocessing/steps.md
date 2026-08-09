# Preprocessing steps — AutoDock Vina (PahP + pyrene)

## Receptor
Used the canonical `PahP/structure.pdb` as-is (already protonated, hydrogens present,
chain A assigned, no waters/hetero groups present). Converted to PDBQT with Open Babel
3.1.0 (`obabel structure.pdb -O receptor.pdbqt -xr`), which assigns Gasteiger charges
and sets up the rigid receptor.

## Ligand
Extracted pyrene from the canonical `ligands.sdf` (matched by name in
`ligand_metadata.csv`), used the shared 3D conformer as-is, converted to PDBQT with
Open Babel 3.1.0.

## Binding site
The canonical `binding_site.yaml` was still an unfilled placeholder at the time of this
work (structure had just been added; box definition was marked BLOCKED/TODO). Ran
fpocket 4.2.2 on the receptor to identify candidate pockets.

fpocket's default ranking (its general "Score") favored a pocket that was mildly polar
and low in druggability. Since druggability is calibrated for oral-drug-likeness and
this project is a PAH water-pollution biosensor, not a drug-discovery target, re-ranked
all 17 candidate pockets using a composite of hydrophobicity score, apolar SASA, and
count of aromatic lining residues (PHE/TYR/TRP — relevant for pi-stacking with a flat
PAH ring system like pyrene), filtering out pockets too small to fit pyrene (<250 A^3).

Pocket 4 was the clear winner on this composite (0.896, next-best 0.674), lined by
4 aromatic residues (PHE123, TYR271, TYR274, PHE306) — the only candidate pocket with
more than one aromatic residue.

## Independent validation
Cross-checked by blind-docking pyrene against the whole receptor (no pocket bias, Vina
searching the entire protein, exhaustiveness 32). The 10 best-affinity poses (-7.98 to
-6.65 kcal/mol) all landed within 1.3-2.4 A of the Pocket 4 center — Vina's own energy
scoring independently converged on the same site.

## Resulting box
center: [70.83, 71.96, 59.18], size: [21.3, 19.6, 27.3] (angstrom)

Proposing this as the shared `binding_site.yaml` value for team review (Ana/Elnaz),
since the fairness rule requires an identical box across all tools.

## Scope of this commit
PahP + pyrene only. PahS/naphthalene is Ana's assignment and is not included here.
