# `input/raw/` — reference material only (NEVER docked directly)

These are the original project source files. They are here for provenance and traceability.
**Nothing in `raw/` is a docking input.** The only inputs anyone docks are the frozen files in
[`input/canonical/`](../canonical/). Everything docked is derived from these raw files, but the raw
files themselves are never fed to a docking tool.

## What belongs in each folder

| Folder            | Contents                                                                                     | Status in this repo |
|-------------------|----------------------------------------------------------------------------------------------|---------------------|
| `constructs/`     | Gene-fragment `.dna` (CFP_GSlink_PahS…fragment1, YFP_GSlink_PahP…fragment2, his6x_PahP…fragment3) + `.gbk` (CGaMPf6_GF4) | **present** |
| `final_plasmids/` | Assembled plasmid `.dna` (piGEM001/002/003, pRS416, pRS416_CGamp, pET-eCFP, pET-YFP, designed-pocc…mScarletI-G3BP1) | **present** |
| `literature/`     | Reference papers `.pdf` (Vina, CB-Dock3, GOLD, VOC biofilters, cadmium/Ca, OR deorphanization) | placeholder — add PDFs here |
| `slides/`         | Presentation decks `.pptx`                                                                     | placeholder — add decks here |
| `notes/`          | Meeting minutes `.docx` / `.odt` / `.pdf`                                                      | placeholder — add notes here |

`literature/`, `slides/`, and `notes/` currently hold only a `.gitkeep`. The source PDFs / PPTX / DOCX
live in the workspace root; they are large binaries and were intentionally **not** committed to keep the
git repo lightweight. Drop them in these folders locally if you want them versioned (consider Git LFS).

## Rules
- **Do not rename raw files.** Some contain spaces or `(1)` in the name — keep the original names for traceability.
- **Do not edit raw files.** Corrections happen downstream in `input/canonical/`, not here.
- Only PahP and PahS are docking targets. The fluorescent proteins (CFP/YFP), GCaMP6f, the
  MBP-mScarlet-G3BP1 construct, and the pRS416 / pET backbones are **reference only**, not receptors.
