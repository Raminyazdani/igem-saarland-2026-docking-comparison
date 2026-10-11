# AutoDock Vina — PahS

Branch: `tool/autodock-vina` · Docking by Ana · Documented by Divyashree

Blind docking of the canonical PAH panel into **PahS**. PahP is the primary target and lives one level up in `tools/autodock-vina/`.

## Why blind

`docking_config.yaml` specifies blind mode for PahS, and the pocket prediction supports it: fpocket finds 60 pockets, and ranking them on the hydrophobicity / apolar-SASA / aromatic-count composite gives no robust winner — across all 66 weight combinations pocket 36 ranks first in 28 (42%), pocket 32 in 27 (41%), pocket 58 in 10 (15%) and pocket 20 in 1 (2%). With no pocket surviving the sweep, a defined box would have encoded an arbitrary choice. The search box therefore encloses the whole receptor: center 73.83 / 71.35 / 76.72, size 65 / 70 / 93 Å.

## Contents

| Folder | What's in it |
|---|---|
| `preprocessing/` | `preprocess.sh` (Meeko 0.7.1), `PREPROCESSING.yaml`, `steps.md` |
| `inputs/` | canonical inputs converted to PDBQT |
| `configurations/` | `config.yaml` — blind box and Vina parameters |
| `outputs/` | raw Vina output and logs, including `blind_docking/` |
| `results/` | `DOCKING_RESULT.json` and `poses/` |

## Known inconsistency

PahS was prepared with **Meeko 0.7.1**; PahP with **Open Babel 3.1.0**. Not harmonised: PAHs have no rotatable bonds so Meeko's main advantage does not apply, redoing PahP would invalidate the MD built on it, and the MD shows the ligands leave the docked pocket regardless. Recorded rather than fixed — see `preprocessing/PREPROCESSING.yaml`.

## Rules

- Read inputs only from `input/canonical/`. Never edit canonical inputs.
- Touch only `tools/autodock-vina/`.
- Compare **ranks**, never raw scores across tools.
