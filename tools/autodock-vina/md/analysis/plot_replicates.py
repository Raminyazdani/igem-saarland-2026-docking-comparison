import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
CUT = 0.5
COLORS = {"pyrene": "#1b6ca8", "phenanthrene": "#c25a1e"}
if len(sys.argv) < 3:
    sys.exit('usage: plot_replicates.py out.png "ligand|run=file.xvg" ...')
out, specs = sys.argv[1], sys.argv[2:]
n = len(specs)
fig, axes = plt.subplots((n + 1) // 2, 2, figsize=(11, 3 * ((n + 1) // 2)), sharex=True, sharey=True)
for ax, spec in zip(np.atleast_1d(axes).flat, specs):
    label, path = spec.split("=", 1)
    lig, run = label.split("|")
    t, y = np.loadtxt(path, unpack=True)
    t /= 1000
    b = y < CUT
    last = t[b].max() if b.any() else 0
    print(f"{lig:<13}{run}: bound {100*b.mean():5.1f}%, last contact {last:5.1f} ns, "
          f"final-50ns mean {y[t>=50].mean():.2f} nm, max {y.max():.2f} nm")
    ax.plot(t, y, lw=0.5, color=COLORS.get(lig, "#444"), alpha=0.85)
    ax.axhline(CUT, ls="--", lw=0.9, color="0.35")
    if b.mean() < 0.99:
        ax.axvline(last, ls=":", lw=1.1, color="#b00020")
        ax.annotate(f"leaves at {last:.1f} ns", xy=(last, 0), xytext=(last + 3, 3.5),
                    fontsize=8.5, color="#b00020")
    ax.text(0.98, 0.93, f"{lig}, {run}", transform=ax.transAxes, ha="right", va="top",
            fontsize=10.5, fontweight="bold")
    ax.text(0.98, 0.81, f"bound {100*b.mean():.1f}% of run", transform=ax.transAxes,
            ha="right", va="top", fontsize=9, color="0.35")
    ax.set_xlim(0, t.max()); ax.set_ylim(0, 4.4)
    ax.spines[["top", "right"]].set_visible(False)
axes = np.atleast_2d(axes)
for ax in axes[:, 0]: ax.set_ylabel("min. distance (nm)")
for ax in axes[-1, :]: ax.set_xlabel("time (ns)")
axes[0, 0].text(99, 0.62, "contact threshold 0.5 nm", ha="right", va="bottom", fontsize=8, color="0.35")
fig.suptitle("Ligand to pocket-4 distance — independent 100 ns replicates", fontsize=11.5, y=0.98)
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(out, dpi=300)
print("\n" + out)
