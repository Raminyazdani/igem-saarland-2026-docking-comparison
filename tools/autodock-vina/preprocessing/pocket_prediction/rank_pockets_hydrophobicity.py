import re
import glob

MIN_VOLUME = 250.0
AROMATIC_RESIDUES = {"PHE", "TYR", "TRP"}

info_file = glob.glob("PahP_fixed_out/*_info.txt")[0]
text = open(info_file).read()
blocks = re.split(r"\nPocket (\d+) :\n", text)

pockets = {}
for i in range(1, len(blocks), 2):
    num = int(blocks[i])
    content = blocks[i + 1]
    pockets[num] = dict(
        hydrophobicity=float(re.search(r"Hydrophobicity score:\s*([\-\d.]+)", content).group(1)),
        apolar_sasa=float(re.search(r"Apolar SASA\s*:\s*([\-\d.]+)", content).group(1)),
        volume=float(re.search(r"Volume\s*:\s*([\-\d.]+)", content).group(1)),
        druggability=float(re.search(r"Druggability Score\s*:\s*([\-\d.]+)", content).group(1)),
    )

for num in pockets:
    atm_file = f"PahP_fixed_out/pockets/pocket{num}_atm.pdb"
    residues = set()
    for line in open(atm_file):
        if line.startswith("ATOM"):
            resname = line[17:20].strip()
            resnum = line[22:26].strip()
            residues.add((int(resnum), resname))
    aromatic = [r for r in residues if r[1] in AROMATIC_RESIDUES]
    pockets[num]["n_residues"] = len(residues)
    pockets[num]["n_aromatic"] = len(aromatic)
    pockets[num]["aromatic_residues"] = sorted(aromatic)

hydro_vals = [p["hydrophobicity"] for p in pockets.values()]
sasa_vals = [p["apolar_sasa"] for p in pockets.values()]
h_min, h_max = min(hydro_vals), max(hydro_vals)
s_min, s_max = min(sasa_vals), max(sasa_vals)

def norm(v, lo, hi):
    return (v - lo) / (hi - lo) if hi > lo else 0.0

for num, p in pockets.items():
    if p["volume"] < MIN_VOLUME:
        p["composite_score"] = -999
    else:
        p["composite_score"] = (
            0.4 * norm(p["hydrophobicity"], h_min, h_max)
            + 0.4 * norm(p["apolar_sasa"], s_min, s_max)
            + 0.2 * min(p["n_aromatic"] / 3.0, 1.0)
        )

ranked = sorted(pockets.items(), key=lambda kv: -kv[1]["composite_score"])

print(f"{'Pocket':<8}{'Composite':<11}{'Hydrophob':<11}{'ApolarSASA':<12}{'Volume':<9}{'#Aromatic':<11}{'Drug(fyi)':<10}")
for num, p in ranked:
    flag = " (too small)" if p["composite_score"] == -999 else ""
    print(f"{num:<8}{p['composite_score']:<11.3f}{p['hydrophobicity']:<11}{p['apolar_sasa']:<12}"
          f"{p['volume']:<9}{p['n_aromatic']:<11}{p['druggability']:<10}{flag}")

top_num, top = ranked[0]
print(f"\nTop pocket by hydrophobicity/aromaticity composite: Pocket {top_num}")
print(f"Aromatic residues lining it: {top['aromatic_residues']}")

def parse_coords(path):
    coords = []
    for line in open(path):
        if line.startswith(("ATOM", "HETATM")):
            x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
            coords.append((x, y, z))
    return coords

spheres = parse_coords(f"PahP_fixed_out/pockets/pocket{top_num}_vert.pqr")
lining = parse_coords(f"PahP_fixed_out/pockets/pocket{top_num}_atm.pdb")

cx = sum(p[0] for p in spheres) / len(spheres)
cy = sum(p[1] for p in spheres) / len(spheres)
cz = sum(p[2] for p in spheres) / len(spheres)
xs = [p[0] for p in lining]; ys = [p[1] for p in lining]; zs = [p[2] for p in lining]
PADDING = 10.0
size_x, size_y, size_z = (max(xs)-min(xs))+PADDING, (max(ys)-min(ys))+PADDING, (max(zs)-min(zs))+PADDING

print(f"\n--- Suggested Vina box for pocket {top_num} ---")
print(f"center_x: {cx:.2f}\ncenter_y: {cy:.2f}\ncenter_z: {cz:.2f}")
print(f"size_x: {size_x:.1f}\nsize_y: {size_y:.1f}\nsize_z: {size_z:.1f}")
