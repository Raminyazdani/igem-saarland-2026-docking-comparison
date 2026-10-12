#!/bin/bash
# Docks every canonical ligand into the Pocket 4 box by calling dock_ligand.py,
# which reads the box and sampling settings from ../configurations/config.yaml.
set -e
cd "$(dirname "$0")"
METADATA="../../../input/canonical/ligands/ligand_metadata.csv"
[ -f "$METADATA" ] || { echo "missing: $METADATA" >&2; exit 1; }
for lig in $(awk -F, 'NR>1 && $1 !~ /^#/ && $1 != "" {print $1}' "$METADATA"); do
  echo "=== $lig"
  python3 dock_ligand.py "$lig"
done
