import argparse, glob, os, re, sys
AROMATIC = {"PHE", "TYR", "TRP"}
FIELDS = {"hydro": r"Hydrophobicity score:\s*([\-\d.]+)",
          "sasa": r"Apolar SASA\s*:\s*([\-\d.]+)",
          "vol": r"Volume\s*:\s*([\-\d.]+)",
          "drug": r"Druggability Score\s*:\s*([\-\d.]+)"}
def parse_info(path):
    blocks = re.split(r"^Pocket (\d+) :\s*$", open(path).read(), flags=re.M)
    return {int(blocks[i]): {k: float(re.search(p, blocks[i+1]).group(1))
                             for k, p in FIELDS.items()} for i in range(1, len(blocks), 2)}
def residues(path):
    return sorted({(int(l[22:26]), l[17:20].strip()) for l in open(path) if l.startswith("ATOM")})
def coords(path):
    return [(float(l[30:38]), float(l[38:46]), float(l[46:54]))
            for l in open(path) if l.startswith(("ATOM", "HETATM"))]
def norm(vals):
    lo, hi = min(vals), max(vals)
    return [(v - lo) / (hi - lo) if hi > lo else 0.0 for v in vals]
def score(pk, wh, ws, wa, cap=3):
    nums = sorted(pk)
    h, s = norm([pk[n]["hydro"] for n in nums]), norm([pk[n]["sasa"] for n in nums])
    return {n: wh*h[i] + ws*s[i] + wa*min(pk[n]["n_arom"]/cap, 1.0) for i, n in enumerate(nums)}
def sweep(pk, step=0.1):
    grid = [round(i*step, 3) for i in range(int(1/step) + 1)]
    wins, total = {}, 0
    for wh in grid:
        for ws in grid:
            wa = round(1 - wh - ws, 3)
            if wa < 0: continue
            total += 1
            top = max(score(pk, wh, ws, wa).items(), key=lambda kv: kv[1])[0]
            wins[top] = wins.get(top, 0) + 1
    return wins, total
def box(d, n, pad):
    sph, lin = coords(f"{d}/pockets/pocket{n}_vert.pqr"), coords(f"{d}/pockets/pocket{n}_atm.pdb")
    c = tuple(sum(p[i] for p in sph)/len(sph) for i in range(3))
    s = tuple(max(p[i] for p in lin) - min(p[i] for p in lin) + pad for i in range(3))
    return c, s, len(sph), len(lin)
ap = argparse.ArgumentParser()
ap.add_argument("out_dir")
ap.add_argument("--min-volume", type=float, default=250.0)
ap.add_argument("--weights", nargs=3, type=float, default=[0.4, 0.4, 0.2])
ap.add_argument("--padding", type=float, default=10.0,
                help="added to the total span, i.e. half of it on each side")
a = ap.parse_args()
info = glob.glob(f"{a.out_dir}/*_info.txt")
if not info: sys.exit(f"no *_info.txt in {a.out_dir}")
pk = parse_info(info[0])
for n in pk:
    r = residues(f"{a.out_dir}/pockets/pocket{n}_atm.pdb")
    pk[n]["res"], pk[n]["n_arom"] = r, sum(1 for _, x in r if x in AROMATIC)
small = sorted(n for n in pk if pk[n]["vol"] < a.min_volume)
keep = {n: p for n, p in pk.items() if n not in small}
if not keep: sys.exit("all pockets below min volume")
print(f"{len(pk)} pockets; excluded <{a.min_volume:g} A^3: {small or 'none'}")
sc = score(keep, *a.weights)
print(f"weights {a.weights} (hydro/sasa/aromatic); hydro and sasa min-max normalised within this set")
print(f"{'pocket':>7}{'score':>8}{'hydro':>8}{'sasa':>8}{'vol':>9}{'arom':>6}{'drug':>7}")
for n in sorted(keep, key=lambda n: -sc[n]):
    p = keep[n]
    print(f"{n:>7}{sc[n]:>8.3f}{p['hydro']:>8.1f}{p['sasa']:>8.1f}{p['vol']:>9.1f}{p['n_arom']:>6}{p['drug']:>7.3f}")
best = max(sc, key=sc.get)
print(f"top: pocket {best}")
print("lining: " + ", ".join(f"{x}{n}" for n, x in keep[best]["res"]))
print("aromatic: " + ", ".join(f"{x}{n}" for n, x in keep[best]["res"] if x in AROMATIC))
wins, total = sweep(keep)
print(f"weight sweep ({total} combinations, step 0.1):")
for n, c in sorted(wins.items(), key=lambda kv: -kv[1]):
    print(f"  pocket {n}: first in {c}/{total} ({100*c/total:.0f}%)")
c, s, nsph, nlin = box(a.out_dir, best, a.padding)
print(f"box from {nsph} alpha spheres, {nlin} lining atoms, "
      f"{a.padding:g} A padding on the span ({a.padding/2:g} A per side)")
print(f"  center_xyz: [{c[0]:.2f}, {c[1]:.2f}, {c[2]:.2f}]")
print(f"  size_xyz:   [{s[0]:.1f}, {s[1]:.1f}, {s[2]:.1f}]")
