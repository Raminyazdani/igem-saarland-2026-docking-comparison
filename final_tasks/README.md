# iGEM: results from the available data

Executed standalone notebooks, full notebook PDFs and scientific reports. F-01 now includes native microscopy from the supplied 17 October archive. Original archives and earlier deliveries remain unchanged outside this folder.

## Layout

- data/input/: all consumed inputs and source manifests, in one flat directory.
- data/output/<task>/: numerical tables, figures, metadata and provenance.
- tasks/<task>/: exactly <task>.ipynb, NOTEBOOK.pdf and REPORT.pdf.

## Completed scope

| Task | Result scope | Input data | Finished without more wet-lab data? |
|---|---|---|---|
| C-06 | Reference coding-sequence, codon and composition analysis | Supplied GenBank reference; historical yeast codon counts | Yes for the reference; clone attribution needs its confirmed sequence |
| D-01 | Recovery and description of 150 native plate readings, by gain/result | Three VMR files, VWP protocol and source notes | Yes for raw recovery; biological dose comparison unresolved |
| F-01 | Native microscopy, recording changes, background, optical QC and sensitivity | ND2/TIFF, source notebook, older static images and z-stacks | Yes for recorded observations and declared assumptions; no calibrated Cd-sensor performance |
| C-EX | Evidence review of alternative explanations for weak reporter response | Frozen F-01/C-06 findings and dated context | Yes for evidence review; causal expression diagnosis unresolved |
| V-01 | Conceptual calcium-associated GCaMP visual | Storyboard and primary-reference notes | Yes as a conceptual visual |
| P-01 | Within-method ranks, six distance traces and retained-run rescoring | Stored docking, MD trace and MM-GBSA files | Yes for stored computational runs |
| P-02 | Conditional binding, reporter and competition models | Documented assumed parameters and model sources | Yes as hypothetical calculations |
| W-01 | Updated offline methods/results draft | Seven frozen summaries and three attributed figure pairs | Yes as a local draft |

F-01 is supplemental; the fourteen canonical assignments have not been renumbered.

## Expanded F-01 findings

120 input files, including derived context, were inventoried and byte-verified; 107 native/export image containers were processed.

20 time-series acquisitions; 14 with native clocks. All 146 static/Z frames are retained; 141 contain fluorescence and 94 have a usable BF-region metric.

13 October, nominal 10 mM Ca / 5 mM Cd: C8: +2.66 ADU over 298.2s; Empty: +0.12 ADU over 299.5s; C6: +15.01 ADU over 298.4s; C1: +0.57 ADU over 299.6s; C2: +0.77 ADU over 299.6s. The C6 recording has the largest within-recording increase in this group. Candidate field-matched pre/post contrasts are C1 -10.22 ADU; C2 +1.92 ADU; Empty +0.68 ADU. Within-recording change and the field-matched treatment contrast answer different questions: the C1 field decreases across its paired acquisitions despite rising slightly within the challenged recording.

No recording met the preset resolved-plateau criterion; an empirical reaction time constant, t50 and t90 were not estimated.

Four same-well comparisons meet the stage/BF field-match criterion. Their pre/post contrasts are tabulated separately from within-recording change.

Recorded stage Z spans 2.34 µm in C2 Ca 1 mM / Cd 5 mM and 1.08 µm in C2 Ca 10 mM / Cd 5 mM. PFS Status is code 1 except for three code-5 frames across those two C2 recordings; PFS offsets are constant within all 14 native time series. Codes are retained without assigning a lock-state meaning; stage motion alone does not establish defocus.

6 AVI files were decoded as processed-export QC and were not counted as additional biological observations.

13 October, nominal 10 mM Ca / 5 mM Cd: C8: +2.66 ADU over 298.2s; Empty: +0.12 ADU over 299.5s; C6: +15.01 ADU over 298.4s; C1: +0.57 ADU over 299.6s; C2: +0.77 ADU over 299.6s. The C6 recording has the largest within-recording increase in this group. Candidate field-matched pre/post contrasts are C1 -10.22 ADU; C2 +1.92 ADU; Empty +0.68 ADU. Within-recording change and the field-matched treatment contrast answer different questions: the C1 field decreases across its paired acquisitions despite rising slightly within the challenged recording.

## Source of the video

The original F-01 AVI was supplied in OneDrive_1_10-16-2026.zip, not downloaded from the web. Its original name is C6_10mM-calcium_5mM-cadmium_D6_t5min_1001.avi. The analysis copy F01_recording.avi has identical SHA256 da2a3a9b7d2ae09a6d28c1c4a0118c60e4543d73326b3be4671455b826c3f81e. The new archive contains the identical AVI and matching native ND2 recording. Rendered copies are not additional cultures or experiments.

The new source ZIP OneDrive_10_10-17-2026.zip has SHA256 5a09b5171633650b78b432e369c93e265d788649fd3c51a1f1953d03399ff962. It is preserved unchanged in the separate workspace archive archives/F01_Expanded_2026-10-17/original/. Extraction, CRC and SHA rereads passed. F01_source_manifest.csv retains source paths, archive members, original names and hashes; input_manifest.csv distinguishes original and derived files.

## Remaining scientific questions

| Task | Requirement or current boundary |
|---|---|
| C-04 | Microscopy does not repair the accepted well map, matched OD and gain interpretation needed for plate-reader reanalysis. |
| C-05 | F-01 describes technical imaging variability; independent-culture identities and biological variation are still needed for empirical power. |
| C-TH | A nominal tested-condition change is not a minimum effective concentration or LOD. Verified concentrations, matched controls and a useful-signal criterion are needed. |
| C-EC | No supported EC50 curve; canonical scope remains deferred. |
| C-EX | Evidence review complete; matched protein abundance is needed to test low expression as a cause. |
| H-01 | Hardware objective, constraints and acceptance criteria remain undefined. |
| S-01 | Workflow, release, owner and approval cannot be established by offline inventory. |
| X-01 | Prioritization is applied here; owners and deadlines were not invented. |

The 13 October notebook documents preparation and sample labels. Its 1 mM Cd stock conflicts with nominal 5 mM conditions, and one C2 filename conflicts with its table's calcium label. Native clocks describe acquisition time, not a documented Cd-addition event. The six October TIFF clocks use an explicit reconstruction assumption and sensitivity check. Acquisition denoising and optics are recorded in Methods. Brightfield-derived regions are not certified individual-cell counts.

For stronger Cd conclusions, request corrected stock/final concentration records, the C2 calcium-label correction, construct/clone and independent-culture mapping, exact addition events and matched baseline/control recordings. Calibration, matched growth/viability or protein measurements are needed according to the specific performance/mechanism question. C-06 requires the confirmed clone sequence for clone attribution; it does not require a plate map or plate-reader data.

## Reproduce

Use Python 3.12, install requirements.txt into the selected Jupyter kernel, open a notebook inside this project and Restart Kernel and Run All. For a repository checkout, enter final_tasks/ before launching Jupyter. Paths and editable settings are in cell 2. Scientific code is inline; no notebook imports a project script. Three original P-02 model scripts are documentary inputs and are never imported or executed. Inputs are read-only; generated task outputs are overwritten. The native-image run reads several GB. Full saved code and results are also available as notebook PDFs.

C-EX and W-01 read explicit frozen summaries/figures; they never silently run upstream tasks. After revising an analysis, refresh its frozen inputs and provenance before rerunning a synthesis. CSV tables and source hashes accompany PNG/SVG figures. Detailed optical/region diagnostics support the reported scope.

Repository copies belong under final_tasks/. Large image inputs use Git LFS; install Git LFS and run git lfs pull after cloning before executing the notebooks. The standalone ZIP contains the actual input bytes. Absolute original-source paths inside evidence records are historical provenance, not executable input dependencies; notebook paths resolve the central data directory relative to the current package.

The unchanged C-06, D-01, P-01, P-02 and V-01 notebooks were independently rerun in the expanded environment; all 23 regenerated CSV tables agreed with the prior delivery within absolute 1e-10 / relative 1e-8 tolerances.

Biomni supplied a targeted methods review, independently assessed against actual metadata; original project files were not uploaded to Biomni. Review decisions and the link are in data/output/F-01/method_review_decisions.json. Figure conventions were informed by the Scientific Visualization skill; reference: Kassis et al. (2026), Scientific Agent Skills, https://doi.org/10.48550/arXiv.2609.00065. The current handover is prepared for a GitHub feature branch and pull request; the GitLab submission is deferred at the user's request. Original archives are unchanged; no merge, deployment or direct Wiki publication is part of this handover.
