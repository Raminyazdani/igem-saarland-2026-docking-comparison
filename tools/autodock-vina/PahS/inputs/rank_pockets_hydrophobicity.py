import re
import glob

MIN_VOLUME = 150.0
AROMATIC_RESIDUES = {"PHE", "TYR", "TRP", "HIS"}

PAHS = {
    "naphthalene": {"min": 150, "ideal_min": 200, "ideal_max": 300, "max": 400},
    "anthracene": {"min": 170, "ideal_min": 220, "ideal_max": 350, "max": 450},
    "phenanthrene": {"min": 170, "ideal_min": 220, "ideal_max": 350, "max": 450},
    "fluoranthene": {"min": 200, "ideal_min": 280, "ideal_max": 450, "max": 550},
    "pyrene": {"min": 200, "ideal_min": 280, "ideal_max": 450, "max": 550},
    "benzo_a_pyrene": {"min": 280, "ideal_min": 400, "ideal_max": 600, "max": 800}
}

info_file = glob.glob("PahS_fixed_out/*_info.txt")[0]
text = open(info_file).read()
blocks = re.split(r"\nPocket (\d+) :\n", text)

pockets = {}
for i in range(1, len(blocks), 2):
    num = int(blocks[i])
    content = blocks[i + 1]

    def get_value(pattern):
        match=re.search(pattern, content)
        if not match:
            return float("nan")
        return float(match.group(1))
    
    pockets[num] = dict(
        hydrophobicity=get_value(r"Hydrophobicity score:\s*([\-\d.]+)"),
        apolar_sasa=get_value(r"Apolar SASA\s*:\s*([\-\d.]+)"),
        volume=get_value(r"Volume\s*:\s*([\-\d.]+)"),
        druggability=get_value(r"Druggability Score\s*:\s*([\-\d.]+)"),
    )

for num in pockets:
    atm_file = f"PahS_fixed_out/pockets/pocket{num}_atm.pdb"
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

# PAH-specific volume capacity
def volume_score(volume, limits):
    min_v = limits["min"]
    ideal_min = limits["ideal_min"]
    ideal_max = limits["ideal_max"]
    max_v = limits["max"]

    if volume < min_v: return 0.0
    if min_v <= volume < ideal_min:
        return (volume - min_v) / (ideal_min - min_v)

    if ideal_min <= volume <= ideal_max:
        return 1.0

    if ideal_max < volume <= max_v:
        return (max_v - volume) / (max_v - ideal_max)

    return 0.0

for num, p in pockets.items():
    p["pah_scores"] = {}
    hydro = norm(p["hydrophobicity"], h_min, h_max)
    sasa = norm(p["apolar_sasa"], s_min, s_max)
    aromatic = min(p["n_aromatic"] / 3.0, 1.0)

    for pah, limits in PAHS.items():
        vol = volume_score(p["volume"], limits)
        score = (0.3 * vol + 0.3 * hydro + 0.25 * sasa + 0.15 * aromatic)
        p["pah_scores"][pah] = score


for pah in PAHS:
    ranked = sorted(pockets.items(), key=lambda kv: kv[1]["pah_scores"][pah], reverse=True)

    print()
    print("="*70)
    print(f"PAH: {pah}")
    print("="*70)

    print(
        f"{'Pocket':<8}"
        f"{'Score':<10}"
        f"{'Volume':<10}"
        f"{'Hydro':<10}"
        f"{'Apolar':<10}"
        f"{'Aromatic':<10}"
        f"{'Drug':<10}"
    )

    for num, p in ranked:
        print(
            f"{num:<8}"
            f"{p["pah_scores"][pah]:<10.3f}"
            f"{p["volume"]:<10.1f}"
            f"{p["hydrophobicity"]:<10.3f}"
            f"{p["apolar_sasa"]:<10.1f}"
            f"{p["n_aromatic"]:<10}"
            f"{p["druggability"]:<10.3f}"
        )

    top_num, top = ranked[0]
    print()
    print(
        f"Top pocket for {pah}: "
        f"Pocket {top_num}"
    )

    print(
        f"aromatic residues: "
        f"{top["aromatic_residues"]}"
    )

    def parse_coords(path):
        coords = []
        for line in open(path):
            if line.startswith(("ATOM", "HETATM")):
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                coords.append((x, y, z))
        return coords

    spheres = parse_coords(f"PahS_fixed_out/pockets/pocket{top_num}_vert.pqr")
    lining = parse_coords(f"PahS_fixed_out/pockets/pocket{top_num}_atm.pdb")

    cx = sum(p[0] for p in spheres) / len(spheres)
    cy = sum(p[1] for p in spheres) / len(spheres)
    cz = sum(p[2] for p in spheres) / len(spheres)
    xs = [p[0] for p in lining]; ys = [p[1] for p in lining]; zs = [p[2] for p in lining]
    PADDING = 10.0
    size_x, size_y, size_z = (max(xs)-min(xs))+PADDING, (max(ys)-min(ys))+PADDING, (max(zs)-min(zs))+PADDING

    print(f"\n--- Suggested Vina box for pocket {top_num} ---")
    print(f"center_x: {cx:.2f}\ncenter_y: {cy:.2f}\ncenter_z: {cz:.2f}")
    print(f"size_x: {size_x:.1f}\nsize_y: {size_y:.1f}\nsize_z: {size_z:.1f}")





'''
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

spheres = parse_coords(f"PahS_fixed_out/pockets/pocket{top_num}_vert.pqr")
lining = parse_coords(f"PahS_fixed_out/pockets/pocket{top_num}_atm.pdb")

cx = sum(p[0] for p in spheres) / len(spheres)
cy = sum(p[1] for p in spheres) / len(spheres)
cz = sum(p[2] for p in spheres) / len(spheres)
xs = [p[0] for p in lining]; ys = [p[1] for p in lining]; zs = [p[2] for p in lining]
PADDING = 10.0
size_x, size_y, size_z = (max(xs)-min(xs))+PADDING, (max(ys)-min(ys))+PADDING, (max(zs)-min(zs))+PADDING

print(f"\n--- Suggested Vina box for pocket {top_num} ---")
print(f"center_x: {cx:.2f}\ncenter_y: {cy:.2f}\ncenter_z: {cz:.2f}")
print(f"size_x: {size_x:.1f}\nsize_y: {size_y:.1f}\nsize_z: {size_z:.1f}")
'''