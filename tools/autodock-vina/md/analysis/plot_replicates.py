import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CUT, TOP = 0.5, 3.4
COL = {"pyrene": "#1b5e9c", "phenanthrene": "#c0601a"}
out = sys.argv[1] if len(sys.argv) > 1 else "pocket4_replicates.png"

def load(f):
    a = np.array([l.split() for l in open(f) if l.strip() and l[0] not in "#@"], float)
    return a[:, 0] / 1000, a[:, 1]

fig, ax = plt.subplots(2, 3, figsize=(13.2, 6.8), sharex=True, sharey=True)
for r, lig in enumerate(("pyrene", "phenanthrene")):
    for c, rep in enumerate((1, 2, 3)):
        a = ax[r][c]
        t, y = load(f"{lig}_rep{rep}_mindist.xvg")
        bound = y < CUT
        frac = 100 * bound.mean()
        last = t[bound].max() if bound.any() else 0.0
        tail = y[t >= 50].mean()
        a.fill_between(t, TOP * 0.955, TOP, where=bound, color=COL[lig], lw=0)
        a.fill_between(t, TOP * 0.955, TOP, where=~bound, color="0.86", lw=0)
        a.plot(t, y, color=COL[lig], lw=0.7)
        a.axhline(CUT, ls="--", lw=0.9, color="0.35")
        if last < t[-1] - 1:
            a.axvline(last, ls=":", lw=1.1, color="#b00020")
            a.annotate(f"leaves {last:.1f} ns", (last, 2.95), xytext=(5, 0),
                       textcoords="offset points", fontsize=8.5, color="#b00020")
        a.set_title(f"{lig} · replicate {rep}   —   {frac:.1f}% in contact",
                    fontsize=10, loc="left", pad=7)
        a.text(0.985, 0.80, f"mean 50-100 ns: {tail:.2f} nm", transform=a.transAxes,
               ha="right", fontsize=8.5, color="0.3")
        a.set(xlim=(0, 100), ylim=(0, TOP))
        a.grid(alpha=0.25, lw=0.5)
        if r == 1: a.set_xlabel("time (ns)")
        if c == 0: a.set_ylabel("min. distance to pocket 4 (nm)")

ax[0][1].text(50, 0.70, "0.5 nm contact cutoff", fontsize=8.5, color="0.35", ha="center")
fig.text(0.012, 0.972, "PahP pocket 4 - ligand retention across three independent 100 ns replicates",
         fontsize=12.5, color="0.1")
fig.text(0.012, 0.937, "Top bar marks frames in contact (colour) or away (grey). "
         "Pyrene holds the docked pose in 2 of 3 runs, phenanthrene in 1 of 3.",
         fontsize=9, color="0.4")
fig.tight_layout(rect=(0, 0, 1, 0.925))
fig.savefig(out, dpi=200)
