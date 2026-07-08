#!/usr/bin/env bash
# Reproducible preprocessing for Uni-Mol Docking (tool/uni-mol).
# Reads ONLY the shared canonical inputs and writes prepared files into ../inputs/.
# Replace the TODO commands with your tool's real preparation. Keep it reproducible.
#
# If Uni-Mol Docking is GUI/web-only and cannot be scripted, leave this as documentation and
# record the exact settings/clicks in steps.md instead.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
TOOL_DIR="$(dirname "$HERE")"                 # tools/uni-mol
REPO_ROOT="$(cd "$TOOL_DIR/../.." && pwd)"
CANON="$REPO_ROOT/input/canonical"
INPUTS="$TOOL_DIR/inputs"
mkdir -p "$INPUTS"

RECEPTOR="$CANON/targets/PahP/structure.pdb"
LIGANDS="$CANON/ligands/ligands.sdf"
BOX="$CANON/targets/PahP/binding_site.yaml"

echo "[uni-mol] receptor : $RECEPTOR"
echo "[uni-mol] ligands  : $LIGANDS"
echo "[uni-mol] box      : $BOX"

# --- RECEPTOR prep (TODO: e.g. strip signal peptide, protonate pH 7.4, convert to your format) ---
# example (AutoDock/Meeko):  mk_prepare_receptor.py -i "$RECEPTOR" -o "$INPUTS/receptor.pdbqt"
echo "TODO: prepare receptor -> $INPUTS/receptor.<ext>"

# --- LIGAND prep (TODO: keep canonical 3D conformers; add charges/format as your tool needs) ---
# example:  mk_prepare_ligand.py -i "$LIGANDS" --multimol_outdir "$INPUTS/ligands_pdbqt"
echo "TODO: prepare ligands -> $INPUTS/ligands.<ext>"

echo "[uni-mol] preprocessing done. Now fill PREPROCESSING.yaml and run ../docking/run_docking.sh"
