#!/usr/bin/env python3
"""One-shot orchestrator: validate -> combine -> tables -> plots.

Usage:
    python compare.py [results_dir]      # default: reports/collected

Where results live:
    - across branches: run collect_from_branches.sh first -> reports/collected/ (the default)
    - single checkout: point it at the per-tool results with `python compare.py tools`
      (finds tools/<tool>/results/DOCKING_RESULT.json)

Typical flow:
    bash collect_from_branches.sh        # gather each tool/* branch's result into reports/collected/
    python compare.py                    # build reports/tables/* and reports/figures/*
"""
import os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
COMBINED = "reports/tables/all_docking_results.csv"


def run(script, *args):
    cmd = [sys.executable, os.path.join(HERE, script), *args]
    print("+", script, *args)
    subprocess.check_call(cmd)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "reports/collected"
    run("validate_results.py", src)
    run("combine_results.py", src, "-o", COMBINED)
    run("make_tables.py", COMBINED, "-o", "reports/tables")
    run("make_plots.py", COMBINED, "-o", "reports/figures")
    print("done -> reports/tables/ and reports/figures/")


if __name__ == "__main__":
    main()
