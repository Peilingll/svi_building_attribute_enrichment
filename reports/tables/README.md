# Results index

Every table in this tree and the script that regenerates it. Nothing here
should be hand-edited: if a number is wrong, fix the script and re-run.
Files with the `_binary` suffix are the two-class variant of the same run
(`--task binary`); files with the `_eval2014` suffix were recomputed on the
2,014-building evaluation set by `scripts/recompute_eval2014.py` and are the
versions the thesis quotes.

Environment: `uv run python -m <module>` for ETL / CPU work; conda
`svi-gpu` (environment.yml) for anything that runs a vision model.

## Stage 1 — can street view read building attributes?

| table | what it shows | script |
|---|---|---|
| `stage1/T1_per_city_train_holdout` | buildings and images per city, dev vs hold-out | `scripts/figs_stage1_dataset.py` |
| `stage1/T1_dinov2_cv_per_fold`, `T1_resnet50_cv_per_fold` | 5-fold CV metrics per backbone | `scripts/figs_stage1_dinov2.py`, `scripts/figs_stage1_resnet.py` |
| `stage1/T1_vlm_inference_health` | InternVL3 parse and coverage rates | `scripts/figs_stage1_vlm.py` |
| `stage1/T1_evaluation_set_by_city_eval2014` | evaluation-set composition by study area | `scripts/recompute_eval2014.py --steps bycity` |
| `stage1/T2_*_holdout_headline` | hold-out headline metrics per backbone | `src/stage1/eval_holdout.py` (numbers); tables by `scripts/figs_stage1_{dinov2,resnet,vlm}.py` |
| `stage1/T3_model_comparison` (+`_eval2014`) | DINOv2 vs ResNet-50 vs InternVL3 side by side | `scripts/figs_stage1_comparison.py`; eval2014 via `scripts/recompute_eval2014.py --steps stage1` |
| `stage1/T4_joint_cell` (+`_eval2014`) | joint TABULA-cell assignment accuracy | `src/stage1/joint_cell_eval.py` |

The `scripts/figs_*.py` scripts are plain-Python versions of the former
result notebooks: they read finished artifacts under `reports/` and
`data/processed/` and write tables and figures; nothing in them trains a model.

## Stage 2 — are those attributes worth anything? (ground-truth inputs, no images)

| table | what it shows | script |
|---|---|---|
| `stage2/T2a_cumulative` | M0 then feature groups added one at a time | `src/stage2/run_ablation.py` |
| `stage2/T2b_leave_one_out` | each feature group removed from S_full | `src/stage2/run_ablation.py` |
| `stage2/T2_per_class_s_full` | per-class breakdown of S_full | `src/stage2/run_ablation.py` |
| `stage2/T2d_label_entropy` | intra-building EPC label disagreement and the resulting oracle | `src/stage2/label_entropy.py` |
| `stage2/T2e_m1plus_fullstock` (+`_clean`, `_clean_binary`) | M1+ upper envelope on the full-stock pool | `src/stage2/m1_plus_fullstock.py` |

Metrics JSON and out-of-fold predictions for every run are in `reports/stage2/`.

## Stage 3 — join the two halves and compare routes

| table | what it shows | script |
|---|---|---|
| `stage3/T3_main` (+`_binary`, `_eval2014`) | M0 / M1 / M2 / M3 routes on the hold-out | `src/stage3/run_stage3.py`; eval2014 via `scripts/recompute_eval2014.py --steps stage3` |
| `stage3/T3_error_propagation` (+variants) | where M3 loses relative to M1 | `src/stage3/run_stage3.py` |
| `stage3/T3_ordinal_collapse` | ordinal metrics and literature-aligned label collapses | `src/stage3/ordinal_collapse.py` |
| `stage3/T3reg_regression_vs_classification` (+`_binary`) | kWh regression vs direct classification | `src/stage3/regression_kwh.py` |
| `stage3/T3_full_comparison` | every route in one table | `scripts/figs_stage3_routes.py` |
| `stage3/T7_htr_instrument` (+`_eval2014`) | transmission heat-loss readout that resolves Stage 1 quality | `src/stage3/htr_instrument.py`; eval2014 via `recompute_eval2014.py --steps htr` |
| `stage3/T8_binary_operating_point` | binary predictions read at two thresholds | `src/stage3/binary_operating_point.py` |

Per-route metrics JSON and hold-out predictions are in `reports/stage3/`,
including the M2 embeddings (`embeddings_dev.parquet`, `embeddings_holdout.parquet`).

## Audit (0.x) — does the data mean what the experiments assume?

See `audit/README.md`. Scripts: `src/audit/a0*.py`.

## Figures (`reports/figures/`)

| folder | script |
|---|---|
| `ch4/F4_1_*`, `F4_2_*`, `F4_3_*`, `F4_4_*` | `scripts/fig_ch4_*.py`; eval2014 variants via `scripts/recompute_eval2014.py --steps figures` |
| `ch4/F4_5_attribute_examples*` | `scripts/fig_ch4_svi_examples_simple.py` (needs Chrome); the `_candidates.csv` beside it lists the six buildings and their predictions |
| `audit/A02_*`, `A03_*` | `src/audit/a02_ep1_ep2.py`, `src/audit/a03_within_cell_labels.py` |
| `stage1/**` | `scripts/figs_stage1_{dataset,dinov2,resnet,vlm,comparison}.py` |
| `stage3/**` | `scripts/figs_stage3_routes.py` |

## Known gaps

- The 2026-06-26 geometry ablation was computed interactively; it is
  superseded by `src/audit/a01_compactheid_source.py`, which uses clean features.
