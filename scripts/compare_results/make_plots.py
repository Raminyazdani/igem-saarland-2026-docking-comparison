#!/usr/bin/env python3
"""Figures for the wiki, from the combined results CSV.

Usage:
    python make_plots.py [all_docking_results.csv] [-o reports/figures]

Outputs (into -o):
    score_heatmap_<target>.png   ligand x tool RANK heatmap (1 = best) per target
    consensus_<target>.png       mean rank across tools per ligand, per target
    score_by_tool_<target>.png   raw scores, one panel per tool (within-tool only)
    runtime_by_tool.png          total runtime per tool

FAIRNESS RULE: raw scores are NEVER plotted on a single shared cross-tool axis. Cross-tool
comparison is always by RANK. score_by_tool_* uses one independent panel per tool and says so.
"""
import os, sys, argparse
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CAPTION = "Cross-tool comparison uses RANKS, not raw scores."


def heatmap(df, target, outdir):
    g = df[(df.target_id == target) & (df.status == "ok")]
    piv = g.pivot_table(index="ligand_id", columns="tool_name", values="rank_used")
    if piv.empty:
        return
    fig, ax = plt.subplots(figsize=(1.8 + 1.2 * piv.shape[1], 1.2 + 0.5 * piv.shape[0]))
    im = ax.imshow(piv.values, cmap="RdYlGn_r", aspect="auto")
    ax.set_xticks(range(piv.shape[1])); ax.set_xticklabels(piv.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(piv.shape[0])); ax.set_yticklabels(piv.index, fontsize=8)
    for i in range(piv.shape[0]):
        for j in range(piv.shape[1]):
            v = piv.values[i, j]
            if v == v:  # not NaN
                ax.text(j, i, int(v), ha="center", va="center", fontsize=8)
    ax.set_title(f"Rank heatmap - {target} (1 = best)\n{CAPTION}", fontsize=9)
    fig.colorbar(im, ax=ax, label="rank_used (1 = best)")
    fig.tight_layout(); fig.savefig(os.path.join(outdir, f"score_heatmap_{target}.png"), dpi=130); plt.close(fig)


def consensus_plot(df, target, outdir):
    g = df[(df.target_id == target) & (df.status == "ok")]
    cons = g.groupby("ligand_id")["rank_used"].mean().sort_values()
    if cons.empty:
        return
    fig, ax = plt.subplots(figsize=(6, 0.6 + 0.4 * len(cons)))
    ax.barh(cons.index, cons.values, color="#4C72B0")
    ax.invert_yaxis()
    ax.set_xlabel("mean rank across tools (lower = better)")
    ax.set_title(f"Consensus ranking - {target}\n{CAPTION}", fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(outdir, f"consensus_{target}.png"), dpi=130); plt.close(fig)


def score_by_tool(df, target, outdir):
    """One panel per tool: raw within-tool scores. Independent y-axes -> no cross-tool axis."""
    g = df[(df.target_id == target) & (df.status == "ok")]
    tools = sorted(g.tool_name.dropna().unique())
    if not tools:
        return
    fig, axes = plt.subplots(len(tools), 1, figsize=(7, 1.8 * len(tools)), squeeze=False)
    for ax, tool in zip(axes[:, 0], tools):
        t = g[g.tool_name == tool].sort_values("docking_score")
        ax.bar(t.ligand_id, t.docking_score, color="#55A868")
        unit = t.score_unit.dropna().iloc[0] if not t.score_unit.dropna().empty else ""
        ax.set_ylabel(f"{tool}\n({unit})", fontsize=8)
        ax.tick_params(axis="x", labelrotation=45, labelsize=7)
    axes[0, 0].set_title(f"Raw scores per tool - {target} (WITHIN-tool only; do NOT compare panels)\n{CAPTION}",
                         fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(outdir, f"score_by_tool_{target}.png"), dpi=130); plt.close(fig)


def runtime_by_tool(df, outdir):
    if "runtime_sec" not in df or df["runtime_sec"].dropna().empty:
        return
    rt = df.groupby("tool_name")["runtime_sec"].sum().sort_values()
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(range(len(rt)), rt.values, color="#C44E52")
    ax.set_xticks(range(len(rt))); ax.set_xticklabels(rt.index, rotation=45, ha="right")
    ax.set_ylabel("total runtime (s)"); ax.set_title("Runtime by tool")
    fig.tight_layout(); fig.savefig(os.path.join(outdir, "runtime_by_tool.png"), dpi=130); plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("csv", nargs="?", default="reports/tables/all_docking_results.csv")
    ap.add_argument("-o", "--outdir", default="reports/figures")
    a = ap.parse_args()

    df = pd.read_csv(a.csv)
    os.makedirs(a.outdir, exist_ok=True)
    for target in sorted(df.target_id.dropna().unique()):
        heatmap(df, target, a.outdir)
        consensus_plot(df, target, a.outdir)
        score_by_tool(df, target, a.outdir)
    runtime_by_tool(df, a.outdir)
    print("figures ->", a.outdir)


if __name__ == "__main__":
    main()
