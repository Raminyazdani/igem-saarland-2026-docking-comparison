#!/usr/bin/env bash
# Docking run for AutoDock Vina (tool/autodock-vina).
# Consumes prepared inputs from ../inputs/ and writes native output to ../outputs/.
# Replace the TODO commands with your tool's real docking call.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
TOOL_DIR="$(dirname "$HERE")"                 # tools/autodock-vina
INPUTS="$TOOL_DIR/inputs"
OUTPUTS="$TOOL_DIR/outputs"
CONFIG="$TOOL_DIR/configurations/config.yaml"
mkdir -p "$OUTPUTS"

echo "[autodock-vina] docking with config: $CONFIG"
# example (AutoDock Vina):
#   vina --receptor "$INPUTS/receptor.pdbqt" --ligand "$INPUTS/lig.pdbqt" \
#        --config "$CONFIG" --out "$OUTPUTS/lig_out.pdbqt" --log "$OUTPUTS/lig.log"
echo "TODO: run AutoDock Vina for each ligand -> $OUTPUTS/"

echo "[autodock-vina] docking done. Next: pick poses -> ../results/poses/, fill ../results/DOCKING_RESULT.json, validate."
