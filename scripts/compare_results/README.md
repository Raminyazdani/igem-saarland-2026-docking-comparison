# `compare_results` — docking comparison package

Small, standard-library + pandas/matplotlib scripts that turn each tool's
`results/DOCKING_RESULT.json` into shared tables and figures. **All cross-tool comparison is by
rank** — raw docking scores from different tools are not on the same scale and are never compared
directly.

## Run it (3 commands)

```bash
pip install -r requirements.txt
bash collect_from_branches.sh          # gather each tool/* branch -> reports/collected/
python compare.py                      # validate -> combine -> tables -> figures
```

Outputs land in `reports/tables/` (CSV + `summary_tables.xlsx`) and `reports/figures/` (PNG).

## Scripts

| Script | Does |
|--------|------|
| `validate_results.py` | Checks result files against `schema/DOCKING_RESULT.schema.json` + business rules. Exit 1 on any ERROR. |
| `load_results.py` | Shared helper: flattens result JSON into long-format rows. |
| `combine_results.py` | Merges all results into `reports/tables/all_docking_results.csv`; computes direction-aware `rank_used`. |
| `make_tables.py` | Summary CSVs (best per tool, consensus, runtime, failures) + xlsx. |
| `make_plots.py` | Rank heatmap, consensus, within-tool score panels, runtime. |
| `compare.py` | Orchestrates validate -> combine -> tables -> plots. |
| `collect_from_branches.sh` | Pulls `results/DOCKING_RESULT.json` from every `tool/*` branch. |

## Validate a single file

```bash
python validate_results.py ../../results/DOCKING_RESULT.example.json
```

## Key rule: ranks, not raw scores

Each team records `score_direction` (`lower_is_better` for Vina/Glide, `higher_is_better` for GOLD).
`combine_results.py` uses it to compute a within-tool rank; consensus is the mean rank across tools.
Every table/figure is labelled to make this explicit.
