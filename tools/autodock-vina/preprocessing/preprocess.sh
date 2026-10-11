#!/usr/bin/env bash
# Reproducible preprocessing for AutoDock Vina, PahP.
# Reads only input/canonical/ and writes prepared PDBQT files into ../inputs/.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TOOL_DIR="$(dirname "$HERE")"
REPO_ROOT="$(cd "$TOOL_DIR/../.." && pwd)"
CANON="$REPO_ROOT/input/canonical"
INPUTS="$TOOL_DIR/inputs"
RECEPTOR="$CANON/targets/PahP/structure.pdb"
LIGANDS="$CANON/ligands/ligands.sdf"
METADATA="$CANON/ligands/ligand_metadata.csv"
mkdir -p "$INPUTS"
for f in "$RECEPTOR" "$LIGANDS" "$METADATA"; do
  [ -f "$f" ] || { echo "missing: $f" >&2; exit 1; }
done
command -v obabel >/dev/null || { echo "obabel not on PATH (conda activate docking)" >&2; exit 1; }
# receptor: canonical structure used as-is (already protonated, chain A, no waters/hetero),
# converted to rigid PDBQT with Gasteiger charges
cp "$RECEPTOR" "$INPUTS/PahP_fixed.pdb"
(cd "$INPUTS" && obabel PahP_fixed.pdb -O receptor.pdbqt -xr)
echo "receptor -> $INPUTS/receptor.pdbqt"
# ligands: canonical 3D conformers split by title, each converted to PDBQT
LIGAND_NAMES=$(awk -F, 'NR>1 && $1 !~ /^#/ && $1 != "" {print $1}' "$METADATA")
for lig in $LIGAND_NAMES; do
  python3 - "$LIGANDS" "$lig" "$INPUTS/$lig.sdf" <<'PY'
import sys
src, name, dest = sys.argv[1], sys.argv[2], sys.argv[3]
for mol in open(src).read().split("$$$$\n"):
    if mol.strip() and mol.split("\n")[0].strip().lower() == name.lower():
        open(dest, "w").write(mol + "$$$$\n"); sys.exit(0)
sys.exit(f"{name} not found in {src}")
PY
  (cd "$INPUTS" && obabel "$lig.sdf" -O "$lig.pdbqt")
  echo "ligand   -> $INPUTS/$lig.pdbqt"
done
echo "done. box parameters are in ../configurations/config.yaml; dock with ../docking/dock_ligand.py"
