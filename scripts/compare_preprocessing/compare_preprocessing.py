#!/usr/bin/env python3
"""Compare every tool's preprocessing recipe side by side.

Reads all tools/*/preprocessing/PREPROCESSING.yaml, flattens them to a tool x step matrix, and reports
where the tools AGREE (candidate shared preprocessing) vs DIVERGE (needs reconciliation). This is the
first step toward designing ONE shared preprocessing that works for every tool.

Usage:
    python compare_preprocessing.py [tools_dir] [-o reports/tables]
        tools_dir default: tools/

Outputs:
    reports/tables/preprocessing_comparison.csv   step (rows) x tool (cols) matrix
    reports/tables/preprocessing_consensus.csv     per step: shared value / divergent values / coverage
"""
import os, sys, glob, json, argparse
import yaml
import pandas as pd

# keys that describe the *recipe* (analysed for convergence); identity/free-text keys are excluded.
STEP_PREFIXES = ("receptor.", "ligand.", "binding_site.")
STEP_EXTRA = ("random_seed",)
SKIP_KEYS = {"tool", "branch", "owners", "notes", "assumptions_and_deviations",
             "input_version_used", "software_versions"}


def flatten(d, prefix=""):
    out = {}
    for k, v in (d or {}).items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(flatten(v, key + "."))
        else:
            out[key] = v
    return out


def is_step(key):
    return key.startswith(STEP_PREFIXES) or key in STEP_EXTRA


def norm(v):
    """Normalize a value for equality comparison; None/'' -> None (unfilled)."""
    if v is None:
        return None
    if isinstance(v, str) and v.strip() == "":
        return None
    if isinstance(v, (list, dict)):
        return json.dumps(v, sort_keys=True)
    return v


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("tools_dir", nargs="?", default="tools")
    ap.add_argument("-o", "--outdir", default="reports/tables")
    a = ap.parse_args()

    files = sorted(glob.glob(os.path.join(a.tools_dir, "*", "preprocessing", "PREPROCESSING.yaml")))
    files = [f for f in files if os.sep + "_TEMPLATE" + os.sep not in f]
    if not files:
        sys.exit(f"no PREPROCESSING.yaml found under {a.tools_dir}/*/preprocessing/")

    recipes = {}   # tool_label -> flattened dict
    for f in files:
        doc = yaml.safe_load(open(f, encoding="utf-8")) or {}
        label = doc.get("tool") or os.path.basename(os.path.dirname(os.path.dirname(f)))
        recipes[label] = flatten(doc)

    # union of step keys across all recipes, in a stable order
    step_keys = []
    for r in recipes.values():
        for k in r:
            if is_step(k) and k not in SKIP_KEYS and k not in step_keys:
                step_keys.append(k)
    step_keys.sort()

    os.makedirs(a.outdir, exist_ok=True)

    # matrix: rows = steps, cols = tools
    matrix = pd.DataFrame(index=step_keys, columns=list(recipes.keys()))
    for tool, r in recipes.items():
        for k in step_keys:
            matrix.loc[k, tool] = r.get(k)
    matrix.to_csv(os.path.join(a.outdir, "preprocessing_comparison.csv"))

    # consensus per step
    rows = []
    n_tools = len(recipes)
    shared, divergent, unfilled = [], [], []
    for k in step_keys:
        vals = {t: norm(recipes[t].get(k)) for t in recipes}
        filled = {t: v for t, v in vals.items() if v is not None}
        distinct = sorted({str(v) for v in filled.values()})
        if not filled:
            state = "UNFILLED"; unfilled.append(k)
        elif len(distinct) == 1:
            state = "SHARED"; shared.append((k, distinct[0]))
        else:
            state = "DIVERGENT"; divergent.append((k, distinct))
        rows.append(dict(step=k, state=state, coverage=f"{len(filled)}/{n_tools}",
                         shared_value=distinct[0] if state == "SHARED" else "",
                         distinct_values=" | ".join(distinct) if state == "DIVERGENT" else ""))
    pd.DataFrame(rows).to_csv(os.path.join(a.outdir, "preprocessing_consensus.csv"), index=False)

    # human summary
    print(f"Compared {n_tools} tool(s): {', '.join(recipes)}")
    print(f"\nSHARED steps (already agree -> keep in the shared preprocessing): {len(shared)}")
    for k, v in shared:
        print(f"  = {k} = {v}")
    print(f"\nDIVERGENT steps (must be reconciled to build one shared preprocessing): {len(divergent)}")
    for k, vs in divergent:
        print(f"  ~ {k}: {' | '.join(vs)}")
    print(f"\nUNFILLED steps (no tool has decided yet): {len(unfilled)}")
    for k in unfilled:
        print(f"  ? {k}")
    print(f"\ntables -> {a.outdir}/preprocessing_comparison.csv, preprocessing_consensus.csv")
    if divergent:
        print("\nNEXT: reconcile each DIVERGENT step into one agreed value, write it as the shared "
              "preprocessing, then re-dock every tool from that common starting point.")


if __name__ == "__main__":
    main()
