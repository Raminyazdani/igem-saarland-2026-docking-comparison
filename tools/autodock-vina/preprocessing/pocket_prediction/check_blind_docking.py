import argparse, glob, re, sys
def coords(path):
    return [(float(l[30:38]), float(l[38:46]), float(l[46:54]))
            for l in open(path) if l.startswith(("ATOM", "HETATM"))]
def poses(path):
    out, atoms, aff = [], [], None
    for l in open(path):
        if l.startswith("MODEL"): atoms, aff = [], None
        elif l.startswith("REMARK VINA RESULT"): aff = float(l.split()[3])
        elif l.startswith(("ATOM", "HETATM")):
            atoms.append((float(l[30:38]), float(l[38:46]), float(l[46:54])))
        elif l.startswith("ENDMDL") and atoms:
            out.append((aff, atoms)); atoms, aff = [], None
    if atoms: out.append((aff, atoms))
    return out
def pockets(d):
    pk = {}
    for f in glob.glob(f"{d}/pockets/pocket*_atm.pdb"):
        n = int(re.search(r"pocket(\d+)_atm", f).group(1))
        sph = coords(f.replace("_atm.pdb", "_vert.pqr"))
        pk[n] = (coords(f), tuple(sum(p[i] for p in sph)/len(sph) for i in range(3)))
    return pk
def contacts(atoms, lining, cut):
    c2 = cut*cut
    return sum(1 for ax, ay, az in atoms for bx, by, bz in lining
               if (ax-bx)**2 + (ay-by)**2 + (az-bz)**2 < c2)
ap = argparse.ArgumentParser()
ap.add_argument("poses")
ap.add_argument("out_dir")
ap.add_argument("--cutoff", type=float, default=4.5)
a = ap.parse_args()
ps, pk = poses(a.poses), pockets(a.out_dir)
if not ps: sys.exit(f"no poses in {a.poses}")
print(f"{len(ps)} poses, {len(pk)} pockets, cutoff {a.cutoff} A")
print(f"{'pose':>5}{'affinity':>10}{'pocket':>8}{'contacts':>10}{'cent.d':>8}{'next':>12}")
hits = {}
for i, (aff, atoms) in enumerate(ps, 1):
    rank = sorted(((n, contacts(atoms, lin, a.cutoff)) for n, (lin, _) in pk.items()),
                  key=lambda kv: -kv[1])
    n, c = rank[0]
    if not c:
        print(f"{i:>5}{aff:>10.2f}{'none':>8}{0:>10}")
        hits.setdefault(None, []).append(aff); continue
    cen = tuple(sum(p[j] for p in atoms)/len(atoms) for j in range(3))
    d = sum((cen[j] - pk[n][1][j])**2 for j in range(3))**0.5
    nxt = f"{rank[1][0]} ({rank[1][1]})" if len(rank) > 1 and rank[1][1] else "-"
    print(f"{i:>5}{aff:>10.2f}{n:>8}{c:>10}{d:>8.2f}{nxt:>12}")
    hits.setdefault(n, []).append(aff)
for n, affs in sorted(hits.items(), key=lambda kv: (kv[0] is None, -len(kv[1]))):
    print(f"{'unassigned' if n is None else f'pocket {n}'}: {len(affs)} poses, best {min(affs):.2f}")
