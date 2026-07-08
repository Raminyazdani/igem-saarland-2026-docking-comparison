# Preprocessing — Discovery Studio 2019

**Goal of this step:** state *exactly* what preparation Discovery Studio 2019 needs to turn the shared canonical
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
- Necessary steps for Discovery Studio 2019: _TODO_ (signal peptide? protonation? charges? format?).
- What I did: _TODO_.

### Ligands
- Source: `input/canonical/ligands/ligands.sdf` (shared 3D conformers).
- Necessary steps for Discovery Studio 2019: _TODO_.
- Did you keep the canonical 3D conformers as-is? _TODO_ (preferred for fairness).

### Binding site / box
- Source: `input/canonical/targets/PahP/binding_site.yaml`.
- Mode (defined/blind) and any box handling: _TODO_.

## Fairness reminder
Change as little as possible from the canonical inputs. Where a tool *forces* a change, record it under
`assumptions_and_deviations` in `PREPROCESSING.yaml` with the reason — those deviations are exactly what we
need to reconcile when designing the shared preprocessing.
