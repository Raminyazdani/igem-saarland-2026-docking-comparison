# Current-data methods and results

## Materials and methods

Seven frozen task summaries are the sources. The analyses use the supplied reference, native instrument records, recorded microscopy, stored PAH calculations and declared model assumptions. All source statements retain their original analytical scope.

**C-06 — Reference coding sequence.** Format only LOCUS metadata spacing in memory; verify ORIGIN bases and raw-file hashes are unchanged. Extract the labelled CDS and translate with standard nuclear code 1; record adjacent stop separately. Derive weights from integer counts within full synonymous families; replace true zeros by 0.5; exclude Met, Trp and stops from CAI. Sensitivity: zero = 1.

**D-01 — Native plate-reader signals.** Decompress JSON and map values with the stored physical row/column indices. Summarize each GUID/gain separately. Plot independent native-value colour scales. No gain conversion, condition assignment, blank or OD correction.

**F-01 — Native microscopy and recording behavior.** Stream native frames; distinguish T,C,P,Z axes; cross-check ND2 timestamps against per-frame metadata. Use acquired event Z coordinates and cross-check optical stacks against Z index and planned positions. Whole-field native means are primary. Estimate spatial background outside BF-derived regions; keep raw means and a 10th-percentile background sensitivity.

**C-EX — Evidence review.** Preserve source result sentences verbatim; classify evidence type without scores or statistical tests. Compare the measured scope with the measurement each causal explanation requires.

**P-01 — Stored PAH calculations.** Recalculate ranks within tool and target; do not pool scoring scales. Summarize strict distance <0.5 nm over each finite trace and extract reported rescoring means/SD.

**P-02 — Conditional PAH models.** Analytical single-site occupancy and fixed-ligand approach to equilibrium. Source reporter ODE integrated by DOP853 (rtol 1e-8; atol 1e-10) on a one-minute output grid.

**V-01 — Conceptual calcium reporter.** Draw cpGFP, CaM and M13 as labelled conceptual domains. Show calcium-associated CaM-M13 interaction and emission under excitation. Export original SVG/PNG artwork and a looping GIF using the storyboard's presentation durations.

## Results

**C-06 — Reference coding sequence.** The labelled CDS spans reference bases 748-2097: 1350 nt and 450 aa; its translation matches its annotation. The adjacent triplet is TAA; a start-to-adjacent-stop segment has 1353 nt.

The 1350-nt reporter CDS encodes 450 amino acids and matches its annotated translation. Its yeast-reference CAI is 0.1708, compared with 0.1495 in the first 50 codons. There are 185 low-weight codon positions and 40 consecutive stretches of at least 2 codons, locating regions for a synonymous-redesign comparison.

**D-01 — Native plate-reader signals.** Recovered 150 readings across 3 distinct stored results, with 50 physical wells A1:E10 each. gain 2939: range 23036-260000, 29/50 entries equal 260000; gain 2976: range 27641-260000, 13/50 entries equal 260000; gain 933: range 22-3328, 0/50 entries equal 260000.

The three stored result sets contain 150 readings across wells A1-E10. Native signals vary across wells and gain settings. The exported readings and coordinates provide a reproducible numerical record of the plate measurements.

**F-01 — Native microscopy and recording behavior.** 120 input files, including derived context, were inventoried and byte-verified; 107 native/export image containers were processed. 20 time-series acquisitions; 14 with native clocks. All 146 static/Z frames are retained; 141 contain fluorescence and 94 have a usable BF-region metric.

13 October, nominal 10 mM Ca / 5 mM Cd: C8: +2.66 ADU over 298.2s; Empty: +0.12 ADU over 299.5s; C6: +15.01 ADU over 298.4s; C1: +0.57 ADU over 299.6s; C2: +0.77 ADU over 299.6s. The C6 recording has the largest within-recording increase in this group. Candidate field-matched pre/post contrasts are C1 -10.22 ADU; C2 +1.92 ADU; Empty +0.68 ADU. Within-recording change and the field-matched treatment contrast answer different questions: the C1 field decreases across its paired acquisitions despite rising slightly within the challenged recording.

**C-EX — Evidence review.** The review retains 7 F-01 findings and 4 C-06 findings verbatim in source_findings.csv. Recorded imaging findings from F-01: 13 October, nominal 10 mM Ca / 5 mM Cd: C8: +2.66 ADU over 298.2s; Empty: +0.12 ADU over 299.5s; C6: +15.01 ADU over 298.4s; C1: +0.57 ADU over 299.6s; C2: +0.77 ADU over 299.6s. The C6 recording has the largest within-recording increase in this group. Candidate field-matched pre/post contrasts are C1 -10.22 ADU; C2 +1.92 ADU; Empty +0.68 ADU. Within-recording change and the field-matched treatment contrast answer different questions: the C1 field decreases across its paired acquisitions despite rising slightly within the challenged recording.

The available imaging and reference analyses support a structured assessment of reporter behavior, technical conditions and reference codon composition. Low protein expression has not been identified as the cause of a weak response. Matched protein abundance, independent-culture identities and same-sample growth/viability measurements distinguish the remaining explanations.

**P-01 — Stored PAH calculations.** 35 docking scores; PahP first ranks: CB-Dock3: benzo_a_pyrene; Glide: anthracene; Vina: benzo_a_pyrene. Contact fractions: pyrene: 19.80%, 100.00%, 100.00%; phenanthrene: 8.00%, 99.68%, 21.13%.

The docking methods give different first-ranked PahP ligands (CB-Dock3: benzo_a_pyrene; Glide: anthracene; Vina: benzo_a_pyrene). Pocket-contact fractions in runs 1-3 are pyrene: 19.80%, 100.00%, 100.00%; phenanthrene: 8.00%, 99.68%, 21.13%. Pyrene has the higher contact fraction in each run, and the selected replicate-2 MM-GBSA means favour pyrene by 9.72 kcal/mol.

**P-02 — Conditional PAH models.** Model 1, Kd=L=100 nM: t95=24.9644 min. Reporter sampled maximum: 9.9333 simulated h; ideal pyrene ratio at 100 nM=1.1500.

At Kd = free ligand = 100 nM, the binding model gives t95 = 24.964 min. The reporter reaches its sampled maximum at 9.933 simulated hours. Fixed competitors shift pyrene half occupancy from 300.0 to 422.3 nM; mixture pyrene occupancy is 0.04522 and the unbound fraction is 0.67827.

**V-01 — Conceptual calcium reporter.** Created 3 panels and an animation lasting 12 presentation seconds per loop.

The completed visual presents calcium-associated CaM-M13 interaction and reporter emission in three panels. Editable SVG and PNG files accompany a GIF with a 12-second presentation loop.

## Figures

![Figure 1](F01_expanded_1.png)

Figure 1. From F-01: All native time-series traces; references and positions belong to individual recordings. No Cd-addition frame is assumed.

Underlying data: ../F-01/ (native trace and QC CSV tables)

![Figure 2](F01_expanded_2.png)

Figure 2. From F-01: Candidate same-field comparisons pass stage-distance and registered BF-correlation checks. Post values use initial/final 10% medians; the C2 calcium-conflict static file has a single post frame. C1/Empty comparisons change both calcium and cadmium labels; C2 R026 keeps nominal calcium at 1 mM. Field matching does not establish same-cell identity, equal exposure or addition time.

Underlying data: ../F-01/ (native trace and QC CSV tables)

![Figure 3](P01_contact.png)

Figure 3. From P-01: All six stored finite traces; dashed line is the strict 0.5 nm criterion. Run 1 initialization differs from runs 2–3.

Underlying data: ../P-01/distance_trace_plot_data.csv

## References and reproducibility

source_index.csv and figure_index.csv retain source hashes and attribution. result_index.csv contains every upstream result sentence. The original calculations and all code are in the standalone task notebooks.

- Sharp & Li (1987), doi:10.1093/nar/15.3.1281.
- Xia (2007), doi:10.1177/117693430700300028.
- EMBOSS CAI manual: https://emboss.sourceforge.net/apps/cvs/emboss/apps/cai.html
- Count source: https://sources.debian.org/data/main/e/emboss/6.6.0%2Bdfsg-15/emboss/data/CODONS/Eyeast_cai.cut
- Original VMR ProtocolResult fields and cadmium_experiment_notes.md: R-WET-12AUG-VOYAGER / R-WET-12AUG-LAYOUT.
- Chen et al. (2013), Ultrasensitive fluorescent proteins for imaging neuronal activity. https://doi.org/10.1038/nature12354
- Montero Llopis et al. (2021), Best practices and tools for reporting reproducible fluorescence microscopy methods. https://doi.org/10.1038/s41592-021-01156-w
- nd2 official documentation: https://talleylambert.com/nd2/
- scikit-image registration documentation: https://scikit-image.org/docs/stable/api/skimage.registration.html
- Nikon Perfect Focus System: near-infrared focus compensation maintains objective-to-coverslip position. https://www.microscope.healthcare.nikon.com/en_EU/resources/glossary/perfect-focus-system
- Supplied 13 October lab notebook, body.b0029 (condition table), b0037–b0069 (prior qualitative observations).
- Biomni methods review supplied in F01_biomni_methods_review.json; no arbitrary drift cutoff adopted.
- F-01 and C-06 frozen summaries: primary methods and references are preserved in those input JSON files.
- 13 October notebook context: CTX02-CTX06; original source hashes and locators in F01_context_review.json.
- https://github.com/Raminyazdani/igem-saarland-2026-docking-comparison/tree/3539358236841e3f95f3e9efdc6d954fe1a1eca2/tools/autodock-vina/md
- https://github.com/Raminyazdani/igem-saarland-2026-docking-comparison/tree/3539358236841e3f95f3e9efdc6d954fe1a1eca2/tools/autodock-vina/results
- https://github.com/Raminyazdani/igem-saarland-2026-docking-comparison/tree/04fd02b7d71f14314549e2e0887300ea54fd5035/tools
- https://github.com/Raminyazdani/igem-saarland-2026-docking-comparison/tree/3539358236841e3f95f3e9efdc6d954fe1a1eca2/tools/autodock-vina/md/models
- Stored source_assumptions.json: explicit source-derived parameter transcription; source hashes and complete parameters are in source_manifest.json.