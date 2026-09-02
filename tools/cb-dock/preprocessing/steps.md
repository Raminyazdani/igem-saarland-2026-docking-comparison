# Preprocessing — CB-Dock3

**Goal of this step:** state *exactly* what preparation CB-Dock3 needs to turn the shared canonical
inputs into something it can dock, and then do it reproducibly. This is deliberately separated from the
docking step so all six tools' recipes can be compared and, ideally, merged into one shared preprocessing.

## What to produce here
1. A filled [`PREPROCESSING.yaml`](PREPROCESSING.yaml) — the structured manifest (keep the keys identical
   across tools; it is read side-by-side by `scripts/compare_preprocessing/`).
2. This `steps.md` — a short human narrative: what was necessary, what you did, and any judgement calls.
3. [`preprocess.sh`](preprocess.sh) — a script that reproduces the preparation from `input/canonical/`
   into `../inputs/`. If your tool is GUI/web-only, list the exact clicks/settings here instead.

## Narrative (fill this in)
### Receptor
- Source: `input/canonical/targets/PahP/structure.pdb` (primary target PahP).
- Necessary steps for CB-Dock3: _TODO_ (signal peptide? protonation? charges? format?).
- What I did: _TODO_.

### Ligands
- Source: `input/canonical/ligands/ligands.sdf` (shared 3D conformers).
- Necessary steps for CB-Dock3: _TODO_.
- Did you keep the canonical 3D conformers as-is? _TODO_ (preferred for fairness).

### Binding site / box
- Source: `input/canonical/targets/PahP/binding_site.yaml`.
- Mode (defined/blind) and any box handling: _TODO_.

## Fairness reminder
Change as little as possible from the canonical inputs. Where a tool *forces* a change, record it under
`assumptions_and_deviations` in `PREPROCESSING.yaml` with the reason — those deviations are exactly what we
need to reconcile when designing the shared preprocessing.

## What was done for these runs

- `PahP_fixed.pdb` and `PahS_fixed.pdb` were uploaded as the receptor files. Their headers report OpenMM
  8.5.2 and they contain hydrogens, but the original model source and exact preparation command are missing.
- PahP contains 308 residues corresponding to canonical residues 10–317; PahS contains 677 residues
  corresponding to residues 10–686. This does not confirm removal of the annotated signal peptide.
- The canonical ligand SDF was split into seven individual SDF files without changing the molecular records.
- CB-Dock3 detected the binding cavities automatically; no user-defined box was supplied.
- These provenance/trimming points must be resolved before preprocessing can be marked `done`.
