# `tools/` — one self-contained workspace per docking tool

Every docking tool gets its own folder `tools/<tool>/`. Inside, the work is split into **two major
steps** that are kept deliberately separate so we can analyse them independently:

1. **`preprocessing/`** — say *exactly* what preparation your tool needs, and do it. Receptor cleanup,
   signal-peptide removal, protonation, charges, format conversion, box definition — all documented in a
   **structured, comparable** manifest (`PREPROCESSING.yaml`) plus a script that reproduces it.
2. **`docking/`** — everything else: the actual docking run, using the prepared inputs.

## Why the split matters (the shared-preprocessing goal)
Because every tool records its preprocessing in the *same structured form*, we can later:
- read and compare all six preprocessing recipes side by side (`scripts/compare_preprocessing/`),
- see where they agree and where they diverge, and
- **design one shared preprocessing** that works for every tool, then re-dock from that single, common
  starting point for the fairest possible comparison.

This convergence is a **stretch goal for later, not a requirement.** Do your tool's own preprocessing now;
the shared design is something we attempt once all recipes are in.

## Per-tool folder tree
```
tools/<tool>/
  README.md            # what this workspace is
  requirements.txt     # this tool's Python deps (managed by Ramin & Elnaz)
  .gitignore           # tool-specific scratch to ignore (managed by Ramin & Elnaz; keep minimal)
  inputs/              # canonical inputs converted to your tool's formats (committed — reviewed in PRs)
  preprocessing/       # PREPROCESSING.yaml (comparable manifest) + steps.md + preprocess.sh
  docking/             # DOCKING.md + run_docking.sh (the actual docking)
  configurations/      # config.yaml — your tool's parameters (box, seed, exhaustiveness, ...)
  outputs/             # raw/native tool output & logs (committed — reviewed in PRs)
  results/             # DOCKING_RESULT.json  <-- THE single standardized file for final comparison
                       #   + poses/ (final chosen poses, committed)
  status/              # status.yaml — progress + blockers (read by the status overview)
```

## The one file that everything else depends on
`tools/<tool>/results/DOCKING_RESULT.json` is the **single standardized result** that feeds the final
tables and plots. It holds the comparison values and keys (per-ligand score, rank, direction, pose path).
Copy `results/DOCKING_RESULT.template.json` (repo root), fill it, and validate it before committing.

## Adding a new tool
Copy `tools/_TEMPLATE/` to `tools/<new-tool>/` and fill in the identity fields. Then add the tool to
`input/canonical/docking_config.yaml`.

See [`../TEAM_INSTRUCTIONS.md`](../TEAM_INSTRUCTIONS.md) for the full per-team workflow.
