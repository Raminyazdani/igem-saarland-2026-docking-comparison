import subprocess
import re
import os
import glob

RECEPTOR_PDB = "PahP_fixed.pdb"
CANONICAL_LIGANDS_SDF = "../../../input/canonical/ligands/ligands.sdf"
CANONICAL_LIGAND_METADATA = "../../../input/canonical/ligands/ligand_metadata.csv"
PYRENE_SEARCH_TERM = "pyrene"
EXHAUSTIVENESS = 32
NUM_MODES = 20
WORKDIR = "blind_docking"

os.makedirs(WORKDIR, exist_ok=True)

receptor_pdbqt = f"{WORKDIR}/receptor.pdbqt"
subprocess.run(["obabel", RECEPTOR_PDB, "-O", receptor_pdbqt, "-xr"], check=True)
print(f"Receptor prepared: {receptor_pdbqt}")

pyrene_sdf = f"{WORKDIR}/pyrene.sdf"
found = False
if os.path.exists(CANONICAL_LIGAND_METADATA):
    for line in open(CANONICAL_LIGAND_METADATA):
        if PYRENE_SEARCH_TERM.lower() in line.lower():
            print(f"Found in metadata: {line.strip()}")

with open(CANONICAL_LIGANDS_SDF) as f:
    sdf_text = f.read()
molecules = sdf_text.split("$$$$\n")
for mol in molecules:
    if mol.strip() and PYRENE_SEARCH_TERM.lower() in mol.split("\n")[0].lower():
        with open(pyrene_sdf, "w") as out:
            out.write(mol + "$$$$\n")
        found = True
        break

if not found:
    raise SystemExit(
        f"Could not auto-find '{PYRENE_SEARCH_TERM}' in {CANONICAL_LIGANDS_SDF}.\n"
        f"Check ligand_metadata.csv for pyrene's exact name/ID and edit PYRENE_SEARCH_TERM above."
    )
print(f"Pyrene extracted: {pyrene_sdf}")

ligand_pdbqt = f"{WORKDIR}/pyrene.pdbqt"
subprocess.run(["obabel", pyrene_sdf, "-O", ligand_pdbqt], check=True)
print(f"Ligand prepared: {ligand_pdbqt}")

xs, ys, zs = [], [], []
for line in open(RECEPTOR_PDB):
    if line.startswith(("ATOM", "HETATM")):
        xs.append(float(line[30:38]))
        ys.append(float(line[38:46]))
        zs.append(float(line[46:54]))

PADDING = 6.0
cx, cy, cz = (max(xs)+min(xs))/2, (max(ys)+min(ys))/2, (max(zs)+min(zs))/2
sx, sy, sz = (max(xs)-min(xs))+PADDING, (max(ys)-min(ys))+PADDING, (max(zs)-min(zs))+PADDING
print(f"\nBlind box: center=({cx:.1f},{cy:.1f},{cz:.1f}) size=({sx:.1f},{sy:.1f},{sz:.1f})")

output_pdbqt = f"{WORKDIR}/pyrene_blind_out.pdbqt"
log_file = f"{WORKDIR}/vina_blind.log"
cmd = [
    "vina", "--receptor", receptor_pdbqt, "--ligand", ligand_pdbqt,
    "--center_x", str(cx), "--center_y", str(cy), "--center_z", str(cz),
    "--size_x", str(sx), "--size_y", str(sy), "--size_z", str(sz),
    "--exhaustiveness", str(EXHAUSTIVENESS), "--num_modes", str(NUM_MODES),
    "--out", output_pdbqt,
]
print(f"\nRunning: {' '.join(cmd)}")
with open(log_file, "w") as log:
    subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=True)
print(f"Vina finished. Log: {log_file}")

poses = []
current_atoms = []
affinity = None
for line in open(output_pdbqt):
    if line.startswith("REMARK VINA RESULT"):
        affinity = float(line.split()[3])
    elif line.startswith(("ATOM", "HETATM")):
        current_atoms.append((float(line[30:38]), float(line[38:46]), float(line[46:54])))
    elif line.startswith("ENDMDL"):
        if current_atoms:
            px = sum(a[0] for a in current_atoms) / len(current_atoms)
            py = sum(a[1] for a in current_atoms) / len(current_atoms)
            pz = sum(a[2] for a in current_atoms) / len(current_atoms)
            poses.append((affinity, px, py, pz))
        current_atoms = []

def parse_coords(path):
    coords = []
    for line in open(path):
        if line.startswith(("ATOM", "HETATM")):
            coords.append((float(line[30:38]), float(line[38:46]), float(line[46:54])))
    return coords

pocket_centers = {}
for vert_file in glob.glob("PahP_fixed_out/pockets/pocket*_vert.pqr"):
    num = int(re.search(r"pocket(\d+)_vert", vert_file).group(1))
    coords = parse_coords(vert_file)
    pocket_centers[num] = (
        sum(c[0] for c in coords) / len(coords),
        sum(c[1] for c in coords) / len(coords),
        sum(c[2] for c in coords) / len(coords),
    )

def dist(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2) ** 0.5

print(f"\n{'Pose':<6}{'Affinity':<11}{'Closest pocket':<16}{'Distance (A)':<14}")
for i, (aff, px, py, pz) in enumerate(poses, start=1):
    closest = min(pocket_centers.items(), key=lambda kv: dist((px, py, pz), kv[1]))
    d = dist((px, py, pz), closest[1])
    flag = "  <-- near Pocket 4!" if closest[0] == 4 and d < 8 else ""
    print(f"{i:<6}{aff:<11}{closest[0]:<16}{d:<14.2f}{flag}")

print("\nIf several of the best-affinity poses (top rows, most negative kcal/mol) "
      "land close to Pocket 4, that's independent support for it as the real binding site.")
