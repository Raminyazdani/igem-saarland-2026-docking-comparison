# Preprocessing — AutoDock Vina (PahS)

Docking by Ana; documented by Divyashree. PahP is handled in `../../preprocessing/`.

## Receptor

- Source: `input/canonical/targets/PahS/structure.pdb`.
- Needed for Vina: hydrogens, partial charges, and conversion to rigid PDBQT. Nothing else — the canonical structure has no waters, cofactors or ions to strip.
- Done: hydrogens added with PDBFixer at pH 7.4, Gasteiger charges, rigid PDBQT via Meeko 0.7.1. Full sequence used; no signal peptide removed; no flexible residues.

## Ligands

- Source: `input/canonical/ligands/ligands.sdf`.
- Needed for Vina: PDBQT with charges and rotatable-bond definitions.
- Done: canonical 3D conformers used as-is — no re-embedding, no tautomer enumeration. Gasteiger charges, PDBQT via Meeko 0.7.1. PAHs have no rotatable bonds, so the torsion tree is trivial in every case.

## Binding site / box

- Source: `input/canonical/targets/PahS/binding_site.yaml`, which was still a placeholder at the time of this work.
- Mode: **blind**, as mandated for PahS by `docking_config.yaml`. Whole-receptor box, center [73.8275, 71.3505, 76.722], size [65, 70, 93] Å.
- This is independently justified by pocket prediction. fpocket found 60 pockets on PahS; ranked on the same hydrophobicity / apolar-SASA / aromatic-count composite used for PahP, no pocket is robust — across all 66 weight combinations pocket 36 ranks first in 42%, pocket 32 in 41% and pocket 58 in 15%. With no pocket surviving the sweep, a defined box would have encoded an arbitrary choice.

## Judgement calls and deviations

- **Prep software differs from PahP.** PahS ligands and receptor were prepared with Meeko 0.7.1; PahP used Open Babel 3.1.0. Not harmonised: PAHs have no rotatable bonds so Meeko's main advantage does not apply, and redoing PahP would invalidate the MD run built on it. Recorded rather than fixed.
- **Blind rather than defined box**, per the reasoning above.
- `configurations/config.yaml` previously carried a defined box that was never used; corrected to match the blind run recorded in `results/DOCKING_RESULT.json`.

## Fairness reminder

Change as little as possible from the canonical inputs. Where a tool *forces* a change, record it under `assumptions_and_deviations` in `PREPROCESSING.yaml` with the reason — those deviations are exactly what we need to reconcile when designing the shared preprocessing.
