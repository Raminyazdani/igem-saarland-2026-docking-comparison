#!/usr/bin/env python3
"""Build summary tables from the combined results CSV.

Usage:
    python make_tables.py [all_docking_results.csv] [-o reports/tables]

Outputs (into -o):
    best_score_per_tool.csv     best (rank 1) ligand per tool+target
    best_ligand_per_target.csv  consensus top ligand per target
    consensus_ranking.csv       mean rank_used per target+ligand across tools
    runtime_comparison.csv      runtime totals per tool
    failure_summary.csv         failed ligands per tool
    summary_tables.xlsx         all of the above, one sheet each (if openpyxl present)

Ranking uses status==ok rows only. Consensus needs >=2 tools per target (warns otherwise).
"""
import os, sys, argparse
import pandas as pd


def best_per_tool(ok):
    return (ok[ok.rank_used == 1]
            [["tool_name", "target_id", "ligand_id", "docking_score", "score_unit"]]
            .sort_values(["target_id", "tool_name"]))


def consensus(ok):
    cons = (ok.groupby(["target_id", "ligand_id"])
              .agg(mean_rank=("rank_used", "mean"), n_tools=("tool_name", "nunique"))
              .reset_index())
    cons["consensus_rank"] = cons.groupby("target_id")["mean_rank"].rank(method="min")
    return cons.sort_values(["target_id", "consensus_rank"])


def runtime(df):
    if "runtime_sec" not in df or df["runtime_sec"].dropna().empty:
        return pd.DataFrame(columns=["tool_name", "total_sec", "mean_sec", "n"])
    return (df.groupby("tool_name")["runtime_sec"]
              .agg(total_sec="sum", mean_sec="mean", n="count")
              .reset_index().sort_values("total_sec"))


def failures(df):
    fail = df[df.status == "failed"]
    if fail.empty:
        return pd.DataFrame(columns=["tool_name", "target_id", "failed_ligands"])
    return (fail.groupby(["tool_name", "target_id"])["ligand_id"]
                .agg(lambda s: ", ".join(sorted(s))).reset_index(name="failed_ligands"))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("csv", nargs="?", default="reports/tables/all_docking_results.csv")
    ap.add_argument("-o", "--outdir", default="reports/tables")
    a = ap.parse_args()

    df = pd.read_csv(a.csv)
    os.makedirs(a.outdir, exist_ok=True)
    ok = df[df.status == "ok"].copy()

    bpt = best_per_tool(ok)
    cons = consensus(ok)
    best_lig = cons[cons.consensus_rank == 1]
    rt = runtime(df)
    fail = failures(df)

    tables = {
        "best_score_per_tool": bpt,
        "consensus_ranking": cons,
        "best_ligand_per_target": best_lig,
        "runtime_comparison": rt,
        "failure_summary": fail,
    }
    for name, t in tables.items():
        t.to_csv(os.path.join(a.outdir, f"{name}.csv"), index=False)

    # optional single workbook
    try:
        with pd.ExcelWriter(os.path.join(a.outdir, "summary_tables.xlsx")) as xl:
            for name, t in tables.items():
                t.to_excel(xl, sheet_name=name[:31], index=False)
    except Exception as e:
        print(f"(skipped .xlsx: {e})")

    for target, n in cons.groupby("target_id")["n_tools"].max().items():
        if n < 2:
            print(f"WARN: consensus for {target} uses only {int(n)} tool - not yet a real consensus.")
    print("tables ->", a.outdir, ":", ", ".join(tables))
    print("NOTE: comparisons use RANKS, not raw cross-tool scores.")


if __name__ == "__main__":
    main()
