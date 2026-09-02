#!/bin/bash
set -e
cd "$(dirname "$0")/.."

vina --receptor inputs/receptor.pdbqt --ligand inputs/pyrene.pdbqt \
  --center_x 70.83 --center_y 71.96 --center_z 59.18 \
  --size_x 21.3 --size_y 19.6 --size_z 27.3 \
  --exhaustiveness 16 --num_modes 9 --seed 42 \
  --out outputs/PahP__pyrene__autodock-vina__v1.pdbqt \
  > outputs/PahP__pyrene__autodock-vina__v1.log 2>&1

mkdir -p results/poses
cp outputs/PahP__pyrene__autodock-vina__v1.pdbqt results/poses/PahP__pyrene__autodock-vina__v1.pdbqt
