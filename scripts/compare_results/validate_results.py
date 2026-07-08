#!/usr/bin/env python3
"""Validate one or more DOCKING_RESULT.json files against the JSON schema + business rules.

Usage:
    python validate_results.py [file-or-dir ...]      # default: results/

Exit code 0 if every file passes (no ERRORs), 1 otherwise. WARNINGs never fail the run.

ERRORs  = schema violations + hard business rules (Section 10 of the build plan).
WARNINGs = missing ligands, pose file not on disk, commit-hash mismatch, failed id not listed.
"""
import sys, os, json, csv, glob, subprocess

try:
    from jsonschema import Draft7Validator
except ImportError:
    sys.exit("Missing dependency: pip install jsonschema")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SCHEMA_PATH = os.path.join(HERE, "schema", "DOCKING_RESULT.schema.json")
LIGAND_META = os.path.join(REPO_ROOT, "input", "canonical", "ligands", "ligand_metadata.csv")
POSE_MARKER = "results/poses/"   # poses live under tools/<tool>/results/poses/ (or a top-level results/poses/)


def load_schema():
    return Draft7Validator(json.load(open(SCHEMA_PATH, encoding="utf-8")))


def known_ligands():
    """Set of ligand_ids from the canonical metadata (empty set if file missing)."""
    if not os.path.exists(LIGAND_META):
        return set()
    with open(LIGAND_META, newline="", encoding="utf-8") as fh:
        return {row["ligand_id"].strip() for row in csv.DictReader(fh) if row.get("ligand_id")}


def frozen_input_hash():
    """Short hash of the input-v1 git tag, or None if not resolvable (repo not tagged yet)."""
    try:
        out = subprocess.run(["git", "-C", REPO_ROOT, "rev-parse", "--short", "input-v1"],
                             capture_output=True, text=True)
        return out.stdout.strip() if out.returncode == 0 else None
    except Exception:
        return None


def iter_result_files(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            files += glob.glob(os.path.join(p, "**", "*DOCKING_RESULT*.json"), recursive=True)
        elif p.endswith(".json"):
            files.append(p)
    return sorted({f for f in files if "template" not in os.path.basename(f).lower()})


def validate_one(doc, validator, ligands, tag_hash):
    """Return (errors, warnings) lists of human-readable strings."""
    errors, warnings = [], []

    # 1. JSON schema
    for e in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
        loc = "/".join(str(x) for x in e.path) or "(root)"
        errors.append(f"schema: {loc}: {e.message}")
    if errors:
        return errors, warnings  # don't pile business rules on a structurally broken file

    # 9/10. commit hash present + optional match to frozen tag
    commit = doc.get("input_commit_hash", "")
    if tag_hash and commit and not (commit.startswith(tag_hash) or tag_hash.startswith(commit)):
        warnings.append(f"input_commit_hash {commit!r} != frozen input-v1 tag {tag_hash!r}")

    seen_by_target = {}          # target_id -> set(ligand_id) for the missing-ligand check
    failed_cases = set(doc.get("failed_cases", []))

    for i, r in enumerate(doc.get("results", [])):
        tag = f"results[{i}] ({r.get('target_id')}/{r.get('ligand_id')})"
        status = r.get("status")
        lig = r.get("ligand_id")
        seen_by_target.setdefault(r.get("target_id"), set()).add(lig)

        # unknown ligand -> ERROR (only when we actually have the metadata)
        if ligands and lig not in ligands:
            errors.append(f"{tag}: ligand_id not in ligand_metadata.csv")

        if status == "ok":
            if r.get("rank_within_tool") is None:
                errors.append(f"{tag}: ok row missing rank_within_tool")
            if not (r.get("score_unit") or "").strip():
                errors.append(f"{tag}: ok row has empty score_unit")
            pose = r.get("pose_file")
            if not pose:
                errors.append(f"{tag}: ok row has empty pose_file")
            else:
                norm = pose.replace("\\", "/")
                if POSE_MARKER not in norm:
                    errors.append(f"{tag}: pose_file must live under a {POSE_MARKER} folder (got {pose!r})")
                elif not os.path.exists(os.path.join(REPO_ROOT, norm)):
                    warnings.append(f"{tag}: pose_file not found on disk ({pose})")

        elif status == "failed":
            if not r.get("failure_reason"):
                errors.append(f"{tag}: failed row needs a non-null failure_reason")
            if lig not in failed_cases:
                warnings.append(f"{tag}: failed ligand {lig!r} not listed in failed_cases[]")

    # 6. every canonical ligand attempted once per target -> WARN if missing
    if ligands:
        for target, seen in seen_by_target.items():
            missing = sorted(ligands - seen)
            if missing:
                warnings.append(f"target {target}: ligands not attempted: {', '.join(missing)}")

    return errors, warnings


def main(argv):
    paths = argv or ["results"]
    files = iter_result_files(paths)
    if not files:
        sys.exit("no DOCKING_RESULT*.json found (looked in: %s)" % ", ".join(paths))

    validator = load_schema()
    ligands = known_ligands()
    tag_hash = frozen_input_hash()
    if not ligands:
        print(f"(note: {LIGAND_META} not found - skipping ligand-membership checks)")

    n_bad = 0
    for f in files:
        rel = os.path.relpath(f, REPO_ROOT)
        try:
            doc = json.load(open(f, encoding="utf-8"))
        except Exception as e:
            print(f"[FAIL] {rel}: not valid JSON -> {e}")
            n_bad += 1
            continue
        errors, warnings = validate_one(doc, validator, ligands, tag_hash)
        if errors:
            n_bad += 1
            print(f"[FAIL] {rel}  tool={doc.get('tool_name')}  n={len(doc.get('results', []))}")
            for m in errors:
                print(f"    ERROR: {m}")
            for m in warnings:
                print(f"    warn:  {m}")
        else:
            tail = f"  ({len(warnings)} warning(s))" if warnings else ""
            print(f"[ OK ] {rel}  tool={doc.get('tool_name')}  n={len(doc.get('results', []))}{tail}")
            for m in warnings:
                print(f"    warn:  {m}")

    print(f"\n{len(files) - n_bad}/{len(files)} file(s) passed")
    sys.exit(1 if n_bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
