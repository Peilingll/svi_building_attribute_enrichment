# SVI Building Attribute Enrichment

Code and results for a master's thesis that asks how much information street-view
imagery (SVI) adds when predicting Dutch residential energy-performance labels.
Public registers (BAG, 3D BAG, EP-Online) and TABULA-NL archetypes form the
"semi-synthetic" backbone; vision models read building attributes from street
view; a three-stage experiment measures what each source contributes.

Study area: residential buildings in Amsterdam, Rotterdam, Utrecht and Delft.

## Where the code is

Folder names predate the thesis numbering.

| Thesis | Code |
|---|---|
| Stage 1 Dataset Construction | `src/data_loader.py`, `lod2_features.py`, `tabula_matcher.py`, `svi_manifest.py`, `stage1/gt_builder.py`, `stage1/splits.py` |
| Stage 2 Attribute Prediction (Exp. I) | `src/stage1/` |
| Stage 3 Archetype Assignment (Exp. II) | `src/tabula/`, `stage1/joint_cell_eval.py`, `stage3/htr_instrument.py` |
| Stage 4 Energy Class Prediction (Exp. III) | `src/stage2/` (ablation), `src/stage3/` (routes) |
| Data checks | `src/audit/` |

Table-to-script map: `reports/tables/README.md`.

## Environments

Two Python environments are used on purpose; do not mix them.

| Environment | Used for | How |
|---|---|---|
| `uv` project venv (`.venv/`) | ETL, LightGBM, figures, tables (CPU) | `uv sync`, then `uv run python -m <module>` |
| conda `stage1-gpu` | anything that runs a vision model (Stage 1 training, embeddings, VLM inference) | `conda activate stage1-gpu`, then `python -m <module>` |

Requirements: Python 3.13+, [uv](https://docs.astral.sh/uv/getting-started/installation/),
a CUDA GPU for the conda environment. Copy `.env.example` to `.env` for API keys.

## Reproducing the experiments

```bash
# Stage 0: registry join per city (bbox and filters from configs/<city>.yaml)
uv run python -m src.data_loader --config configs/amsterdam.yaml
uv run python -m src.tabula_matcher --config configs/amsterdam.yaml
uv run python -m src.svi_manifest

# Stage 1: ground truth, splits, training, hold-out evaluation (GPU env)
uv run python -m src.stage1.gt_builder
uv run python -m src.stage1.splits
python -m src.stage1.train --model dinov2 --all-folds
python -m src.stage1.eval_holdout --model dinov2 --ckpt <path>
python -m src.stage1.vlm.internvl3_runner --split holdout --resume

# Stage 2: feature ablation on ground-truth attributes
uv run python -m src.stage2.run_ablation
uv run python -m src.stage2.run_ablation --task binary

# Stage 3: route comparison on the hold-out set
python -m src.stage3.extract_embeddings          # GPU env
uv run python -m src.stage3.run_stage3
uv run python -m src.stage3.run_stage3 --task binary

# Recompute every thesis-referenced result on the 2,014-building evaluation set
uv run python scripts/recompute_eval2014.py

# Thesis figures (all rendered from reports/ data; run from the repo root)
uv run python scripts/fig_ch4_1_label_distributions.py
```

Each module carries its own usage notes in the docstring.

## Inputs not included in the repository

Everything under `data/raw/`, `data/interim/`, `data/openfacades_output/` and
`models/` is excluded, either for licensing reasons or because it is large and
regenerable. Reviewers need the following only for the stages marked below.

| input | where it comes from | put it at | needed for |
|---|---|---|---|
| EP-Online certificate export (CSV, snapshot 2026-04-01) | open data at ep-online.nl | `data/raw/v20260401_v4_csv/v20260401_v4_csv.csv` | Stage 0 registry join, `src.stage2.extract_kwh`, `src.audit.*` |
| TABULA-NL workbook | TABULA WebTool, NL country data | `data/raw/tabula/tabula-values.xlsx` | `src.tabula.build_lookup` only (the resulting `tabula_nl.csv` is tracked) |
| CBS neighbourhood polygons 2023 | fetched automatically from PDOK WFS by `src.stage2.m1_plus_fullstock` | `data/raw/cbs_buurten_2023.parquet` | the M1+ full-stock experiment |
| Street-view crops | Mapillary panoramas processed with [OpenFACADES](https://github.com/seshing/OpenFACADES) into per-building crops; not redistributable under the Mapillary terms | `data/openfacades_output/phase_c_<city>_grid/` (paths recorded in `svi_manifest.parquet`) | Stage 1 training, embedding extraction and VLM inference |
| Trained checkpoints | produced by `src.stage1.train` | `models/stage1/*.pt` | Stage 1 hold-out evaluation and embedding extraction |

What can be reproduced without any of these: Stage 2 in full, Stage 3 in full
(the Stage 1 hold-out predictions, per-image VLM outputs and DINOv2 embeddings
it consumes are tracked under `reports/`), every audit that reads
`data/processed/`, and every table and figure. Stage 1 itself (training the
vision models and running InternVL3) needs the street-view crops and a GPU;
its outputs are tracked so the downstream stages do not depend on rerunning it.

OpenFACADES is used as the image acquisition pipeline only. The code here
reads its output folder layout (`src/svi_manifest.py`) and maps its building
ids to BAG (`src/footprint_join.py`); no OpenFACADES code or model weights are
imported.

## Repository layout

```
├── config.yaml                 # Delft-era base config (WFS endpoints, filters)
├── configs/<city>.yaml         # per-city bbox and fetch parameters
├── src/
│   ├── data_loader.py          # Stage 0 step 1: BAG + 3D BAG + EP-Online join
│   ├── lod2_features.py        # Stage 0 step 2: geometry features from 3D BAG
│   ├── tabula_matcher.py       # Stage 0 step 3: TABULA-NL archetype + U-values
│   ├── svi_manifest.py         # street-view image manifest for Stage 1
│   ├── tabula/                 # rebuild the TABULA-NL lookup from the official workbook
│   ├── audit/                  # a01-a07 data audits quoted in the thesis
│   ├── stage1/                 # vision models -> building attributes (+ vlm/)
│   ├── stage2/                 # attributes -> EPC label, LightGBM ablation
│   └── stage3/                 # end-to-end route comparison, regression, ordinal metrics
├── scripts/
│   ├── fig_ch4_*.py            # thesis figures rendered from reports/ data
│   ├── figs_stage1_*.py, figs_stage3_routes.py   # per-stage result tables and figures
│   ├── _stage1_plot.py, _stage3_plot.py   # shared plotting helpers
│   ├── compute_*.py            # one-off numbers (oracle, random baseline, R2)
│   ├── recompute_eval2014.py   # re-run every result on the evaluation set
│   └── derive_city_bboxes.py   # one-off bbox helper
├── data/processed/             # tracked parquet outputs, splits, TABULA lookup (see its README)
├── reports/
│   ├── stage{1,2,3}/           # metrics JSON + prediction parquet per run
│   ├── tables/                 # thesis tables (md/csv) + results index README
│   └── figures/                # thesis figures (png + pdf)
└── uv.lock, pyproject.toml     # uv environment
```

The LaTeX thesis and the dated research logs are not in this repository. They live in
`doc_processed/` (thesis-docs repository): `thesistemplate-main-v3/` takes its figures
from `reports/figures/`, `research_log/` holds the English logs.


Not tracked (local only, see `.gitignore`): `data/raw/`, `data/interim/`,
`models/`, `logs/`, `archive/` (LOCO experiment, notebooks, retired scripts,
older thesis templates), `doc_processed/` (planning notes), `notebooks/`,
`Thesis_reports/` (figure workshop and review notes), `doc_processed/` (thesis text,
plans and logs; its own git repository).

## Data sources

| Source | Method | Key fields |
|---|---|---|
| [BAG](https://www.pdok.nl/) | PDOK WFS API | pand_id, bouwjaar, geometry |
| [3D BAG](https://3dbag.nl/) | 3D BAG WFS API | roof type, height, volume, surface areas |
| [EP-Online](https://www.ep-online.nl/) | local CSV download (`data/raw/`, not tracked) | energy label A-G, primary fossil energy kWh/m2 |
| [TABULA-NL](https://webtool.building-typology.eu/) | webtool workbook `data/raw/tabula/tabula-values.xlsx` (not tracked), parsed by `src/tabula/build_lookup.py` | 24 archetypes, U-values |
| Street view | Mapillary panoramas, cropped per building with OpenFACADES (see below) | one image manifest row per view |

Data dictionary for `data/processed/`: [`data/processed/README.md`](data/processed/README.md).
