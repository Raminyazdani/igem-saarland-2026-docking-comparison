#!/usr/bin/env bash
# Reproducible preprocessing for AutoDock Vina, PahS.
# Reads only input/canonical/ and writes prepared PDBQT files into ../inputs/.
# Prepared with Meeko (PahP uses Open Babel - see ../../preprocessing/preprocess.sh
# and the note in PREPROCESSING.yaml).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TOOL_DIR="$(dirname "$HERE")"
REPO_ROOT="$(cd "$TOOL_DIR/../../.." && pwd)"
CANON="$REPO_ROOT/input/canonical"
INPUTS="$TOOL_DIR/inputs"
RECEPTOR="$CANON/targets/PahS/structure.pdb"
LIGANDS="$CANON/ligands/ligands.sdf"
mkdir -p "$INPUTS"
for f in "$RECEPTOR" "$LIGANDS"; do
  [ -f "$f" ] || { echo "missing: $f" >&2; exit 1; }
done
for c in mk_prepare_receptor.py mk_prepare_ligand.py; do
  command -v "$c" >/dev/null || { echo "$c not on PATH (Meeko 0.7.1)" >&2; exit 1; }
done
mk_prepare_receptor.py -i "$RECEPTOR" --write_pdbqt "$INPUTS/receptor.pdbqt"
echo "receptor -> $INPUTS/receptor.pdbqt"
mk_prepare_ligand.py -i "$LIGANDS" --multimol_outdir "$INPUTS/ligands_pdbqt"
echo "ligands  -> $INPUTS/ligands_pdbqt/"
echo "done. PahS was docked blind over the whole receptor; box in ../configurations/config.yaml"
