# AutoDock Vina — PahS

Branch: `tool/autodock-vina` · Docking by Ana · Documented by Divyashree

Blind docking of the canonical PAH panel into **PahS**. PahP is the primary target and lives one level up in `tools/autodock-vina/`.

## Why blind

`docking_config.yaml` specifies blind mode for PahS, and the pocket prediction supports it: fpocket finds 60 pockets, and ranking them on the hydrophobicity / apolar-SASA / aromatic-count composite gives no robust winner — across all 66 weight combinations pocket 36 ranks first in 28 (42%), pocket 32 in 27 (41%), pocket 58 in 10 (15%) and pocket 20 in 1 (2%). With no pocket surviving the sweep, a defined box would have encoded an arbitrary choice. The search box therefore encloses the whole receptor: center 73.83 / 71.35 / 76.72, size 65 / 70 / 93 Å.

## Two campaigns

A blind search over the whole receptor, and per-pocket focused runs kept in `outputs/` (pocket 36 for six ligands, `_out_p36`; pocket 12 for naphthalene, `_out_p12`). For the five aromatics the two agree to within 0.11 kcal/mol, well inside Vina's resolution, which indicates the blind search converges on pocket 36 unaided. They differ for naphthalene (−6.578 blind vs −5.223 in pocket 12, 1.36 kcal/mol) because its focused run targeted a pocket the blind search did not favour for that ligand — and that difference matters, because only in the blind run does the glucose negative control rank last.

**The blind run is the reported deliverable**, per the blind mode specified for PahS in `docking_config.yaml`. `results/poses/` and `results/DOCKING_RESULT.json` both come from it. The focused runs are retained as a cross-check, not as results.

| ligand | blind | focused |
|---|---|---|
| benzo[a]pyrene | -8.686 | -8.595 |
| phenanthrene | -8.245 | -8.258 |
| fluoranthene | -8.118 | -8.004 |
| anthracene | -7.938 | -7.909 |
| pyrene | -7.864 | -7.863 |
| naphthalene | -6.578 | -5.223 |
| glucose (control) | -6.109 | -5.682 |

## Contents

| Folder | What's in it |
|---|---|
| `preprocessing/` | `preprocess.sh` (Meeko 0.7.1), `PREPROCESSING.yaml`, `steps.md` |
| `inputs/` | canonical inputs converted to PDBQT |
| `configurations/` | `config.yaml` — blind box and Vina parameters |
| `outputs/` | raw Vina output and logs, including `blind_docking/` |
| `results/` | `DOCKING_RESULT.json` and `poses/` |

## Known inconsistency

PahS was prepared with **Meeko 0.7.1**; PahP with **Open Babel 3.1.0**. Not harmonised: PAHs have no rotatable bonds so Meeko's main advantage does not apply, redoing PahP would invalidate the MD built on it, and the PahP MD result does not depend on which preparation route was used. Recorded rather than fixed — see `preprocessing/PREPROCESSING.yaml`.

## Rules

- Read inputs only from `input/canonical/`. Never edit canonical inputs.
- Touch only `tools/autodock-vina/`.
- Compare **ranks**, never raw scores across tools.
