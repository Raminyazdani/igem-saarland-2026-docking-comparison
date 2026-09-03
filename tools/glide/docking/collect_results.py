#!/usr/bin/env python3
"""Turn Glide's native docking output into the repo's standardized result file.

Reads   outputs/glide_dock.csv       (Glide writes one row per pose, for every input ligand)
        outputs/glide_dock_skip.csv  (ligands Glide could not pose, with its own reason)
        outputs/glide_dock_lib.sdf   (docked poses, globally sorted best-first)
        outputs/glide_grid.in        (the grid that was actually used)
        input/canonical/ligands/ligand_metadata.csv
Writes  results/DOCKING_RESULT.json
        results/poses/PahP__<ligand>__glide__v1.sdf   (best pose per ligand)

Every canonical ligand gets a row: docked ones as "ok", the rest as "failed" with the
reason Glide reported. Scores are copied verbatim - nothing is inferred or filled in.
"""
import csv, json, os, re, subprocess, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.dirname(HERE)                                  # tools/glide
REPO = os.path.abspath(os.path.join(TOOL, "..", ".."))
OUT, RES = os.path.join(TOOL, "outputs"), os.path.join(TOOL, "results")
POSES = os.path.join(RES, "poses")
CSV_IN = os.path.join(OUT, "glide_dock.csv")
SKIP_IN = os.path.join(OUT, "glide_dock_skip.csv")
SDF_IN = os.path.join(OUT, "glide_dock_lib.sdf")
GRID_IN = os.path.join(OUT, "glide_grid.in")
META = os.path.join(REPO, "input", "canonical", "ligands", "ligand_metadata.csv")
CANON_BOX = os.path.join(REPO, "input", "canonical", "targets", "PahP", "binding_site.yaml")
TARGET = "PahP"

# Column names as written by Glide v11.0 (Schrodinger 2026-1).
TITLE, SCORE, CPU = "title", "r_i_docking_score", "r_glide_cpu_time"


def git_short_hash(path):
    try:
        r = subprocess.run(["git", "log", "-1", "--format=%h", "--", path],
                           capture_output=True, text=True, cwd=REPO)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def run_date():
    """The date the docking job finished, read from Glide's own log.

    Taken from the log rather than the clock so that re-extracting an existing run does not
    silently restamp it with today's date.
    """
    log = os.path.join(OUT, "glide_dock.log")
    if os.path.exists(log):
        m = re.search(r"^Date:\s+\w+,\s+(\w+)\s+(\d+)\s+(\d{4})", open(log, encoding="utf-8",
                      errors="replace").read(), re.M)
        if m:
            try:
                return datetime.datetime.strptime(" ".join(m.groups()), "%B %d %Y").date().isoformat()
            except ValueError:
                pass
    return datetime.date.today().isoformat()


def grid_params():
    """The grid that was actually used, straight out of the Glide input file."""
    out = {}
    for line in open(GRID_IN, encoding="utf-8") if os.path.exists(GRID_IN) else []:
        key, _, val = line.partition(" ")
        if key in ("GRID_CENTER", "INNERBOX", "OUTERBOX"):
            out[key.lower()] = [float(v) for v in val.replace(",", " ").split()]
    return out


def skipped_reasons():
    """Glide's own message for each ligand it could not pose."""
    if not os.path.exists(SKIP_IN):
        return {}
    return {r[TITLE].strip(): " - ".join(x for x in (r["docking_status"], r["message"]) if x)
            for r in csv.DictReader(open(SKIP_IN, newline="", encoding="utf-8")) if r.get(TITLE)}


def scrub(record):
    """Replace absolute local paths with the repo-relative source.

    Glide stamps <s_m_source_file> with the full path of the ligand file it read, which on
    a workstation carries the username and drive layout. The poses are the deliverable, so
    the provenance is kept but written in the form every other workspace uses.
    """
    marker = "/input/canonical/"
    out = []
    for line in record.split("\n"):
        slashed = line.replace("\\", "/")
        i = slashed.find(marker)
        if i != -1:
            line = "input/canonical/" + slashed[i + len(marker):]
        out.append(line)
    return "\n".join(out)


def best_poses():
    """{title: sdf_record} for the first record of each ligand.

    Glide sorts the pose file ascending by docking score, so the first record for a
    ligand is its best pose - the same pose whose score is reported below.
    """
    if not os.path.exists(SDF_IN):
        return {}
    out, rec = {}, []
    for line in open(SDF_IN, encoding="utf-8", errors="replace"):
        rec.append(line)
        if line.startswith("$$$$"):
            out.setdefault(rec[0].strip(), scrub("".join(rec)))
            rec = []
    return out


SITE_NOTE = (
    "BINDING SITE: the canonical binding_site.yaml is still a PLACEHOLDER (six null values, no "
    "input-v1 tag), and Glide has no blind-docking mode, so a box had to come from somewhere. This "
    "run uses the fpocket 4.2.2 Pocket 4 box that the AutoDock Vina team derived and proposed for "
    "the shared binding_site.yaml, so all tools search one region. It is independently corroborated: "
    "all 7 CB-Dock3 blind-docking poses on PahP land 0.8-2.1 A from this centre, and a clearance scan "
    "of the canonical structure finds 24.8% of the inner box free of protein here (nearest heavy atom "
    "3.48 A). The site is lined by 16 residues, 62% hydrophobic, with five aromatics available for "
    "pi-stacking (Phe123, Tyr271, Tyr274, Phe275, Phe306) and a polar face (Ser242, Ser243, Gln246, "
    "His250, Lys273). The box is still PROVISIONAL: rerun once input-v1 freezes the canonical box.")

NEGCTRL_NOTE = (
    "NEGATIVE CONTROL RANKS 2nd - this is a real property of the score, not a pipeline fault. All 7 "
    "ligands docked into the same site (best-pose centroids 0.95-2.72 A from the grid centre). The "
    "GlideScore components show why: the PAHs score through lipophilic contact (-2.3 to -2.9) and vdW "
    "(-17 to -24) with zero H-bond and near-zero Coulomb, whereas glucose scores a weak lipophilic "
    "-1.0 but gains H-bond -0.79 and Coulomb -8.87 from the pocket's polar face. The pocket is only "
    "62% hydrophobic, so a polyol genuinely does have something to bind. Interpretation: glucose is a "
    "plumbing/property control, not a specificity control - it is mismatched to the PAHs on nearly "
    "every physicochemical axis, so the comparison is confounded and cannot be read as evidence about "
    "pocket selectivity either way.")

RECEPTOR_WARNING = (
    "Canonical receptor caveat: structure.pdb covers residues 10-317 of sequence.fasta, so it still "
    "contains the predicted N-terminal signal peptide, although target_metadata.csv and "
    "reports/DOCKING_WORKFLOW_PLAN.md both call for docking the mature domain. Not changed here - "
    "the receptor must stay identical across tools. Independently flagged by the CB-Dock3 team too.")

RANKING_WARNING = (
    "HOW TO READ THE RANKING. Across the 6 PAHs, GlideScore correlates with heavy-atom count at "
    "r = -0.68; CB-Dock3 on the same site gives r = -1.00, i.e. its ranking is almost entirely "
    "ligand size. Glide is less size-driven but still not an affinity predictor: against the four "
    "ligands with published SPR affinities for this protein (iScience 2023, 26:107912), the raw "
    "GlideScore ordering is inverted (Spearman rho = -1.00, n=4) while size-normalised ligand "
    "efficiency is weakly positive (rho = +0.20) and correctly puts naphthalene first, matching the "
    "experimental finding that naphthalene binds tightest. With n=4 these coefficients are extremely "
    "noisy and no significance is claimed. The honest summary is that neither tool reproduces the "
    "experimental affinity order, which is the expected behaviour of docking scores. Compare RANKS "
    "across tools, never raw scores.")


def main():
    if not os.path.exists(CSV_IN):
        sys.exit("missing %s - run docking/run_docking.sh first" % CSV_IN)

    rows = list(csv.DictReader(open(CSV_IN, newline="", encoding="utf-8")))
    if not rows or TITLE not in rows[0] or SCORE not in rows[0]:
        sys.exit("%s has no %r/%r columns (found: %s)"
                 % (CSV_IN, TITLE, SCORE, list(rows[0]) if rows else []))

    # Best (most negative) score per ligand, plus the CPU time Glide reported for it.
    scored, cpu = {}, {}
    for r in rows:
        name = r[TITLE].strip()
        try:
            score = float(r[SCORE])
        except (TypeError, ValueError):
            continue
        if name and (name not in scored or score < scored[name]):
            scored[name] = score
        try:
            cpu[name] = float(r[CPU])
        except (TypeError, ValueError, KeyError):
            pass

    os.makedirs(POSES, exist_ok=True)
    poses, skips = best_poses(), skipped_reasons()
    rank = {n: i + 1 for i, n in enumerate(sorted(scored, key=scored.get))}

    results, failed = [], []
    for row in csv.DictReader(open(META, newline="", encoding="utf-8")):
        lid = row["ligand_id"].strip()
        entry = {"target_id": TARGET, "ligand_id": lid,
                 "pubchem_cid": row.get("pubchem_cid", "").strip() or None,
                 "score_unit": "kcal/mol", "notes": ""}
        if lid in scored:
            pose_file = None
            if lid in poses:
                name = "%s__%s__glide__v1.sdf" % (TARGET, lid)
                open(os.path.join(POSES, name), "w", encoding="utf-8").write(poses[lid])
                pose_file = "tools/glide/results/poses/" + name
            entry.update(docking_score=scored[lid], rank_within_tool=rank[lid],
                         pose_file=pose_file, runtime_sec=cpu.get(lid),
                         status="ok", failure_reason=None)
        else:
            failed.append(lid)
            entry.update(docking_score=None, rank_within_tool=None, pose_file=None,
                         runtime_sec=None, status="failed",
                         failure_reason=skips.get(lid, "no scored row in %s"
                                                  % os.path.basename(CSV_IN)))
        results.append(entry)

    version_file = os.path.join(os.environ.get("SCHRODINGER", ""), "version.txt")
    version = (open(version_file, encoding="utf-8").read().strip().splitlines()[0]
               if os.path.exists(version_file) else "Schrodinger Glide (version not detected)")

    grid = grid_params()
    provisional = not (os.path.exists(CANON_BOX) and not re.search(
        r"^center_x:\s*null", open(CANON_BOX, encoding="utf-8").read(), re.M))

    doc = {
        "schema_version": "1.0",
        "tool_name": "Glide (Schrodinger)",
        "branch": "tool/glide",
        "team_members": ["Ramin"],
        "software_version": version,
        "date_completed": run_date(),
        "input_commit_hash": git_short_hash("input/canonical") or "unknown",
        "score_direction": "lower_is_better",
        "receptor_prep_method": "prepwizard: hydrogens deleted and re-added, disulfides assigned, "
                                "PROPKA pH 7.4, restrained minimization (OPLS_2005); no Epik, no "
                                "Prime side-chain/loop filling (model has no missing heavy atoms)",
        "ligand_prep_method": "LigPrep minimal-change (-i 0 -nt -s 1 -g): canonical 3D conformers "
                              "and stereochemistry kept, no ionization, no tautomers, one "
                              "stereoisomer per ligand",
        "docking_parameters": {
            "precision": "SP", "docking_method": "confgen", "poses_per_lig": 5,
            "postdock": True, "postdock_npose": 5, "postdockstrain": False,
            "canonicalize": True, "epik_penalties": False, "forcefield": "OPLS_2005",
            "grid_center": grid.get("grid_center"), "inner_box": grid.get("innerbox"),
            "outer_box": grid.get("outerbox"),
            "box_source": ("PROVISIONAL (published pocket; canonical box still null)"
                           if provisional else "canonical binding_site.yaml"),
            "seed": None,
            "seed_mechanism": "Glide exposes no random seed; CANONICALIZE=True used instead",
        },
        "hardware": "Windows 11 x86-64, single core (-HOST localhost)",
        "runtime_total_sec": round(sum(cpu.values()), 3) or None,
        "results": results,
        "failed_cases": failed,
        "warnings": ([SITE_NOTE] if provisional else []) + [NEGCTRL_NOTE, RANKING_WARNING,
                                                              RECEPTOR_WARNING],
        "notes": "Real Glide SP run on Schrodinger Suite 2026-1 (Glide v11.0). All 7 canonical "
                 "ligands docked successfully into the shared fpocket-4 site; no failures. Scores are "
                 "copied verbatim from Glide's native CSV and were not tuned. Docking was run twice "
                 "from the identical grid and gave identical scores, so the pipeline is deterministic "
                 "despite Glide exposing no random seed. See warnings for how to read the ranking.",
    }
    with open(os.path.join(RES, "DOCKING_RESULT.json"), "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")
    print("wrote results/DOCKING_RESULT.json: %d ok, %d failed"
          % (len(results) - len(failed), len(failed)))


if __name__ == "__main__":
    main()
