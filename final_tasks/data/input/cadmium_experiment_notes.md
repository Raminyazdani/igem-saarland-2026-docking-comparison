# Task-focused evidence from the existing memory

Prepared 16 October 2026. These are curated copies of existing evidence notes, not new measurements. Original source IDs and structural locators are retained below. References to prior codon reports in the historical memory are superseded: the user now assumes a fresh audit with no previous analysis.

---

## Memory source: R-WET-12AUG-LAYOUT

Source memory file: `E:/igem/igem_task_digest_2026-10-16/02_TASK_MEMORY/resources/R-WET-12AUG-LAYOUT.md`

### R-WET-12AUG-LAYOUT — 12 August cadmium and calcium experiment record


## Evidence and provenance

- SRC002 · [original] · body.b0195–body.b0215
- SRC007 · Protocols and Lab Notebook/Shared Lab Notebook.docx · body.b0195–body.b0215

## Extracted evidence

- Notebook dates the exposure entry 12 August and names Jasmine, Ruiqi and Edison.
- Cadmium table labels S1/S2/S3 at plate rows A/B/C and Cont. at D; concentration headings label plate columns 2–10 as 0.0267, 0.089, 0.178, 0.445, 1.78, 4.45, 17.79, 44.48, 88.96 µM; column 11 is a dash.
- Calcium table labels S1/S2/S3 at rows B/C/D and Cont. at E; its headings are 0.5–10.0 mM at plate columns 2–10.
- Control annotation explicitly says non-transformed cells in YPD, with remaining cells in SC-Ura. Notebook mentions observation by confocal microscope and Tecan plate reader.

## Available inputs

- Dated experiment entry; dose/control candidate map; named custodians

## Missing or unverified inputs

- Authoritative as-executed plate map; clone identities behind S1/S2/S3; instrument/export linkage; same-run OD and blanks; culture/batch mapping

## Limits and uncertainty

- Layouts are documented methods, not validated assignments of every instrument well.
- S1/S2/S3 identities and independent cultures are not resolved; no explicit sensor 0 µM control identity.
- Notebook plate reader brand mention Tecan conflicts with supplied BMG Voyager files; instrument/run linkage requires confirmation.
- Notebook cadmium concentration headings omit 8.90 and 0.89 µM that occur in the workbook; controls and media are not matched by assumption.

---

## Memory source: R-WET-12AUG-VOYAGER

Source memory file: `E:/igem/igem_task_digest_2026-10-16/02_TASK_MEMORY/resources/R-WET-12AUG-VOYAGER.md`

### R-WET-12AUG-VOYAGER — Three accessible 12 August fluorescence result files


## Evidence and provenance

- SRC007 · Data well plate reader/12082026/iGEM Test1 2026-08-12 17-44-05autogained cadmium.vmr · $[0].ProtocolResult
- SRC007 · Data well plate reader/12082026/iGEM Test1 2026-08-12 17-44-05gaincorrectedFisempty.vmr · $[0].ProtocolResult
- SRC007 · Data well plate reader/12082026/iGEM Test1 2026-08-12 17-44-05gained933 cadmium.vmr · $[0].ProtocolResult
- SRC007 · Data well plate reader/12082026/iGEM Calcium GFP.vwp · $[0]

## Extracted evidence

- All three VMR files decode as gzip containing a JSON value plus a hexadecimal trailer. Each result has 50 completed/expected measurement entries, Cycles=1, Chromatics=1, Fluorescence, and explicit row/column arrays spanning A1:E10.
- Result data reside at $[0].ProtocolResult.WorkflowPlan.WorkflowStatements[0].Data.Data; matched row/column arrays are under the same Data object.
- Filename autogained: ProtocolResult Guid 44c70734-f083-483c-90f7-eca669518e7c; UtcDateTime 2026-08-12T16:11:22.0386233Z; AdjustedGain Value 2939.
- Filename gaincorrectedFisempty: Guid 8d04e45f-8447-4530-a97e-3e6a6de61c7c; UtcDateTime 2026-08-12T15:44:05.6743455Z; AdjustedGain Value 2976.
- Filename gained933: Guid bc4aa3cb-e29e-49df-9755-826a2c57f28a; UtcDateTime 2026-08-12T16:16:22.2734998Z; FixedGain Value 933.
- All have reader serial 430-004882, GFP preset, BottomChannel, raw excitation wavelength field 4700 and emission field 5150. These raw encoded fields are not silently converted to nm.
- The autogained and gaincorrected arrays contain repeated literal values 260000; their scientific interpretation has not been established.
- The VWP contains a protocol, not an additional measured dataset.

## Available inputs

- Three original numeric fluorescence arrays; row/column indices; run IDs/timestamps; method/gain metadata; protocol

## Missing or unverified inputs

- Authoritative file-to-experiment match; physical well/dose/control map; gain calibration and overload meaning; blank and 0 µM identities; same-well same-time OD; biological replicate identities; any missing runs

## Limits and uncertainty

- Raw numeric presence now verified, superseding the master report access-level uncertainty; no background correction, dose response, power or threshold has been calculated.
- The three files are distinct result IDs/times, not assumed technical or biological replicates.
- Result layouts use generic Sample content and zero-valued concentration fields, without biological condition labels; filename wording does not prove processing or cell identity.
- 50-well A1:E10 instrument footprint does not directly equal notebook plate columns 2–10/11 dose layout. Reconcile before joining.
- Gain values differ. Do not combine or subtract across gains without validated calibration.
- No OD measurement channel is identified in these files. Hexadecimal trailer is retained but its vendor checksum semantics are unverified.

---

## Memory source: R-WET-CADMIUM-WORKBOOK

Source memory file: `E:/igem/igem_task_digest_2026-10-16/02_TASK_MEMORY/resources/R-WET-CADMIUM-WORKBOOK.md`

### R-WET-CADMIUM-WORKBOOK — Dose planning workbook and source inconsistencies


## Evidence and provenance

- SRC007 · Protocols and Lab Notebook/Concentrations cadmuim exposure experiment 12-08.xlsb · sheet.Pipetting scheme.R16C2–R27C8
- SRC007 · Protocols and Lab Notebook/Concentrations cadmuim exposure experiment 12-08.xlsb · sheet.detection limits.R3C2–R16C4

## Extracted evidence

- Workbook Pipetting scheme!E17:E27 lists Cd µM values 88.96, 44.48, 17.79, 8.90, 4.45, 1.78, 0.89, 0.445, 0.178, 0.089, 0.0267, with stock and yeast volume columns.
- The calcium list at Pipetting scheme!C4:C13 includes 1.5 mM, which is absent from the notebook calcium table.
- Headers C16 and D16 label mg/L and µg/L, but top corresponding rows contain identical literal entries (for example C17=D17=10). H27 is the literal value 99733.0 under yeast (µL).
- The detection limits sheet contains PahP/PahS Kd and environmental-threshold tables; these are unattributed workbook entries, not team assay measurements.

## Available inputs

- Structured dose, stock, volume and reference-table cells with exact locators

## Missing or unverified inputs

- Version/as-executed dosing confirmation; correction of ambiguous units and 99733 values; provenance for literature Kd/reference thresholds

## Limits and uncertainty

- No formulas were recalculated or source values corrected.
- Sheet labels describe planning/reference content; workbook does not establish observed Cd fluorescence or a measured detection limit.
- Notebook/workbook concentration omissions, unit-label conflicts and anomalous volume values require authoritative correction before analysis.

---

## Memory source: R-WET-17SEP-PLAN

Source memory file: `E:/igem/igem_task_digest_2026-10-16/02_TASK_MEMORY/resources/R-WET-17SEP-PLAN.md`

### R-WET-17SEP-PLAN — 17 September calcium and cadmium comparison plan


## Evidence and provenance

- SRC007 · Protocols and Lab Notebook/Concentrations cadmuim exposure experiment 12-08.xlsb · sheet.pippeting sheme for 17-09.R1C2–R22C18
- SRC007 · Protocols and Lab Notebook/Concentrations cadmuim exposure experiment 12-08.xlsb · sheet.Well plate distribution 17-09.R2C3–R10C2

## Extracted evidence

- Plan labels piGEM005 C5, empty vector and empty cells, with and without calcium.
- Sensor: B2/B3/B4 with calcium, B6/B7/B8 without; empty vector: C2/C3/C4 and C6/C7/C8; empty cells: D2/D3/D4 and D6/D7/D8.
- Each trio is labelled 0.0267, 1.78 and 88.96 µM Cd.

## Available inputs

- Condition and well-map candidate for a separate 17 September run

## Missing or unverified inputs

- Whether executed; actual run IDs/files; as-executed dose/volume corrections; calcium level/timing; replicate mapping

## Limits and uncertainty

- This is a plan; no corresponding dated 17 September numeric fluorescence dataset was identified in the supplied batch.
- Calcium final dose and exact timing need confirmation. Lowest-dose yeast-volume cells again contain 99733.0.
- Do not use this later plan to relabel 12 August VMR results or to infer biological replicates.

---

## Memory source: R-WET-08OCT-BASELINE

Source memory file: `E:/igem/igem_task_digest_2026-10-16/02_TASK_MEMORY/resources/R-WET-08OCT-BASELINE.md`

### R-WET-08OCT-BASELINE — 8 October GCaMP-cell baseline fluorescence design


## Evidence and provenance

- SRC002 · [original] · body.b0623–body.b0630; word/media/image17.png
- SRC007 · Protocols and Lab Notebook/Shared Lab Notebook.docx · body.b0623–body.b0630; word/media/image17.png

## Extracted evidence

- Notebook calls the entry kinetic GFP signal measurement on 8 October: 200 µL water/SD-Ura/culture diluted to OD 0.2; Ex 480/Em 530; Gain 80; Z position 30000; every 30 minutes.
- Embedded plate map visually verified: Date 2026-10-08, Exp ID GCaMP-cell; columns 1–3 are A H2O, B SD-Ura, C vfree, D c1, E c2, F c6, G c8.
- The image shows three wells per group.

## Available inputs

- Baseline group/well design, optical settings and target starting OD

## Missing or unverified inputs

- Matching 8 October raw kinetic RFU; actual OD by well/time; culture mapping; control identity; sample handling/timing

## Limits and uncertainty

- No Cd dose labels in this run design; it is not established as a Cd concentration series.
- vfree requires exact empty-vector/control definition; three wells do not establish three independent cultures.
- No matching 8 October raw RFU export was found in supplied files; do not transplant Gain 80 to 12 August Voyager runs.

---

## Memory source: R-WET-EXPRESSION-OD

Source memory file: `E:/igem/igem_task_digest_2026-10-16/02_TASK_MEMORY/resources/R-WET-EXPRESSION-OD.md`

### R-WET-EXPRESSION-OD — Yeast growth and expression-context observations


## Evidence and provenance

- SRC002 · [original] · body.b0533–body.b0564; body.b0603–body.b0645

## Extracted evidence

- Notebook contains OD600 tables for normal cells, empty vector and piGEM5 colonies, including 22/23/28 September and 8/9/13 October.
- 8 October lists empty vector and clones C1/C2/C6/C8; cultures were diluted to OD600 0.2 before follow-up.
- 13 October notes C6 was diluted in 20 mL rather than 10 mL.

## Available inputs

- Historical growth observations and clone labels

## Missing or unverified inputs

- Same-run fluorescence-to-OD joins; validated protein abundance or expression assay; corrected source anomalies; media and dilution provenance

## Limits and uncertainty

- Growth OD is not protein-expression quantification and is not automatically matched to plate-reader wells/time points.
- Source anomalies include entry dated 30.10.2026 (body.b0578), after this ingestion date, and literal 0..489 (body.b0614); no correction inferred.
- Media labels differ between some culture/control entries; reconcile rather than assume equivalence.

---

## Memory source: R-WET-CONSTRUCT

Source memory file: `E:/igem/igem_task_digest_2026-10-16/02_TASK_MEMORY/resources/R-WET-CONSTRUCT.md`

### R-WET-CONSTRUCT — Documented pRS416 and PRS426 cloning histories


## Evidence and provenance

- SRC002 · [original] · body.b0072–body.b0192; body.b0244–body.b0515
- SRC009 · DNA.xlsx · sheet.Primers.row.6–sheet.Primers.row.16
- SRC009 · Schedules.xlsx · sheet.GCaMP.R35C1–R50C5

## Extracted evidence

- Notebook initially records pRS416-GCaMP and later PRS426-GCaMP labelled piGEM5.
- The August/Sep history records sequencing submissions for piGEM5 C3 and C5 and miniprep labels C1/C3/C4/C8/C9/C10.
- 10 September transformation entry lists BY4741 negative control, empty vector, piGEM5 C3 and C5.
- DNA.xlsx Primers contains M13 forward/reverse, pRS416 primers, GCaMP fragment primers and oiGS010_GCaMP6F_piGEM005_F; other DNA workbook tabs are empty placeholders.
- Notebook calls gene fragment GCaMPf6. piGEM5 is a construct ID and must not be interpreted as proof of GCaMP5 variant.
- Schedules contains GCaMP-PRS416 wording on an August 19 row near PRS426 work, supporting unresolved label consistency rather than an authoritative sequence.

## Available inputs

- Cloning chronology, construct/colony labels, sequencing-submission evidence, primer list

## Missing or unverified inputs

- Final validated full piGEM5 sequence/consensus; clone-to-assay mapping; exact backbone/promoter/terminator/5-prime context; historical prior-report request (superseded; no prior report required)

## Limits and uncertainty

- Cloning/submission and primer inventory do not prove sequence-confirmed full construct or identify clones actually measured.
- Master report uses GCaMP5 wording, source notebook usually GCaMPf6, and design deck GCaMP6f. Variant identity remains unresolved until mapped to actual sequence.
- Do not assume pRS416 reference design equals PRS426 experimental clone. No new sequence alignment or codon analysis performed.

---

## Memory source: R-WET-SEQUENCING

Source memory file: `E:/igem/igem_task_digest_2026-10-16/02_TASK_MEMORY/resources/R-WET-SEQUENCING.md`

### R-WET-SEQUENCING — Supplied sequencing files are candidate inputs


## Evidence and provenance

- SRC008 · Sequencing results/29.07.26/pRS416C8-fw-Premixed.seq · FASTA header; related July sample inventory
- SRC008 · Sequencing results/29.07.26/pRS416C16-rev-Premixed.ab1 · ABIF directory; related July sample inventory
- SRC008 · Sequencing results/12.08.26/KZV214_74312147_74312147.phd.1 · BEGIN_SEQUENCE and BEGIN_COMMENT; related August sample inventory

## Extracted evidence

- Supplied archive includes four pRS416C8/C16 forward/reverse July sample sets and fourteen August KZV sample sets.
- 78 sequencing files are present: 18 AB1, 14 SCF, 14 PHD, 32 SEQ including clipped/unclipped variants.
- SEQ/PHD are readable inert text; AB1 directory and selected metadata and SCF headers/comments were inspected as inventory.

## Available inputs

- Original traces, base-call text and quality-format files; named early pRS416 reads

## Missing or unverified inputs

- Sample ID→construct/clone/primer map; later piGEM5 readbacks if applicable; approved consensus and measured-clone linkage

## Limits and uncertainty

- No alignment, consensus calling, base-quality assessment, variant determination, ORF/codon/structure checks performed.
- Files predate documented later PRS426 piGEM5 sequencing submissions and do not by filename alone resolve final C3/C5 clone identity.
- KZV identifiers require sample-sheet mapping; presence is not confirmation of complete usable coverage.

---

## Memory source: R-WET-MICROSCOPY

Source memory file: `E:/igem/igem_task_digest_2026-10-16/02_TASK_MEMORY/resources/R-WET-MICROSCOPY.md`

### R-WET-MICROSCOPY — Calcium and cadmium confocal method and assets


## Evidence and provenance

- SRC002 · [original] · body.b2059–body.b2076
- SRC007 · Protocols and Lab Notebook/Shared Lab Notebook.docx · body.b0632–body.b0646
- SRC006 · Data confocal/12082026/Cadmium/B10_1.tif · TIFF header; related microscopy member inventory
- SRC006 · Data confocal/12082026/Calcium/B10.nd2 · ND2 chunk inventory and UTF16 metadata; related microscopy inventory
- SRC003 · C6_10mM-calcium_5mM-cadmium_D6_t5min_1001.avi · ffprobe stream metadata

## Extracted evidence

- 9 October microscopy record maps A1 buffer; B1–B4 S1; C1–C4 S2; D1–D4 S6; E1–E4 BSX; F1–F4 C(Control).
- Record states 1 mM Ca, 50 µL cadmium; stocks 100 mM Ca and 1 or 100 mM Cd, with Cd concentration unresolved.
- 12 August confocal folder contains 25 cadmium TIF, 26 calcium TIF, one calcium PNG, and 2 calcium ND2 containers. TIFF metadata shows 512×512, 16-bit mode, 2 frames; channel meanings are not supplied.
- AVI metadata: Motion JPEG, 512×512, 121 frames at 10 fps, duration 12.1s, ImageJ AVI title. Filename asserts C6, 10mM calcium, 5mM cadmium, D6, t5min.

## Available inputs

- Original microscopy image/video files; well-map candidate and buffer/Ca/Cd method notes

## Missing or unverified inputs

- Image→well→dose→clone→date mapping; channel/exposure/gain and calibration; independent-culture IDs; segmentation/cell-intensity data if C-05 imaging branch approved; final Cd stock and volume confirmation; structural source for V-01

## Limits and uncertainty

- Metadata and filenames establish candidate assets, not cell intensities, biological response, final concentration, or independent replicate count.
- 12 August data, 9 October method and AVI filename conditions must not be joined without provenance.
- ND2 readable scope includes chunk inventory and metadata strings; semantic axes/channels remain unvalidated. TIFF/AVI pixels have not been quantified.
- An experimental microscopy video is not an atomistic calcium-binding trajectory for V-01.

---

## Memory source: R-WET-NOTEBOOK-VERSIONS

Source memory file: `E:/igem/igem_task_digest_2026-10-16/02_TASK_MEMORY/resources/R-WET-NOTEBOOK-VERSIONS.md`

### R-WET-NOTEBOOK-VERSIONS — Direct and ZIP notebooks are distinct source versions


## Evidence and provenance

- SRC002 · [original] · SHA256 adcef001c7fc1abc91d46f92336c3fb1614e577c0e5cfbad9bd2a293136ce01a
- SRC007 · Protocols and Lab Notebook/Shared Lab Notebook.docx · SHA256 15eb826989cc939cba04a258f712b23924c1d1accc47eafe0459119e7a9c9de6

## Extracted evidence

- Direct and ZIP notebooks have different bytes and extracted text; both are retained.
- The same 9 October confocal entry appears at direct body.b2059–b2076 and ZIP body.b0632–b0646.
- ZIP notebook additionally contains a 15 September encapsulation trial at body.b2029–b2054, including recorded observation that 3% agarose solidifies too fast and a proposed concentration reduction.

## Available inputs

- Two independently hashed original documents with source-specific locators

## Missing or unverified inputs

- Team decision on current notebook authority; method/result version approvals

## Limits and uncertainty

- No evidence declares either version authoritative or superseding.
- A duplicated relocated entry is not a second independent experiment.
- Encapsulation content is retained only as a hardware/wiki candidate and does not establish the dry-lab hardware deliverable.

---

## Memory source: R-WET-PROTOCOL

Source memory file: `E:/igem/igem_task_digest_2026-10-16/02_TASK_MEMORY/resources/R-WET-PROTOCOL.md`

### R-WET-PROTOCOL — GCaMP work-in-progress protocol establishes intended system


## Evidence and provenance

- SRC007 · Protocols and Lab Notebook/CGaMP - work in progress.docx · body.b0001–body.b0005; body.b0127–body.b0132

## Extracted evidence

- Work-in-progress document lists BY4741, vector p416, and an intended test exposing mid-log cells expressing CGaMP6f to different Cd levels and measuring fluorescence.
- Named source is Calcium signaling mediates the response to cadmium toxicity in Saccharomyces cerevisiae cells.

## Available inputs

- Intended host/reporter context and literature title pointer

## Missing or unverified inputs

- Final experimental construct identity and primary evidence verification if mechanistic claims are later used

## Limits and uncertainty

- Protocol intent is not an executed assay or direct Cd-binding evidence; document is explicitly work in progress.
- Detailed generic cloning/buffer recipes add no task-specific evidence and are excluded from active memory.

---

## Memory source: R-REMOTE-CONSTRUCTS

Source memory file: `E:/igem/igem_task_digest_2026-10-16/02_TASK_MEMORY/resources/R-REMOTE-CONSTRUCTS.md`

### R-REMOTE-CONSTRUCTS — GCaMP6f and pRS416 reference construct availability


## Evidence and provenance

- https://github.com/Raminyazdani/igem-saarland-2026-docking-comparison · 04fd02b7d71f14314549e2e0887300ea54fd5035 · input/raw/constructs/CGaMPf6_GF4 1.gbk · LOCUS; FEATURES promoter 48..747, CGaMP6F CDS 748..2097 and downstream annotations · Commit-pinned source
- https://github.com/Raminyazdani/igem-saarland-2026-docking-comparison · 04fd02b7d71f14314549e2e0887300ea54fd5035 · input/raw/final_plasmids/pRS416 1.dna · binary reference map; content archived · Commit-pinned source
- https://github.com/Raminyazdani/igem-saarland-2026-docking-comparison · 04fd02b7d71f14314549e2e0887300ea54fd5035 · input/raw/final_plasmids/pRS416_CGamp (1) 1.dna · binary reference design; content archived · Commit-pinned source%201.dna)
- https://github.com/Raminyazdani/igem-saarland-2026-docking-comparison · 04fd02b7d71f14314549e2e0887300ea54fd5035 · input/raw/README.md · reference-only constructs · Commit-pinned source

## Extracted evidence

- The pinned GenBank reference is a 2389 bp linear design dated 30-JUN-2026 with ScTEF1 promoter and a CGaMP6F-labelled CDS.
- Two pRS416 design/reference SnapGene files are preserved byte-for-byte.
- The repository identifies these as reference constructs rather than PAH docking receptors.
- These reference artifacts do not establish the sequencing-confirmed PRS426/piGEM5 clone actually measured in the notebook.

## Available inputs

- Pinned GenBank annotated sequence reference
- Two archived pRS416 binary design maps

## Missing or unverified inputs

- Final experimental piGEM5/PRS426 consensus sequence and clone-to-run mapping
- Historical prior-report request (superseded; no prior report required)
- Verified 5-prime transcript context
- Appropriate validated GCaMP structural reference if V-01 needs mechanistic detail

## Limits and uncertainty

- No codon analysis, translation, alignment, folding prediction or sequence redesign was performed.
- Annotation presence is not validation of ORF correctness, expression or sensor function.
- The pRS416/PRS426 backbone difference must be reconciled against the final experimental clone.
