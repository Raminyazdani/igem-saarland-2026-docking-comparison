#!/usr/bin/env python3
"""Merge all DOCKING_RESULT*.json into one normalized long table.

Recomputes a direction-aware `normalized_rank` per (tool, target) from docking_score when
`rank_within_tool` is missing, then sets `rank_used = rank_within_tool or normalized_rank`.

Usage:
    python combine_results.py [file-or-dir ...] -o reports/tables/all_docking_results.csv

WARNING: raw docking_score is NOT comparable across tools. Use rank_used / consensus only.
"""
import os, sys, argparse
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from load_results import load_many  # noqa: E402


def _normalized_rank(group):
    """Direction-aware min-rank of ok rows within one (tool, target) group."""
    asc = group["score_direction"].iloc[0] == "lower_is_better"
    ok = group[group["status"] == "ok"]
    return ok["docking_score"].rank(ascending=asc, method="min")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="*", help="result files/dirs (default: results/)")
    ap.add_argument("-o", "--out", default="reports/tables/all_docking_results.csv")
    a = ap.parse_args()

    rows = load_many(a.paths or ["results"])
    if not rows:
        sys.exit("no DOCKING_RESULT*.json rows found")
    df = pd.DataFrame(rows)

    df["normalized_rank"] = pd.NA
    for _, g in df.groupby(["tool_name", "target_id"], dropna=False):
        df.loc[g.index.intersection(_normalized_rank(g).index), "normalized_rank"] = _normalized_rank(g)
    df["rank_used"] = df["rank_within_tool"].fillna(df["normalized_rank"])

    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    df.to_csv(a.out, index=False)
    print(f"wrote {a.out}  ({len(df)} rows, {df.tool_name.nunique()} tool(s), {df.target_id.nunique()} target(s))")
    print("NOTE: raw docking_score is NOT comparable across tools - compare rank_used / consensus_ranking.")


if __name__ == "__main__":
    main()
