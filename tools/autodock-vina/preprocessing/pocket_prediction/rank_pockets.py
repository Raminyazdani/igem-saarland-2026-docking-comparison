"""
Rank fpocket output pockets by druggability score (not fpocket's default
'Score', which favors size/geometry over actual drug-binding likelihood),
and compute a Vina-ready docking box (center + size) for a chosen pocket.
"""
import re
import glob

# ---- 1. Parse *_info.txt and rank all pockets by druggability ----
info_file = glob.glob("PahP_fixed_out/*_info.txt")[0]
text = open(info_file).read()
blocks = re.split(r"\nPocket (\d+) :\n", text)

data = []
for i in range(1, len(blocks), 2):
    num = int(blocks[i])
    content = blocks[i + 1]
    score = float(re.search(r"Score\s*:\s*([\-\d.]+)", content).group(1))
    drug = float(re.search(r"Druggability Score\s*:\s*([\-\d.]+)", content).group(1))
    hydro = float(re.search(r"Hydrophobicity score:\s*([\-\d.]+)", content).group(1))
    apolar_sasa = float(re.search(r"Apolar SASA\s*:\s*([\-\d.]+)", content).group(1))
    vol = float(re.search(r"Volume\s*:\s*([\-\d.]+)", content).group(1))
    data.append(dict(pocket=num, fpocket_score=score, druggability=drug,
                      hydrophobicity=hydro, apolar_sasa=apolar_sasa, volume=vol))

data.sort(key=lambda d: -d["druggability"])

print(f"{'Pocket':<8}{'fScore':<10}{'Drug':<10}{'Hydrophob':<12}{'ApolarSASA':<12}{'Volume':<10}")
for d in data:
    print(f"{d['pocket']:<8}{d['fpocket_score']:<10}{d['druggability']:<10}"
          f"{d['hydrophobicity']:<12}{d['apolar_sasa']:<12}{d['volume']:<10}")

top = data[0]["pocket"]
print(f"\nTop pocket by druggability: Pocket {top}")

# ---- 2. List residues lining the chosen pocket (sanity check) ----
atm_file = f"PahP_fixed_out/pockets/pocket{top}_atm.pdb"
residues = set()
for line in open(atm_file):
    if line.startswith("ATOM"):
        resname = line[17:20].strip()
        resnum = line[22:26].strip()
        residues.add((int(resnum), resname))
print(f"\nResidues lining pocket {top}:")
for resnum, resname in sorted(residues):
    print(f"  {resname}{resnum}")

# ---- 3. Compute Vina box (center from alpha spheres, size from lining atoms + padding) ----
def parse_coords(path):
    coords = []
    for line in open(path):
        if line.startswith(("ATOM", "HETATM")):
            x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
            coords.append((x, y, z))
    return coords

spheres = parse_coords(f"PahP_fixed_out/pockets/pocket{top}_vert.pqr")
lining = parse_coords(atm_file)

cx = sum(p[0] for p in spheres) / len(spheres)
cy = sum(p[1] for p in spheres) / len(spheres)
cz = sum(p[2] for p in spheres) / len(spheres)

xs = [p[0] for p in lining]; ys = [p[1] for p in lining]; zs = [p[2] for p in lining]
PADDING = 10.0  # angstrom, added to lining-atom extent on each axis
size_x = (max(xs) - min(xs)) + PADDING
size_y = (max(ys) - min(ys)) + PADDING
size_z = (max(zs) - min(zs)) + PADDING

print(f"\n--- Suggested Vina box for pocket {top} ---")
print(f"center_x: {cx:.2f}\ncenter_y: {cy:.2f}\ncenter_z: {cz:.2f}")
print(f"size_x: {size_x:.1f}\nsize_y: {size_y:.1f}\nsize_z: {size_z:.1f}")
