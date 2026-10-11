import argparse, os, shutil, subprocess, sys
CANON = "../../../input/canonical/ligands/ligands.sdf"
RECEPTOR = "../inputs/receptor.pdbqt"
CENTER = (70.83, 71.96, 59.18)
SIZE = (21.3, 19.6, 27.3)
ap = argparse.ArgumentParser()
ap.add_argument("ligand", help="exact name as it appears in ligands.sdf")
ap.add_argument("--exhaustiveness", type=int, default=16)
ap.add_argument("--num-modes", type=int, default=9)
ap.add_argument("--seed", type=int, default=42)
a = ap.parse_args()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sdf = f"../inputs/{a.ligand}.sdf"
for mol in open(CANON).read().split("$$$$\n"):
    if mol.strip() and mol.split("\n")[0].strip().lower() == a.ligand.lower():
        open(sdf, "w").write(mol + "$$$$\n"); break
else:
    sys.exit(f"{a.ligand} not found in {CANON}")
pdbqt = f"../inputs/{a.ligand}.pdbqt"
subprocess.run(["obabel", sdf, "-O", pdbqt], check=True)
out = f"../outputs/PahP__{a.ligand}__autodock-vina__v1.pdbqt"
log = f"../outputs/PahP__{a.ligand}__autodock-vina__v1.log"
os.makedirs("../outputs", exist_ok=True)
cmd = ["vina", "--receptor", RECEPTOR, "--ligand", pdbqt,
       "--center_x", str(CENTER[0]), "--center_y", str(CENTER[1]), "--center_z", str(CENTER[2]),
       "--size_x", str(SIZE[0]), "--size_y", str(SIZE[1]), "--size_z", str(SIZE[2]),
       "--exhaustiveness", str(a.exhaustiveness), "--num_modes", str(a.num_modes),
       "--seed", str(a.seed), "--out", out]
with open(log, "w") as f:
    subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, check=True)
os.makedirs("../results/poses", exist_ok=True)
shutil.copy(out, f"../results/poses/PahP__{a.ligand}__autodock-vina__v1.pdbqt")
print(f"{a.ligand}: {out}")
for l in open(log):
    if l.split() and l.split()[0].isdigit():
        print(l.rstrip())
