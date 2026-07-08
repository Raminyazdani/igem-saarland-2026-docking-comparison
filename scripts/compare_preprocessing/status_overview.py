#!/usr/bin/env python3
"""Team-wide progress dashboard from every tool's status file.

Reads all tools/*/status/status.yaml into one table so we can see, at a glance, who has finished
preprocessing, docking, and committed a result.

Usage:
    python status_overview.py [tools_dir] [-o reports/tables]
Outputs:
    reports/tables/status_overview.csv
"""
import os, sys, glob, argparse
import yaml
import pandas as pd

COLS = ["tool", "branch", "preprocessing_status", "docking_status",
        "result_committed", "poses_committed", "last_updated", "n_blockers"]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("tools_dir", nargs="?", default="tools")
    ap.add_argument("-o", "--outdir", default="reports/tables")
    a = ap.parse_args()

    files = sorted(glob.glob(os.path.join(a.tools_dir, "*", "status", "status.yaml")))
    files = [f for f in files if os.sep + "_TEMPLATE" + os.sep not in f]
    if not files:
        sys.exit(f"no status.yaml found under {a.tools_dir}/*/status/")

    rows = []
    for f in files:
        d = yaml.safe_load(open(f, encoding="utf-8")) or {}
        blockers = d.get("blockers") or []
        rows.append({
            "tool": d.get("tool"), "branch": d.get("branch"),
            "preprocessing_status": d.get("preprocessing_status"),
            "docking_status": d.get("docking_status"),
            "result_committed": d.get("result_committed"),
            "poses_committed": d.get("poses_committed"),
            "last_updated": d.get("last_updated"),
            "n_blockers": len(blockers),
        })
    df = pd.DataFrame(rows, columns=COLS).sort_values("tool")
    os.makedirs(a.outdir, exist_ok=True)
    out = os.path.join(a.outdir, "status_overview.csv")
    df.to_csv(out, index=False)
    print(df.to_string(index=False))

    done = int((df.result_committed == True).sum())  # noqa: E712
    print(f"\n{done}/{len(df)} tools have committed a validated result. -> {out}")


if __name__ == "__main__":
    main()
