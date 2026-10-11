import argparse, os, shutil, subprocess, sys, yaml
CANON = "../../../input/canonical/ligands/ligands.sdf"
RECEPTOR = "../inputs/receptor.pdbqt"
CONFIG = "../configurations/config.yaml"
ap = argparse.ArgumentParser()
ap.add_argument("ligand", help="exact name as it appears in ligands.sdf")
ap.add_argument("--config", default=CONFIG)
a = ap.parse_args()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
cfg = yaml.safe_load(open(a.config))
box = cfg["box"]
if box.get("mode") != "defined" or not box.get("center_xyz") or not box.get("size_xyz"):
    sys.exit(f"{a.config}: box.mode must be 'defined' with center_xyz and size_xyz set")
cx, cy, cz = box["center_xyz"]
sx, sy, sz = box["size_xyz"]
exh, nmodes, seed = cfg["exhaustiveness"], cfg["num_poses"], cfg["random_seed"]
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
       "--center_x", str(cx), "--center_y", str(cy), "--center_z", str(cz),
       "--size_x", str(sx), "--size_y", str(sy), "--size_z", str(sz),
       "--exhaustiveness", str(exh), "--num_modes", str(nmodes),
       "--seed", str(seed), "--out", out]
with open(log, "w") as f:
    subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, check=True)
os.makedirs("../results/poses", exist_ok=True)
shutil.copy(out, f"../results/poses/PahP__{a.ligand}__autodock-vina__v1.pdbqt")
print(f"{a.ligand}: box {cx}/{cy}/{cz} size {sx}/{sy}/{sz} exh {exh} seed {seed}")
for l in open(log):
    if l.split() and l.split()[0].isdigit():
        print(l.rstrip())
