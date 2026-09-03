# Preprocessing — Glide (Schrodinger)

**Goal of this step:** state *exactly* what preparation Glide (Schrodinger) needs to turn the shared canonical
inputs into something it can dock, and then do it reproducibly. This is deliberately separated from the
docking step so all six tools' recipes can be compared and, ideally, merged into one shared preprocessing.

Run it with [`preprocess.sh`](preprocess.sh) (needs `$SCHRODINGER` set and a Glide licence).
Structured manifest: [`PREPROCESSING.yaml`](PREPROCESSING.yaml).

## What the canonical receptor actually is

Checked before deciding anything, straight from `input/canonical/targets/PahP/structure.pdb`:

| property | value |
|---|---|
| atoms / residues | 4931 / 308, single chain A, contiguous 1–308 |
| hydrogens | already present (2509 H, added by OpenMM 8.5.2) |
| HETATM, waters, metals | none |
| altlocs / occupancies | none / all 1.00 |
| missing heavy atoms | none (0 incomplete residues) |
| chain breaks | none (no Cα–Cα gap > 4.5 Å) |
| cysteines | 2, **not** disulfide-bonded (SG–SG > 2.5 Å) |
| termini | C-terminal OXT present |

This is why the recipe below is short. Most of what a protein-prep checklist normally fixes (missing side
chains, missing loops, waters, alternate locations, het groups) simply is not present here.

## Narrative

### Receptor
- Source: `input/canonical/targets/PahP/structure.pdb` (primary target PahP).
- **Necessary for Glide:** (1) the file *must* become Maestro format — Glide's `RECEP_FILE` rejects PDB;
  (2) hydrogens must carry Schrodinger atom names, otherwise the H-bond network cannot be assigned;
  (3) protonation states at the canonical pH 7.4; (4) the restrained minimization that Glide's scoring
  function assumes, which is the step the Glide validation literature shows matters most.
- **What I did:** one `prepwizard` call —
  `-rehtreat` (delete the OpenMM hydrogens and re-add them; their non-Schrodinger names would otherwise
  break H-bond assignment), `-disulfides`, `-noepik` (no het groups to protonate), `-propka_pH 7.4`,
  `-f OPLS_2005`, keeping the default restrained minimization (0.3 Å RMSD).
- **What I deliberately did not do:** `-fillsidechains` and `-fillloops`. The model has no missing heavy
  atoms and no chain breaks, so they would only introduce Prime-dependent changes (and `-fillloops`
  reserves 8 PSP_PLOP tokens whether or not anything is missing).

### Ligands
- Source: `input/canonical/ligands/ligands.sdf` — 7 molecules, all neutral, all with explicit hydrogens,
  RDKit 3D. Six are rigid PAHs (0 rotatable bonds); `glucose_NEGCTRL` is the flexible control.
- **Necessary for Glide:** conversion to Maestro with Schrodinger atom typing. Essentially nothing else:
  the six PAHs have no ionizable group and no tautomer at pH 7 ± 2, so ionization and tautomer
  enumeration are genuine no-ops for them.
- **Did I keep the canonical 3D conformers?** Yes —
  `ligprep -i 0 -nt -s 1 -g` = no ionization/neutralization, tautomerizer off (it is **on** by default),
  one stereoisomer, chirality read from the input 3D geometry. This is the documented "adjust only the
  geometry" recipe and gives exactly 7 output structures, one per canonical ligand.
- **The one unavoidable change:** LigPrep's final `bmin` stage always perturbs and re-minimizes
  coordinates, so the docked geometry is not bit-identical to the canonical SDF. There is no flag to
  disable it. Chemistry, stereochemistry and protonation are untouched.
- The asymmetry is worth stating: this prep is a no-op *chemically* for the six PAHs, but glucose has
  five stereocentres and several anomeric/tautomeric forms, so `-s 1 -g` is doing real work there —
  it pins glucose to exactly the canonical anomer instead of enumerating alternatives.

### Binding site / box
- Source: `input/canonical/targets/PahP/binding_site.yaml` → **still a PLACEHOLDER**: `status: PLACEHOLDER`
  and all six numbers `null`. No `input-v1` tag exists in the repo either.
- **Glide cannot work around this.** It has no blind-docking mode: a receptor grid needs an explicit
  centre, and the ligand-centroid search box is capped near 14 Å. Whole-protein docking is not an option.
- `preprocess.sh` reads the canonical box first and uses it whenever it is defined. While it is null it
  falls back to the box in `configurations/config.yaml`, printing a warning on every run. That fallback
  is **the box the AutoDock Vina team derived with fpocket 4.2.2 (Pocket 4) and proposed for the shared
  `binding_site.yaml`** — centre `70.83, 71.96, 59.18`. Using their box is the point: it is what makes
  the tools comparable, and it is not a choice made to improve scores.
- It is independently corroborated three ways: all 7 CB-Dock3 blind-docking poses on PahP land
  0.8–2.1 Å from that centre; a clearance scan of the canonical structure finds 24.8% of the inner box
  free of protein there (nearest heavy atom 3.48 Å); and the site is lined by 16 residues, 62%
  hydrophobic, with five aromatics for π-stacking (Phe123, Tyr271, Tyr274, Phe275, Phe306).
- **Box translation.** Vina's box becomes Glide's `OUTERBOX` (`21.3, 19.6, 27.3`) so the enclosed volume
  matches. `INNERBOX` is **8 Å**, not the usual 10: the inner box bounds only the ligand *centroid*, and
  Glide requires `outer ≥ inner + longest ligand` on every axis. The shortest axis is 19.6 Å and
  benzo[a]pyrene is 11.46 Å, so 8 is the largest legal value (8 + 11.46 = 19.46 ≤ 19.6). `preprocess.sh`
  checks this per axis and refuses to build a grid that would silently clip the biggest ligand.

### A wrong turn worth recording
An earlier version of this workspace centred the grid on the **centroid of the six published pocket
residues** from *iScience* 2023, 26:107912 (which map onto our structure as Tyr32, Leu125, Ala200,
Tyr205, Phe227, Leu244 — a 6/6 identity match at offset −1). That was **wrong**, and the failure mode is
instructive: the centroid of a ring of residues is not the same thing as the cavity they enclose. It fell
1.71 Å from Asp201 OD2, i.e. *inside* protein density, with only 2% of the inner box free. Three ligands
could not be posed at all and the other four were pushed 11.5–15.0 Å out onto the surface, where the
polar glucose control outscored every PAH. The residue mapping itself was probably fine — Leu244 also
lines the fpocket-4 site — but a box centre must be validated against actual free volume before use.

## For the coordinators — two decisions needed

1. **The canonical receptor still contains its signal peptide.** `structure.pdb` covers residues 10–317
   of `sequence.fasta`, i.e. only 9 residues were trimmed, so the hydrophobic stretch
   `FYSVYLAVALLLMPLPLLAQ` (model residues 1–20) is still in the model. Both `target_metadata.csv`
   ("Remove N-terminal signal peptide -> dock mature domain") and `reports/DOCKING_WORKFLOW_PLAN.md`
   §6/§12-Q6 call for the *mature* domain. The receptor was not changed here — it must stay identical
   across tools — and the CB-Dock3 team independently flagged the same thing.

2. **The binding box needs freezing, and there is now a concrete candidate.** The AutoDock Vina team's
   fpocket Pocket 4 box (centre `70.83, 71.96, 59.18`, size `21.3, 19.6, 27.3`) is what this workspace
   uses, and CB-Dock3's blind docking independently lands on it. Writing it into
   `input/canonical/targets/PahP/binding_site.yaml` and tagging `input-v1` would make the comparison
   provably fair. Until then every tool re-derives it, and two tools have already recorded a stale
   `input_commit_hash` (`6564a76`, which predates the commit that added the real structures — the
   correct value is `fad5b9b`).

## Fairness reminder
Change as little as possible from the canonical inputs. Where a tool *forces* a change, record it under
`assumptions_and_deviations` in `PREPROCESSING.yaml` with the reason — those deviations are exactly what we
need to reconcile when designing the shared preprocessing.
