"""
Model 3: competition between PAHs for PahP
iGEM Saarland 2026

Our MM-GBSA Kd values (sub-nM to sub-pM) are too tight to use directly here:
they saturate the receptor in every scenario and the model becomes degenerate.
Absolute Kd are therefore sampled from a plausible range that respects a ranking.

The ranking used is Vina's. MM-GBSA over replicate 2, where both ligands stayed
in pocket 4 for the whole run, gives pyrene -28.43 and phenanthrene -18.71, which
reproduces the Vina order, so the two methods now agree. The alternative ranking
kept below is the withdrawn replicate-1 one, computed on frames from after each
ligand had left the pocket. It is retained only to show what that error would have
changed. See md/analysis/README.md.

Output: model3_competition.png
"""
import numpy as np
import matplotlib.pyplot as plt
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))  # write figures next to the script

rng = np.random.default_rng(42)

# two orders are tested. the first is the withdrawn replicate-1 order,
# computed on post-dissociation frames; it is kept only to show what
# trusting it would have changed.
RANKING_REP1_WITHDRAWN = ["phenanthrene", "pyrene", "fluoranthene", "anthracene", "naphthalene"]
# fluoranthene -8.095 and pyrene -8.021 differ by less than Vina resolves; order as scored
RANKING_VINA = ["fluoranthene", "pyrene", "phenanthrene", "anthracene", "naphthalene"]

# illustrative Kd set, nM - ordered to match whichever ranking is used
KD_LADDER = [100, 300, 500, 1500, 5000]
KD_GLUCOSE = 1e6

CONC = {"pyrene": 20, "phenanthrene": 50, "fluoranthene": 20,
        "anthracene": 10, "naphthalene": 500, "glucose": 1000}

def build_kd(ranking, ladder):
    kd = dict(zip(ranking, ladder))
    kd["glucose"] = KD_GLUCOSE
    return kd

def occupancy(kd, conc):
    terms = {l: conc.get(l, 0.0) / kd[l] for l in kd}
    denom = 1.0 + sum(terms.values())
    return {l: t / denom for l, t in terms.items()}

ligands = RANKING_REP1_WITHDRAWN + ["glucose"]

print("Scenario: polluted site. Concentrations (nM):")
for l, c in CONC.items():
    print(f"  {l:<15}{c:>8g}")

print("\nOccupancy under each ranking:\n")
for name, ranking in [("replicate-1 order (withdrawn)", RANKING_REP1_WITHDRAWN), ("Vina order", RANKING_VINA)]:
    kd = build_kd(ranking, KD_LADDER)
    th = occupancy(kd, CONC)
    total = sum(th.values())
    print(f"  {name}  (total occupancy {total:.3f})")
    for l in sorted(th, key=th.get, reverse=True):
        if th[l] > 1e-4:
            print(f"    {l:<15}{th[l]:>8.4f}")
    print()

fig, ax = plt.subplots(1, 3, figsize=(15, 4.5))

labels = ["replicate-1 order\n(withdrawn)", "Vina order\n(= replicate-2 MM-GBSA)"]
bottom = np.zeros(2)
for lig in ligands:
    vals = [occupancy(build_kd(r, KD_LADDER), CONC).get(lig, 0)
            for r in (RANKING_REP1_WITHDRAWN, RANKING_VINA)]
    ax[0].bar(labels, vals, bottom=bottom, label=lig)
    bottom += np.array(vals)
ax[0].set(ylabel="receptor occupancy",
          title="(a) What the withdrawn ranking would have changed")
ax[0].legend(fontsize=7)

kd = build_kd(RANKING_VINA, KD_LADDER)
scan = np.logspace(-1, 5, 200)
for label, background in [("pyrene alone", {}), ("+ mixture background", CONC)]:
    frac = []
    for c in scan:
        mix = dict(background)
        mix["pyrene"] = c
        frac.append(occupancy(kd, mix)["pyrene"])
    ax[1].semilogx(scan, frac, label=label)
ax[1].set(xlabel="[pyrene] (nM)", ylabel="fraction bound to pyrene",
          title="(b) Competitors shift the curve right")
ax[1].legend(fontsize=8)
ax[1].grid(alpha=0.3)

N = 5000
shares = {l: [] for l in ligands}
totals = []
for _ in range(N):
    draw = sorted(10 ** rng.uniform(1, 4, size=len(KD_LADDER)))
    kd = build_kd(RANKING_VINA, draw)
    kd["glucose"] = 10 ** rng.uniform(4, 7)
    th = occupancy(kd, CONC)
    tot = sum(th.values())
    totals.append(tot)
    for l in ligands:
        shares[l].append(100 * th[l] / tot if tot > 0 else 0)

ax[2].boxplot([shares[l] for l in ligands], vert=False,
              tick_labels=ligands, showfliers=False)
ax[2].set(xlabel="share of bound receptor (%)",
          title=f"(c) Monte-Carlo over Kd uncertainty (n={N})")
ax[2].tick_params(labelsize=7)

plt.tight_layout()
plt.savefig("model3_competition.png", dpi=150)
print("wrote model3_competition.png\n")

totals = np.array(totals)
print(f"Total occupancy across {N} draws: median {np.median(totals):.3f}, "
      f"5th-95th pct {np.percentile(totals,5):.3f} - {np.percentile(totals,95):.3f}")

dom = {l: 0 for l in ligands}
for i in range(N):
    dom[max(ligands, key=lambda l: shares[l][i])] += 1
print("\nHow often each ligand dominates the signal:")
for l in sorted(dom, key=dom.get, reverse=True):
    if dom[l]:
        print(f"  {l:<15}{100*dom[l]/N:>6.1f}%")

gl = np.array(shares["glucose"])
print(f"\nNegative control: glucose exceeds 5% of the signal in "
      f"{100*np.mean(gl>5):.1f}% of draws.")
print("\nNote: naphthalene is present at 25x the pyrene concentration but binds")
print("more weakly - concentration matters as much as affinity in a mixture.")
