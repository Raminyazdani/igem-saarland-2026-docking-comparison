#!/usr/bin/env python3
"""Shared helper: read DOCKING_RESULT*.json files into flat, long-format rows.

One output row per (tool, target_id, ligand_id). Tool-level fields (score_direction,
software_version, commit hash, ...) are carried onto every row so downstream tables/plots
can group without re-opening the JSON.

Import this from combine_results.py etc. Can also be run directly to print a row count:
    python load_results.py [file-or-dir ...]
"""
import sys, os, json, glob


def collect_files(paths):
    """Expand files/dirs into a sorted list of DOCKING_RESULT*.json, skipping templates."""
    files = []
    for p in paths:
        if os.path.isdir(p):
            files += glob.glob(os.path.join(p, "**", "*DOCKING_RESULT*.json"), recursive=True)
        elif p.endswith(".json"):
            files.append(p)
    return sorted({f for f in files if "template" not in os.path.basename(f).lower()})


def load_rows(path):
    """Return long-format row dicts for one result file (one dict per result entry)."""
    d = json.load(open(path, encoding="utf-8"))
    rows = []
    for r in d.get("results", []):
        rows.append(dict(
            source_file=os.path.basename(path),
            tool_name=d.get("tool_name"),
            branch=d.get("branch"),
            score_direction=d.get("score_direction"),
            software_version=d.get("software_version"),
            input_commit_hash=d.get("input_commit_hash"),
            date_completed=d.get("date_completed"),
            target_id=r.get("target_id"),
            ligand_id=r.get("ligand_id"),
            pubchem_cid=r.get("pubchem_cid"),
            docking_score=r.get("docking_score"),
            score_unit=r.get("score_unit"),
            rank_within_tool=r.get("rank_within_tool"),
            runtime_sec=r.get("runtime_sec"),
            pose_file=r.get("pose_file"),
            status=r.get("status"),
            failure_reason=r.get("failure_reason"),
        ))
    return rows


def load_many(paths):
    rows = []
    for f in collect_files(paths):
        try:
            rows += load_rows(f)
        except Exception as e:  # keep going; combine/validate report the bad file
            print(f"skip {f}: {e}", file=sys.stderr)
    return rows


if __name__ == "__main__":
    rows = load_many(sys.argv[1:] or ["results"])
    tools = {r["tool_name"] for r in rows}
    targets = {r["target_id"] for r in rows}
    print(f"{len(rows)} rows from {len(tools)} tool(s), {len(targets)} target(s)")
