import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
CUT = 0.5
COLORS = ["#1b6ca8", "#c25a1e", "#3f7d3f", "#7b4397"]
if len(sys.argv) < 3:
    sys.exit("usage: plot_mindist.py out.png label=file.xvg [label=file.xvg ...]")
out, pairs = sys.argv[1], [a.split("=", 1) for a in sys.argv[2:]]
fig, axes = plt.subplots(len(pairs), 1, figsize=(7.2, 2.7*len(pairs)), sharex=True, sharey=True)
axes = np.atleast_1d(axes)
for ax, (label, path), col in zip(axes, pairs, COLORS):
    t, y = np.loadtxt(path, unpack=True)
    t /= 1000
    bound = y < CUT
    last = t[bound].max() if bound.any() else 0
    print(f"{label}: bound {100*bound.mean():.1f}%, last contact {last:.1f} ns, final-half mean {y[t>=t.max()/2].mean():.2f} nm")
    ax.plot(t, y, lw=0.5, color=col, alpha=0.85)
    ax.axhline(CUT, ls="--", lw=0.9, color="0.35")
    ax.axvline(last, ls=":", lw=1.1, color="#b00020")
    ax.annotate(f"last contact {last:.1f} ns", xy=(last, 0), xytext=(last+2, 3.55), fontsize=8.5, color="#b00020")
    ax.text(0.985, 0.93, f"{label}  —  bound {100*bound.mean():.1f}% of run", transform=ax.transAxes, ha="right", va="top", fontsize=10, fontweight="bold")
    ax.text(t.max()-1, CUT+0.12, f"contact threshold {CUT} nm", ha="right", va="bottom", fontsize=8, color="0.35")
    ax.set_ylabel("min. distance (nm)")
    ax.set_xlim(0, t.max())
    ax.set_ylim(0, 4.4)
    ax.spines[["top", "right"]].set_visible(False)
axes[-1].set_xlabel("time (ns)")
fig.suptitle("Ligand to pocket-4 lining distance, PahP, 100 ns MD", fontsize=11.5, y=0.98)
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(out, dpi=300)
print(out)
