#!/usr/bin/env bash
# Reproducible preprocessing for CB-Dock3 (tool/cb-dock).
# Reads ONLY the shared canonical inputs and writes prepared files into ../inputs/.
# Recreates the ligand split and checks the existing prepared receptor files.
#
# Receptor regeneration remains blocked until its source and preparation command are recorded.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
TOOL_DIR="$(dirname "$HERE")"                 # tools/cb-dock
REPO_ROOT="$(cd "$TOOL_DIR/../.." && pwd)"
CANON="$REPO_ROOT/input/canonical"
INPUTS="$TOOL_DIR/inputs"
mkdir -p "$INPUTS"

RECEPTOR="$CANON/targets/PahP/structure.pdb"
LIGANDS="$CANON/ligands/ligands.sdf"
BOX="$CANON/targets/PahP/binding_site.yaml"

echo "[cb-dock] receptor : $RECEPTOR"
echo "[cb-dock] ligands  : $LIGANDS"
echo "[cb-dock] box      : $BOX"

# The prepared receptor models already used for the web runs live here. Their
# original model source and exact OpenMM preparation command still need to be
# supplied before this step is fully reproducible.
for prepared_receptor in "$INPUTS/protein/PahP_fixed.pdb" "$INPUTS/protein/PahS_fixed.pdb"; do
  test -s "$prepared_receptor" || {
    echo "Missing prepared receptor: $prepared_receptor" >&2
    exit 1
  }
done
echo "[cb-dock] prepared receptor files found (provenance still pending)"

# Split the canonical multi-record SDF without changing any molecular record.
python - "$LIGANDS" "$INPUTS/ligands" <<'PY'
from pathlib import Path
import sys

source = Path(sys.argv[1])
output_dir = Path(sys.argv[2])
output_dir.mkdir(parents=True, exist_ok=True)

records = [record.strip() for record in source.read_text().split("$$$$") if record.strip()]
for record in records:
    ligand_id = record.splitlines()[0].strip()
    (output_dir / f"{ligand_id}.sdf").write_text(record + "\n$$$$\n")

print(f"[cb-dock] wrote {len(records)} unchanged ligand records to {output_dir}")
PY

echo "[cb-dock] ligand preprocessing done; receptor provenance remains a blocker"
