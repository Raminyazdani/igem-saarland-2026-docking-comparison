scrape the output data after running CB-Dock 3. Just add the results url

python tools/cb-dock/scripts/download_cb_dock_results.py \
  --result-url "YOUR_FULL_CB_DOCK_RESULT_URL" \
  --protein PahP \
  --ligand pyrene \
  --output-root tools/cb-dock/outputs


python tools/cb-dock/scripts/summarize_cb_dock_results.py

python tools/cb-dock/scripts/collect_best_poses.py

python tools/cb-dock/scripts/create_docking_result.py

## Additional setup and final validation

Run the commands from the repository root. The scripts use PyYAML and Playwright; ask a coordinator to add
and pin them in the managed `tools/cb-dock/requirements.txt`.

```bash
python -m pip install -r requirements.txt
python -m pip install -r tools/cb-dock/requirements.txt
python -m playwright install chromium

git rev-parse --short input-v1
python tools/cb-dock/scripts/create_docking_result.py --input-commit-hash <input-v1-hash>
python scripts/compare_results/validate_results.py tools/cb-dock/results/DOCKING_RESULT.json
```

Do not use the current branch hash in place of `input-v1`; the tag has not been created yet.
The final `create_docking_result.py` command above must therefore be rerun with `--input-commit-hash` once
that tag exists.
