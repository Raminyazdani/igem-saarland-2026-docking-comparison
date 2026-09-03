#!/usr/bin/env bash
# Reproducible preprocessing for Glide (Schrodinger) (tool/glide).
# Reads ONLY the shared canonical inputs and writes prepared files into ../inputs/.
#
# Steps: (1) receptor -> prepared Maestro, (2) ligands -> prepared Maestro,
#        (3) receptor grid from the binding box.
# Verified against Schrodinger Suite 2026-1 (Glide v11.0): flags/keywords come from
# `prepwizard -h`, `ligprep -long_help` and `glide -gridgen-keywords` on that release.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
TOOL_DIR="$(dirname "$HERE")"                 # tools/glide
REPO_ROOT="$(cd "$TOOL_DIR/../.." && pwd)"
CANON="$REPO_ROOT/input/canonical"
INPUTS="$TOOL_DIR/inputs"
OUTPUTS="$TOOL_DIR/outputs"
CONFIG="$TOOL_DIR/configurations/config.yaml"
mkdir -p "$INPUTS" "$OUTPUTS"

: "${SCHRODINGER:?set SCHRODINGER to your Schrodinger installation directory}"
# Windows ships .exe launchers; Linux/macOS do not.
EXE=""; [ -x "$SCHRODINGER/glide" ] || EXE=".exe"

RECEPTOR="$CANON/targets/PahP/structure.pdb"
LIGANDS="$CANON/ligands/ligands.sdf"
BOX="$CANON/targets/PahP/binding_site.yaml"

echo "[glide] receptor : $RECEPTOR"
echo "[glide] ligands  : $LIGANDS"
echo "[glide] box      : $BOX"

# Schrodinger job control refuses to register output files outside the launch directory,
# so jobs are launched from tools/glide/ (inputs/ and outputs/ are both below it) and the
# .log files they drop here are collected into outputs/ when the script exits.
# Job OUTPUT files must be bare filenames too (a relative subdirectory does not exist
# in job control's temp directory), so artifacts are written here and moved to inputs/.
cd "$TOOL_DIR"
trap 'mv -f "$TOOL_DIR"/*.log "$OUTPUTS"/ 2>/dev/null || true' EXIT

# --- 1. RECEPTOR ---------------------------------------------------------------
# Glide's RECEP_FILE must be Maestro format, so preparation and conversion are one step.
# The canonical model already has all heavy atoms and a contiguous chain, so the Prime
# steps (-fillsidechains / -fillloops) are deliberately NOT used; see steps.md.
# -rehtreat: the canonical hydrogens come from OpenMM with non-Schrodinger atom names,
#            which break H-bond assignment, so they are deleted and re-added.
"$SCHRODINGER/utilities/prepwizard$EXE" \
    -rehtreat -disulfides -noepik -propka_pH 7.4 -f OPLS_2005 \
    -JOBNAME glide_prep_receptor -HOST localhost -WAIT \
    "$RECEPTOR" PahP_prepared.maegz
mv -f PahP_prepared.maegz "$INPUTS/"

# --- 2. LIGANDS ----------------------------------------------------------------
# Minimal-change preparation: keep the canonical 3D conformers and stereochemistry,
# change no protonation states. -i 0 = do not neutralize/ionize, -nt = no tautomers,
# -s 1 = one stereoisomer, -g = take chirality from the input 3D geometry.
"$SCHRODINGER/ligprep$EXE" -i 0 -nt -s 1 -g \
    -isd "$LIGANDS" -omae ligands_prepared.maegz \
    -JOBNAME glide_prep_ligands -HOST localhost -WAIT
mv -f ligands_prepared.maegz "$INPUTS/"

# --- 3. RECEPTOR GRID ----------------------------------------------------------
# The grid must come from the shared canonical box so every tool searches the same
# region. Read it out of binding_site.yaml (flat key: value file).
box_val() { grep -E "^$1:" "$BOX" | head -1 | sed -E 's/^[^:]+:[[:space:]]*//; s/[[:space:]]*#.*$//; s/[[:space:]]*$//'; }
CX=$(box_val center_x); CY=$(box_val center_y); CZ=$(box_val center_z)
SX=$(box_val size_x);   SY=$(box_val size_y);   SZ=$(box_val size_z)

# The canonical box is still a PLACEHOLDER (all six values null) and there is no input-v1
# tag. Glide has no blind-docking mode, so rather than stopping, fall back to the PROVISIONAL
# box in configurations/config.yaml - the fpocket Pocket 4 box the AutoDock Vina team proposed
# for the shared binding_site.yaml, so every tool searches one region. Canonical always wins.
cfg_vec() { grep -E "^[[:space:]]+$1:" "$CONFIG" | head -1 | sed -E 's/.*\[//; s/\].*//; s/,/ /g'; }
if [ -z "$CX" ] || [ "$CX" = "null" ]; then
    read -r CX CY CZ <<< "$(cfg_vec center_xyz)"
    read -r SX SY SZ <<< "$(cfg_vec size_xyz)"
    echo "[glide] WARNING: canonical binding box is still a PLACEHOLDER."
    echo "[glide] WARNING: using the PROVISIONAL box from config.yaml: centre $CX $CY $CZ, size $SX $SY $SZ"
    echo "[glide] WARNING: results are NOT on the shared canonical box - rerun after input-v1."
fi
for v in "$CX" "$CY" "$CZ" "$SX" "$SY" "$SZ"; do
    [ -n "$v" ] && [ "$v" != "null" ] || { echo "[glide] STOP: no usable binding box." >&2; exit 2; }
done

# Inner box (bounds the ligand centroid) comes from config.yaml; documented range is 6-14 A.
# Glide requires outer >= inner + longest ligand in EVERY dimension, and the longest canonical
# ligand, benzo[a]pyrene, is 11.46 A. Checked per axis so an anisotropic box cannot slip through.
read -r IX IY IZ <<< "$(cfg_vec inner_xyz)"
: "${IX:=10}"; : "${IY:=$IX}"; : "${IZ:=$IX}"
for pair in "$SX $IX" "$SY $IY" "$SZ $IZ"; do
    awk -v s="${pair% *}" -v i="${pair#* }" 'BEGIN{ if (s < i + 11.46) exit 1 }' || {
        echo "[glide] STOP: outer box ${pair% *} A cannot hold benzo[a]pyrene (11.46 A)" >&2
        echo "[glide] with an inner box of ${pair#* } A (Glide needs outer >= inner + 11.46)." >&2
        exit 2
    }
done

cat > "$OUTPUTS/glide_grid.in" <<EOF
GRIDFILE   PahP_glide_grid.zip
RECEP_FILE inputs/PahP_prepared.maegz
GRID_CENTER $CX, $CY, $CZ
INNERBOX   $IX, $IY, $IZ
OUTERBOX   $SX, $SY, $SZ
FORCEFIELD OPLS_2005
EOF

"$SCHRODINGER/glide$EXE" "$OUTPUTS/glide_grid.in" -OVERWRITE -HOST localhost -WAIT
mv -f PahP_glide_grid.zip "$INPUTS/"

echo "[glide] preprocessing done -> $INPUTS/"
