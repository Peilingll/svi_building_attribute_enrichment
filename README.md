# SVI Building Attribute Enrichment

Code and results for a master's thesis that asks how much information street-view
imagery (SVI) adds when predicting Dutch residential energy-performance labels.
Public registers (BAG, 3D BAG, EP-Online) and TABULA-NL archetypes form the
"semi-synthetic" backbone; vision models read building attributes from street
view; three experiments measure what each source contributes.

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
a CUDA GPU for the conda environment.

## Reproducing the experiments

```bash
# Dataset construction (thesis Stage 1); bbox and filters from configs/<city>.yaml
uv run python -m src.data_loader --config configs/amsterdam.yaml
uv run python -m src.tabula_matcher --config configs/amsterdam.yaml
uv run python -m src.svi_manifest

# Experiment I: ground truth, splits, training, hold-out evaluation (GPU env)
uv run python -m src.stage1.gt_builder
uv run python -m src.stage1.splits
python -m src.stage1.train --model dinov2 --all-folds
python -m src.stage1.eval_holdout --model dinov2 --ckpt <path>
python -m src.stage1.vlm.internvl3_runner --split holdout --resume

# Experiment III: feature ablation on reference attributes
uv run python -m src.stage2.run_ablation
uv run python -m src.stage2.run_ablation --task binary

# Experiment III: route comparison on the hold-out set
python -m src.stage3.extract_embeddings          # GPU env
uv run python -m src.stage3.run_stage3
uv run python -m src.stage3.run_stage3 --task binary

# Recompute every thesis-referenced result on the 2,014-building evaluation set
uv run python scripts/recompute_eval2014.py

# Thesis figures (all rendered from reports/ data; run from the repo root)
uv run python scripts/fig_ch4_1_label_distributions.py
```

Each module carries its own usage notes in the docstring.

## Inputs not in the repository

| input | source | path | needed for |
|---|---|---|---|
| EP-Online export (CSV, 2026-04-01, 1.5 GB) | [ep-online.nl](https://www.ep-online.nl/) open data | `data/raw/v20260401_v4_csv/v20260401_v4_csv.csv` | dataset construction; rebuilding `data/interim/ep_four_cities.parquet` |
| Street-view crops | Mapillary panoramas via [OpenFACADES](https://github.com/seshing/OpenFACADES); not redistributable | `data/openfacades_output/phase_c_<city>_grid/` | rerunning Experiment I |

### Reproducibility

Everything else runs from a clone: Experiments II and III, all audits, the
TABULA lookup, and every table and figure. Experiment I outputs (hold-out
predictions, per-image VLM results, DINOv2 embeddings) are versioned under
`reports/`; rerunning Experiment I requires the street-view crops and a GPU.

OpenFACADES is used only for image acquisition: this repository reads its
output structure (`src/svi_manifest.py`) and maps building IDs to BAG records
(`src/footprint_join.py`). No OpenFACADES code or model weights are included
or imported.

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

## Data sources

| Source | Method | Key fields |
|---|---|---|
| [BAG](https://www.pdok.nl/) | PDOK WFS API | pand_id, bouwjaar, geometry |
| [3D BAG](https://3dbag.nl/) | 3D BAG WFS API | roof type, height, volume, surface areas |
| [EP-Online](https://www.ep-online.nl/) | local CSV download (`data/raw/`, not tracked) | energy label A-G, primary fossil energy kWh/m2 |
| [TABULA-NL](https://webtool.building-typology.eu/) | webtool workbook `data/raw/tabula/tabula-values.xlsx`, parsed by `src/tabula/build_lookup.py` | 24 archetypes, U-values |
| Street view | Mapillary panoramas, cropped per building with OpenFACADES (see Inputs above) | one image manifest row per view |

Data dictionary for `data/processed/`: [`data/processed/README.md`](data/processed/README.md).
