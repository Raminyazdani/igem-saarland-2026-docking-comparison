#!/usr/bin/env bash
# Docking run for Glide (Schrodinger) (tool/glide).
# Consumes prepared inputs from ../inputs/ and writes native output to ../outputs/.
# Keywords verified against Schrodinger Suite 2026-1 (Glide v11.0) via `glide -docking-keywords`.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
TOOL_DIR="$(dirname "$HERE")"                 # tools/glide
INPUTS="$TOOL_DIR/inputs"
OUTPUTS="$TOOL_DIR/outputs"
CONFIG="$TOOL_DIR/configurations/config.yaml"
mkdir -p "$OUTPUTS"

: "${SCHRODINGER:?set SCHRODINGER to your Schrodinger installation directory}"
EXE=""; [ -x "$SCHRODINGER/glide" ] || EXE=".exe"

GRID="$INPUTS/PahP_glide_grid.zip"
LIGS="$INPUTS/ligands_prepared.maegz"
for f in "$GRID" "$LIGS"; do
    [ -s "$f" ] || { echo "[glide] missing $f - run preprocessing/preprocess.sh first" >&2; exit 2; }
done

echo "[glide] docking with config: $CONFIG"

# Same launch-directory rule as preprocessing: launch from tools/glide/ and collect logs.
cd "$TOOL_DIR"
trap 'mv -f "$TOOL_DIR"/*.log "$OUTPUTS"/ 2>/dev/null || true' EXIT

# Glide exposes no random seed (confirmed: no seed keyword in `glide -docking-keywords`).
# CANONICALIZE is the documented substitute - it discards the input coordinates and
# rebuilds each ligand from connectivity, removing the run's dependence on input geometry.
# EPIK_PENALTIES is off because Epik was not run, so docking score == GlideScore.
cat > "$OUTPUTS/glide_dock.in" <<EOF
GRIDFILE        inputs/PahP_glide_grid.zip
LIGANDFILE      inputs/ligands_prepared.maegz
PRECISION       SP
DOCKING_METHOD  confgen
POSES_PER_LIG   5
POSTDOCK        True
POSTDOCK_NPOSE  5
POSTDOCKSTRAIN  False
CANONICALIZE    True
EPIK_PENALTIES  False
FORCEFIELD      OPLS_2005
POSE_OUTTYPE    ligandlib_sd
COMPRESS_POSES  False
WRITE_CSV       True
REPORT_CPU_TIME True
KEEPSKIPPED     True
EOF

# -HOST localhost (a single subjob) keeps every ligand's result in one output set.
"$SCHRODINGER/glide$EXE" "$OUTPUTS/glide_dock.in" -OVERWRITE -HOST localhost -WAIT

# Job control returns output files to the launch directory; keep them with the other
# native output in outputs/ so collect_results.py finds them.
mv -f glide_dock*.sdf glide_dock*.csv "$OUTPUTS/" 2>/dev/null || true

echo "[glide] docking done. Collecting scores and poses..."
python "$HERE/collect_results.py"
