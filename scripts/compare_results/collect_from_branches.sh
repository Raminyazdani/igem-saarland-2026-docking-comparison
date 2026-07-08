#!/usr/bin/env bash
# Collect each tool/* branch's standardized result into reports/collected/.
# On branch tool/<name>, the result lives at tools/<name>/results/DOCKING_RESULT.json.
# Output names keep the substring "DOCKING_RESULT" so validate/combine globs match.
# Reports MISSING for any branch that has not produced a result yet.
set -euo pipefail

OUT=reports/collected
mkdir -p "$OUT"

branches=$(git branch --list 'tool/*' --format='%(refname:short)')
if [ -z "$branches" ]; then
  echo "No tool/* branches found. Create them first (see README / git commands)."
  exit 0
fi

for b in $branches; do
  name="${b#tool/}"                              # tool/gold -> gold
  path="tools/${name}/results/DOCKING_RESULT.json"
  safe=$(echo "$b" | tr '/' '_')                 # tool/gold -> tool_gold
  if git cat-file -e "$b:$path" 2>/dev/null; then
    git show "$b:$path" > "$OUT/${safe}.DOCKING_RESULT.json"
    echo "collected $b -> $OUT/${safe}.DOCKING_RESULT.json"
  else
    echo "MISSING result on $b (expected $path)"
  fi
done

echo "Done. Next: python compare.py $OUT"
