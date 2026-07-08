# PAH Docking-Comparison Repo & Workflow Plan (v1 — 2026-07-08)

Confidence labels: **CONFIRMED** (from files/memory), **LIKELY** (reasonable inference), **UNCERTAIN** (needs a decision), **BLOCKED** (cannot proceed until an input exists).

---

## 1. Short Decision Summary
- **Dock target = PahP** (periplasmic PAH-binding protein, 317 aa) as primary; **PahS** (686 aa) secondary/blind. The other construct files (CFP/YFP, GCaMP6f, MBP-mScarlet-G3BP1, pRS416, pET backbones) are **reference only — not docking receptors**. **CONFIRMED** from constructs + iScience 2023.
- **Dock the protein, not the plasmid/fusion.** Extract CDS → translate → dock the PahP protein domain only (strip FP, His-tag, linker; remove PahP signal peptide). **CONFIRMED/LIKELY**.
- **Ligands = the prepared PAH panel** (pyrene primary + phenanthrene, benzo[a]pyrene, naphthalene, anthracene, fluoranthene) + glucose negative control. Already standardized. **CONFIRMED**.
- **Structures do not exist** for PahP/PahS → an **AlphaFold model + binding box is the one hard blocker**. **BLOCKED**.
- Repo = `main` (frozen canonical input) + one branch per tool + one mandatory `DOCKING_RESULT.json` + a small Python compare package. **CONFIRMED design**.
- Repo skeleton is already scaffolded in this folder and the compare scripts are tested end-to-end.

## 2. Recommended Repository Name
**`igem-saarland-2026-docking-comparison`** (used for the scaffold). Shorter alternatives if you prefer: `saar-pahp-docking` or `igem-saar-dock-bench`.

## 3. Repository Folder Tree
```
igem-saarland-2026-docking-comparison/
  README.md
  TEAM_INSTRUCTIONS.md
  .gitignore
  input/
    raw/constructs/            # .dna/.gbk reference copies (NOT docked directly)
    canonical/                 # SHARED, FROZEN starting point
      targets/                 # PahP.fasta, PahS.fasta, target_metadata.csv, (+ PahP.pdb when ready)
      ligands/                 # ligands.smi, ligands_3D.sdf, ligand_metadata.csv
      binding_site/            # PahP_box.json (added at input-v1)
      config.yaml
    tool_specific/             # per-team converted inputs (gitignored)
  results/
    DOCKING_RESULT.template.json
    DOCKING_RESULT.example.json
    poses/  logs/
  scripts/compare_results/     # validate / combine / make_tables / make_plots / compare / schema / requirements
  reports/                     # generated tables + figures (this plan lives here)
```
Only these folders — nothing else is needed for a clean comparison. **Keep it this simple.**

## 4. Explanation of Main Folders
- `input/raw/` — the untouched project construct files, for provenance. **Read-only.** They are *not* docking inputs.
- `input/canonical/` — the **single shared, frozen** starting point. Same receptor + same ligands + same box for every tool. Changing anything here means re-freezing (new `input-vN`) for everyone.
- `input/tool_specific/` — where each team converts canonical inputs into their tool's format (PDBQT, mol2, Maestro…). Gitignored so bulky/format-specific files don't pollute the shared history.
- `results/` — the mandatory `DOCKING_RESULT.json` + final poses + logs.
- `scripts/compare_results/` — the Python comparison package.
- `reports/` — generated tables/plots for the wiki/model page.

## 5. Canonical Input Plan
Files in `input/canonical/` (the only shared truth):

```
filename: targets/PahP.fasta
purpose: mature PahP protein sequence to fold/dock
source: translated from piGEM002/GF2/GF3 (.dna)
how to generate: DONE (snapgene_reader -> Biopython translate)
who may edit: Ramin (on main only)
validation rule: 1 sequence, ~317 aa (or shorter after signal-peptide removal), no stop chars
status: CONFIRMED (present)

filename: targets/PahS.fasta
purpose: PahS sequence (secondary target)
source: translated from piGEM001/GF1
how to generate: DONE
who may edit: Ramin (main)
validation rule: 1 sequence, ~686 aa
status: CONFIRMED (present)

filename: targets/target_metadata.csv
purpose: target id, priority, membrane flag, structure status
source: project memory
how to generate: DONE
who may edit: Ramin (main)
validation rule: PahP row priority 1
status: CONFIRMED (present)

filename: targets/PahP.pdb (+ PahP_clean.pdb)
purpose: THE receptor structure everyone docks into
source: AlphaFold2/3 (ColabFold) from PahP.fasta, then cleaned
how to generate: ColabFold -> remove signal peptide -> add H, fix termini (PDBFixer/Maestro)
who may edit: one nominated modeller (main only)
validation rule: single chain, pLDDT recorded, pocket residues resolved
status: BLOCKED (must be produced first)

filename: binding_site/PahP_box.json
purpose: shared docking box / pocket center+size
source: fpocket or P2Rank on PahP.pdb
how to generate: run pocket predictor, pick the PAH pocket, save center xyz + size
who may edit: same modeller (main only)
validation rule: center+size present; consistent Angstrom units
status: BLOCKED (needs PahP.pdb)

filename: ligands/ligands_3D.sdf
purpose: identical 3D ligands for all tools
source: RDKit ETKDG from validated SMILES
how to generate: DONE (6 PAHs + glucose control, pH 7.4)
who may edit: Ramin (main)
validation rule: each entry parses; formula matches PubChem CID
status: CONFIRMED (present)

filename: ligands/ligands.smi + ligand_metadata.csv
purpose: SMILES + CID/formula/MW/logP/InChIKey
source: RDKit
how to generate: DONE
who may edit: Ramin (main)
validation rule: InChIKey matches CID
status: CONFIRMED (present)

filename: config.yaml
purpose: single source of truth (targets, ligands, tools, score-comparability warning)
source: project memory
how to generate: DONE
who may edit: Ramin (main)
validation rule: input_version set; scores_not_directly_comparable: true
status: CONFIRMED (present)
```
**Freeze rule:** tag `input-v1` **only after** `PahP.pdb` + `PahP_box.json` are added. Everything else is ready now.

## 6. Preprocessing Checklist
```
Step: Extract CDS from .dna/.gbk
Input: piGEM001/002/003, GF1-3   Output: PahP/PahS CDS FASTA
Tool: snapgene_reader + Biopython   Manual/auto: automated
Validation: single clean ORF, no internal stop   Risk: low   Priority: DONE (CONFIRMED)

Step: Translate CDS -> protein
Input: CDS FASTA   Output: PahP.fasta (317aa), PahS.fasta (686aa)
Tool: Biopython   Manual/auto: automated
Validation: PahP identical across constructs   Risk: low   Priority: DONE (CONFIRMED)

Step: Choose docking scope (protein vs construct)
Input: fusion constructs   Output: decision = dock PahP domain only (strip FP/His/linker)
Tool: reasoning   Manual/auto: manual
Validation: FP/tag sequences excluded   Risk: med (define PahP boundaries)   Priority: HIGH (LIKELY)

Step: Signal-peptide handling for PahP
Input: PahP.fasta   Output: mature PahP sequence
Tool: SignalP 6   Manual/auto: automated
Validation: cleavage site reported   Risk: med   Priority: HIGH (LIKELY)

Step: Generate receptor structure
Input: mature PahP.fasta   Output: PahP.pdb
Tool: AlphaFold2/3 (ColabFold)   Manual/auto: automated (Colab/GPU)
Validation: pLDDT map; pocket region well-folded   Risk: HIGH   Priority: CRITICAL (BLOCKED)

Step: Clean receptor
Input: PahP.pdb   Output: PahP_clean.pdb
Tool: PDBFixer / Maestro Prep   Manual/auto: semi
Validation: H added, termini capped, no clashes   Risk: low   Priority: after structure

Step: Define docking box / pocket
Input: PahP_clean.pdb   Output: PahP_box.json
Tool: fpocket / P2Rank   Manual/auto: semi
Validation: box covers hydrophobic PAH pocket   Risk: med   Priority: after structure (BLOCKED)

Step: Prepare ligands from SMILES + 3D conformers
Input: PubChem CIDs   Output: ligands_3D.sdf
Tool: RDKit ETKDG + MMFF, pH 7.4   Manual/auto: automated
Validation: formula vs CID   Risk: low   Priority: DONE (CONFIRMED)

Step: Per-tool conversion
Input: canonical receptor+ligands   Output: PDBQT (Vina), mol2 (GOLD), Maestro (Glide)...
Tool: Meeko/MGLTools, Hermes, LigPrep   Manual/auto: per team
Validation: charges/atom types sane   Risk: med   Priority: per branch (LIKELY)
```

## 7. Branch Strategy and Git Commands
**Branches:** `main` (protected, canonical only) + `dock/vina`, `dock/gold`, `dock/glide`, `dock/cb-dock`, `dock/unimol`, `dock/discovery-studio` (+ optional `dock/smina` fallback). Each team: uses `input/canonical/`, writes converted input to `input/tool_specific/<tool>/`, raw outputs to `results/logs/`, final poses to `results/poses/`, and the mandatory `results/DOCKING_RESULT.json`.

```bash
# 1. init
git init && git add . && git commit -m "canonical input + scaffold + compare package"

# 2. commit canonical input (already staged above); add structure when ready
git add input/canonical/targets/PahP.pdb input/canonical/binding_site/PahP_box.json
git commit -m "add PahP AlphaFold model + docking box"

# 3. FREEZE the input version (only after receptor+box exist)
git tag -a input-v1 -m "frozen shared docking input v1"
git push origin main --tags

# 4. create tool branches
for b in vina gold glide cb-dock unimol discovery-studio; do git branch dock/$b input-v1; done
git push origin --all

# 5. give branches to teams
#   each member: git clone <url>; git checkout dock/<tool>; git rev-parse --short HEAD  (= input_commit_hash)

# 6. collect results later
bash scripts/compare_results/collect_from_branches.sh          # pulls each branch's DOCKING_RESULT.json
python scripts/compare_results/compare.py reports/collected     # validate -> combine -> tables -> plots
```
(Teams may also open a Pull Request per branch instead of step 6's script — either works.)

## 8. Mandatory Result File Schema
**Filename:** `results/DOCKING_RESULT.json` (one per branch). JSON = easy to validate/merge. Schema in `scripts/compare_results/schema/DOCKING_RESULT.schema.json`; template + full example in `results/`.

**Required top-level:** `schema_version, tool_name, branch, team_members[], software_version, date_completed, input_commit_hash, target_id, receptor_prep_method, ligand_prep_method, docking_parameters{}, score_direction, results[]`. Optional: `hardware, runtime_total_sec, failed_cases[], warnings[], notes`.
**Each `results[]` row:** `ligand_id, pubchem_cid, docking_score, score_unit, rank_within_tool, pose_file, runtime_sec, status(ok|failed), failure_reason, notes`.

**Minimal valid example** (`schema/DOCKING_RESULT.minimal.example.json`) and **complete example** (`results/DOCKING_RESULT.example.json`) are in the repo.

**Validation rules:** `branch` starts `dock/`; `target_id` ∈ {PahP, PahS}; `date_completed` is YYYY-MM-DD; `score_direction` ∈ {lower_is_better, higher_is_better}; ≥1 result row; every `ok` row has a `rank_within_tool`. Run `validate_results.py` before committing.

**Common mistakes to avoid:** mixing tools in one file; leaving `input_commit_hash` blank (breaks reproducibility); omitting failed ligands instead of marking `status:"failed"`; wrong `score_direction`; comparing raw scores across tools.

> **Different tools produce scores with different meanings** (Vina kcal/mol vs GOLD ChemPLP vs GlideScore vs Uni-Mol confidence). The `score_direction` field + rank-based consensus are what make the comparison valid.

## 9. Python Comparison Package Design (`scripts/compare_results/`)
```
script: validate_results.py
purpose: validate DOCKING_RESULT files against the JSON schema (+ business checks)
input: a file or dir   output: pass/fail report, non-zero exit on failure
example: python validate_results.py reports/collected

script: combine_results.py
purpose: merge all results into one long table; recompute normalized_rank from score+direction
input: dir of result JSONs   output: reports/all_docking_results.csv
example: python combine_results.py reports/collected -o reports/all_docking_results.csv

script: make_tables.py
purpose: summary tables
input: all_docking_results.csv   output: best_score_per_tool.csv, consensus_ranking.csv,
        best_ligand_per_target.csv, runtime_comparison.csv, failure_summary.csv
example: python make_tables.py reports/all_docking_results.csv -o reports

script: make_plots.py
purpose: figures for the wiki
input: all_docking_results.csv   output: rank_heatmap_<target>.png, consensus_<target>.png, runtime.png
example: python make_plots.py reports/all_docking_results.csv -o reports/figures

script: compare.py
purpose: one-shot orchestrator (validate -> combine -> tables -> plots)
input: dir of collected results   output: everything in reports/
example: python compare.py reports/collected

helper: collect_from_branches.sh  -> pulls each dock/* branch's result into reports/collected/
schema/  -> DOCKING_RESULT.schema.json + minimal example
requirements.txt -> pandas, matplotlib, jsonschema, pyyaml, openpyxl
```
**Status: implemented and tested end-to-end** on 3 synthetic tools (Vina/GOLD/Glide, mixed score directions). Consensus correctly ranked benzo[a]pyrene #1 and the glucose negative control last across tools — confirming the direction-aware normalization works. (Excel export via openpyxl is a trivial add if you want `.xlsx` alongside CSV.)

## 10. Draft TEAM_INSTRUCTIONS.md
Written and in the repo root (`TEAM_INSTRUCTIONS.md`) — short enough to actually read: get your branch → use only `input/canonical/` → what you may/may not modify → produce & validate `DOCKING_RESULT.json` → report failures honestly → keep it fair (ranks not raw scores).

## 11. Immediate To-Do List for Ramin
1. **Create the GitHub repo** and push this scaffold (commands in §7). Decide private vs public (wiki is public later).
2. **Unblock the structure:** run **ColabFold on mature PahP** (after SignalP) → add `PahP.pdb` + `PahP_box.json` → tag `input-v1`. This is the only thing blocking everyone.
3. **Confirm the PAH panel** (currently 6 PAHs + control) — or trim to pyrene + 3 if you want it lighter.
4. **Confirm licences** (Glide/GOLD/Discovery Studio); assign the open Glide/GOLD slots and the Discovery Studio owner, or drop DS and add a free `dock/smina` branch.
5. **Send branches to the 6 teams** once `input-v1` is frozen.
6. (Optional) decide if PahS gets docked in v1 or waits for v2.

## 12. Blocking Questions for Ramin
1. **Structure go-ahead:** OK to generate the PahP AlphaFold model now, and who owns it? *(BLOCKED until answered.)*
2. **Licences:** which of Glide / GOLD / Discovery Studio does the team actually have? *(UNCERTAIN — you said details next prompt.)*
3. **PahP only, or PahP + PahS in v1?** *(UNCERTAIN — affects branch count and box prep.)*
4. **PAH panel final?** Keep 6+control, or reduce? *(UNCERTAIN.)*
5. **GitHub:** which account/org, and public or private for now? *(UNCERTAIN.)*
6. **Signal peptide:** confirm we dock the *mature* PahP (SignalP-cleaved), not the full 317 aa. *(LIKELY yes — confirm.)*
