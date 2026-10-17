# F-01 source transcription

Source: `13102026_Cadmium_LabNotebook.docx`, 13 October 2026, original new ZIP. `context_samples.csv` transcribes all20rows of `body.b0029` unchanged in meaning. Sample and concentration fields are documented labels, not sequencing confirmation or verified final concentrations.

- **Preparation:** `body.b0012–b0020`: cultures OD-normalized; 3washes using500µL at4000rpm2min in60mMPIPESpH6.5;100µL/well. EmbeddedODphoto is consistent with approximatelyOD0.1 after dilution.
- **Conditions:** `body.b0029`: C1,C2,C6,C8 andEmpty; nominalCa0,1,10mM andCd0,0.5,5mM; t0/5min labels andwell/field names.
- **Stock conflict:** `body.b0024` says1mMCdstock; `body.b0029` includes5mMCdconditions. Use nominaldose labels; no calibrateddosemodel.
- **Filename conflict:** source table row11 (`body.b0029.r0012`) names `C2_1mM-calcium_5mM-cadmium_B6_t5min_2.nd2`; actual input is `C2_0mM-calcium_5mM-cadmium_B6_t5min_2.nd2`. KeepdocumentCa1mM andfilenameCa0mM separately. Actual `_1.nd2` counterpart with1mMCais also present but is not explicitly in the source table.
- **Prior observations:** `body.b0037–b0045,b0050,b0062,b0069`: author describesstrong5mMCdlabelledresponse, around2min;some500µMresponders; activationat1and10mMCa;emptyvectornochange; quantification stillpending. These are historicalqualitativeobservations, notnewmeasuredresults.
- **Time origin:** t0/5minconditionnames do not locateCdaddition in a movie. Use ND2 acquisition time; withoutidentifiedadditionframe, curves aretime since recording start andinitial-reference normalized.
- **Identity:** `body.b0005` has `piGEM004?`; samplelabels C1/C2/C6/C8 are usable, exacttestedconstructsequence remains unresolved. Different fields/repeatedacquisitions/exports arenotindependentcultures.
- **Prior S1 figures:** `Figures.pptx` slide2 is normalizedCd5mMfluorescence, slide3 rawnoCdfluorescence, both0–300s. Bands,n,normalizationandadditioneventarenotdefined; comparequalitativelyonlyunlessnativeanalysisisrecovered.
