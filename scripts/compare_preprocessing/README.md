# `compare_preprocessing` — analyse and converge the preprocessing step

The docking comparison has **two** analysable layers. `scripts/compare_results/` compares the *docking
results*; this package compares the *preprocessing* that came before them.

Each tool records its preparation in `tools/<tool>/preprocessing/PREPROCESSING.yaml` using an identical set
of keys. That lets us read all recipes side by side, find what already agrees, and reconcile what does not —
the path toward **one shared preprocessing that works for every tool** (a stretch goal, not a requirement).

## Run
```bash
pip install -r ../compare_results/requirements.txt   # same deps (pandas, pyyaml)
python compare_preprocessing.py            # -> reports/tables/preprocessing_comparison.csv + _consensus.csv
python status_overview.py                  # -> reports/tables/status_overview.csv (team dashboard)
```

## What you get
- **`preprocessing_comparison.csv`** — a step (rows) x tool (cols) matrix of every preprocessing choice.
- **`preprocessing_consensus.csv`** — per step: `SHARED` (all tools agree), `DIVERGENT` (values differ),
  or `UNFILLED`, with coverage.
- Printed summary: the SHARED steps become the backbone of a shared recipe; the DIVERGENT steps are the
  ones to reconcile.

## The convergence workflow (future / optional)
1. Every team fills `PREPROCESSING.yaml` for its tool.
2. Run `compare_preprocessing.py` → see SHARED vs DIVERGENT steps.
3. Agree on one value for each DIVERGENT step (e.g. one protonation pH, one charge model, one box).
4. Write that agreed recipe as the shared preprocessing and re-dock every tool from it — the fairest
   possible comparison, since only the docking engine differs.
