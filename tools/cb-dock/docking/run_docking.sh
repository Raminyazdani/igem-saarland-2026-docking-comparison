#!/usr/bin/env bash
# Docking run for CB-Dock3 (tool/cb-dock).
# Consumes prepared inputs from ../inputs/ and writes native output to ../outputs/.
# CB-Dock3 submission is manual since it's a web server; this script records the settings and paths.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
TOOL_DIR="$(dirname "$HERE")"                 # tools/cb-dock
INPUTS="$TOOL_DIR/inputs"
OUTPUTS="$TOOL_DIR/outputs"
CONFIG="$TOOL_DIR/configurations/config.yaml"
mkdir -p "$OUTPUTS"

echo "[cb-dock] docking with config: $CONFIG"
echo "CB-Dock3 is a web server, so submission is manual."
echo "Upload one prepared receptor PDB and one ligand SDF per job."
echo "Use structure-based blind docking with five CurPocket cavities."
echo "After each job, use scripts/download_cb_dock_results.py with its result URL."
echo "Recorded local output directory: $OUTPUTS"

echo "[cb-dock] see DOCKING.md and ../commands.md for the full manual/local workflow"
