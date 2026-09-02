import subprocess
import os

LIGAND_NAME = "naphthalene"
CANONICAL_LIGANDS_SDF = "../../../input/canonical/ligands/ligands.sdf"
RECEPTOR_PDBQT = "../inputs/receptor.pdbqt"

CENTER = (70.83, 71.96, 59.18)
SIZE = (21.3, 19.6, 27.3)
EXHAUSTIVENESS = 16
NUM_MODES = 9
SEED = 42

os.chdir(os.path.dirname(os.path.abspath(__file__)))

ligand_sdf = f"../inputs/{LIGAND_NAME}.sdf"
with open(CANONICAL_LIGANDS_SDF) as f:
    sdf_text = f.read()
molecules = sdf_text.split("$$$$\n")
found = False
for mol in molecules:
    if mol.strip() and LIGAND_NAME.lower() in mol.split("\n")[0].lower():
        with open(ligand_sdf, "w") as out:
            out.write(mol + "$$$$\n")
        found = True
        break
if not found:
    raise SystemExit(f"Could not find '{LIGAND_NAME}' in {CANONICAL_LIGANDS_SDF}")
print(f"Extracted: {ligand_sdf}")

ligand_pdbqt = f"../inputs/{LIGAND_NAME}.pdbqt"
subprocess.run(["obabel", ligand_sdf, "-O", ligand_pdbqt], check=True)
print(f"Prepared: {ligand_pdbqt}")

out_pdbqt = f"../outputs/PahP__{LIGAND_NAME}__autodock-vina__v1.pdbqt"
log_file = f"../outputs/PahP__{LIGAND_NAME}__autodock-vina__v1.log"
cmd = [
    "vina", "--receptor", RECEPTOR_PDBQT, "--ligand", ligand_pdbqt,
    "--center_x", str(CENTER[0]), "--center_y", str(CENTER[1]), "--center_z", str(CENTER[2]),
    "--size_x", str(SIZE[0]), "--size_y", str(SIZE[1]), "--size_z", str(SIZE[2]),
    "--exhaustiveness", str(EXHAUSTIVENESS), "--num_modes", str(NUM_MODES), "--seed", str(SEED),
    "--out", out_pdbqt,
]
print(f"Running: {' '.join(cmd)}")
with open(log_file, "w") as log:
    subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=True)
print(f"Done. Log: {log_file}")

os.makedirs("../results/poses", exist_ok=True)
pose_file = f"../results/poses/PahP__{LIGAND_NAME}__autodock-vina__v1.pdbqt"
subprocess.run(["cp", out_pdbqt, pose_file], check=True)
print(f"Pose copied: {pose_file}")

print("\n--- Top poses ---")
with open(log_file) as f:
    lines = f.readlines()
    start = next(i for i, l in enumerate(lines) if l.strip().startswith("1"))
    for l in lines[start:start+9]:
        print(l.rstrip())
