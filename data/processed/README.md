# `data/processed/` — Data Dictionary

Tracked intermediate outputs of the Stage 0 registry pipeline plus the frozen
splits that every experiment reads. Raw inputs live in `data/raw/` (not tracked).
Row counts below were read on 2026-09-10.

## Layout

```
data/processed/
├── README.md
├── tabula_nl.csv                       # canonical TABULA-NL U-value lookup (24 archetypes)
├── tabula_nl_provenance.csv            # which TABULA construction backs every value
├── legacy/tabula_nl_handmade.csv       # superseded hand-typed lookup, kept for pre-2026-07-27 results
├── <city>/                             # amsterdam, rotterdam, utrecht, delft
│   ├── bag_3dbag_ep_joined.parquet     # Stage 0 step 1: BAG + 3D BAG + EP-Online join
│   ├── bag_ep_joined.parquet           # earlier BAG + EP-Online join, no 3D BAG (not for delft)
│   ├── residential_with_3d_features.parquet   # step 2: LOD2 geometry features
│   ├── residential_tabula_matched.parquet     # step 3: TABULA archetype + U-values
│   └── step1.log, step3.log            # run logs, audit trail (not for delft)
├── stage1_gt.parquet                   # Stage 1 ground truth, four cities concatenated
├── stage1_gt_<city>.parquet            # per-city copies for sanity checks
├── svi_manifest.parquet                # one row per street-view crop, capped at 8 per building
├── dev_fold_indices.parquet            # 80% development set with fold 0-4
├── holdout_test_pand_ids.parquet       # 20% frozen hold-out (+ .checksum.txt)
├── evaluation_pand_ids.parquet         # hold-out minus 4 unevaluable buildings (+ .checksum.txt)
├── ep_kwh.parquet                      # continuous primary fossil energy per pand_id
└── legacy_ep_kwh_plain.parquet         # pre-2026-08-10 slice built from the plain column
```

## Stage 0 registry pipeline (per city)

All four cities run the same three steps, driven by `configs/<city>.yaml`
(`pipeline.use_3dbag: true`). The root `config.yaml` is the original Delft
configuration and still writes to top-level paths; the Delft outputs were moved
into `delft/` by hand.

| step | module | reads | writes |
|---|---|---|---|
| 1 | `src.data_loader` | PDOK BAG WFS (2 km tiles), 3D BAG WFS, EP-Online CSV | `<city>/bag_3dbag_ep_joined.parquet` |
| 2 | `src.lod2_features` | step 1 output | `<city>/residential_with_3d_features.parquet` |
| 3 | `src.tabula_matcher` | step 2 output + `tabula_nl.csv` | `<city>/residential_tabula_matched.parquet` |

`<city>/bag_ep_joined.parquet` is the older two-source join. It is still read by
`src/svi_manifest.py` as the BAG geometry source when mapping street-view crops
to buildings.

```bash
uv run python -m src.data_loader     --config configs/amsterdam.yaml
uv run python -m src.lod2_features   --config configs/amsterdam.yaml
uv run python -m src.tabula_matcher  --config configs/amsterdam.yaml
```

## File schemas

### `<city>/bag_3dbag_ep_joined.parquet` (86 columns)

One row per BAG pand that has an EP-Online certificate.

- key: `pand_id` (16-digit zero-padded string)
- BAG: `identificatie`, `bouwjaar`, `status`, `gebruiksdoel`, `aantal_verblijfsobjecten`, `geometry` (RD New, EPSG:28992)
- 3D BAG: `b3_*` attributes (heights, roof and wall areas, volume, `b3_bouwlagen`, reconstruction quality)
- EP-Online: `Energieklasse`, `Gebouwtype`, `Gebouwklasse`, `Postcode`, `Registratiedatum`, `Status`
- derived: `build_period`

### `<city>/bag_ep_joined.parquet` (21 columns)

Same BAG + EP-Online columns without the `b3_*` fields.

### `<city>/residential_with_3d_features.parquet` (8 columns)

`pand_id`, `volume`, `envelope_area`, `shape_factor`, `building_height`,
`num_floors_estimated`, `floor_area_estimated`, `lod2_quality_flag`.

### `<city>/residential_tabula_matched.parquet` (16 columns)

Step 2 columns plus `Gebouwtype`, `bouwjaar`, `tabula_building_type`
(SFH / TH / MFH / AB), `tabula_period` (NL.01–NL.06), `u_wall`, `u_roof`,
`u_floor`, `u_window`.

### `stage1_gt.parquet` (8 columns)

Built by `src.stage1.gt_builder --cities all`. One row per pand_id:
`pand_id`, `city`, `bouwjaar` (year target), `Gebouwtype` (raw BAG label, used
for stratification), `building_type` (SFH/TH/MFH/AB target), `num_floors`
(from `b3_bouwlagen`), `Energieklasse` (Stage 2/3 target), `tabula_period`.

### `svi_manifest.parquet` (8 columns)

Built by `src.svi_manifest`. One row per street-view crop:
`pand_id`, `panorama_id` (Mapillary), `bdid` (OpenFACADES footprint id),
`file_path`, `city`, `aov_geo` (degrees of building width in view),
`distance` (m), `image_idx` (0–7 rank by `aov_geo` desc, `distance` asc).
Image files themselves are not tracked.

### Splits

Built by `src.stage1.splits` (StratifiedGroupKFold, group = pand_id,
strata = city × Gebouwtype × Energieklasse × tabula_period, seed 42).

| file | rows | columns |
|---|---|---|
| `dev_fold_indices.parquet` | 8,068 | `pand_id`, `fold` (0–4), `city`, `building_type`, `Energieklasse`, `tabula_period` |
| `holdout_test_pand_ids.parquet` | 2,018 | same minus `fold`, plus `split` |
| `evaluation_pand_ids.parquet` | 2,014 | hold-out minus 2 buildings without a valid InternVL3 record and 2 without valid 3D BAG areas; built by `src.stage1.evaluation_set` |

The `.checksum.txt` files carry the SHA-256 prefix, counts and excluded ids so
a regenerated split can be verified.

### `ep_kwh.parquet` (5 columns)

Built by `src.stage2.extract_kwh` from the raw EP-Online CSV. Residential
certificates only, latest per pand_id: `pand_id`, `pf_kwh` (primary fossil
energy, kWh/m²·yr, taken from `PrimaireFossieleEnergieEMGForfaitair` with
fallback to the plain column), `pf_plain`, `pf_source`, `energieklasse_raw`.
`legacy_ep_kwh_plain.parquet` is the earlier slice that used only the plain
column (audit A04); kept so pre-fix regression results stay reproducible.

### TABULA lookup

`tabula_nl.csv` is regenerated by `src.tabula.build_lookup` from the TABULA
workbook `data/raw/tabula/tabula-values.xlsx` (not tracked).
`tabula_nl_provenance.csv` names the TABULA construction behind every U-value.
`legacy/tabula_nl_handmade.csv` is the pre-2026-07-27 hand-typed table;
`src.tabula.impact_check` diffs the two.

Period codes (`src/tabula_matcher.py`):

| code | construction year |
|---|---|
| NL.01 | ≤ 1964 |
| NL.02 | 1965–1974 |
| NL.03 | 1975–1991 |
| NL.04 | 1992–2005 |
| NL.05 | 2006–2014 |
| NL.06 | ≥ 2015 |

## Row counts (2026-09-10)

| file | amsterdam | rotterdam | utrecht | delft |
|---|---|---|---|---|
| `bag_3dbag_ep_joined` | 63,734 | 38,024 | 20,036 | 3,500 |
| `bag_ep_joined` | 63,785 | 38,037 | 20,060 | — |
| `residential_with_3d_features` | 63,348 | 37,936 | 20,022 | 3,496 |
| `residential_tabula_matched` | 63,346 | 37,936 | 20,021 | 3,495 |
| `stage1_gt_<city>` | 63,344 | 37,923 | 20,021 | 3,496 |

| file | rows |
|---|---|
| `stage1_gt.parquet` | 124,784 |
| `svi_manifest.parquet` | 47,238 |
| `dev_fold_indices.parquet` | 8,068 |
| `holdout_test_pand_ids.parquet` | 2,018 |
| `evaluation_pand_ids.parquet` | 2,014 |
| `ep_kwh.parquet` | 1,556,809 |
| `legacy_ep_kwh_plain.parquet` | 1,552,143 |

## Source endpoints

- BAG WFS: `https://service.pdok.nl/lv/bag/wfs/v2_0` (layer `bag:pand`), fetched in 2 km tiles because PDOK caps one query at about 51k features.
- 3D BAG WFS: `https://data.3dbag.nl/api/BAG3D/wfs` (layer `BAG3D:lod12`).
- EP-Online: local CSV snapshot in `data/raw/`.
- Municipal boundaries: `https://service.pdok.nl/kadaster/bestuurlijkegebieden/wfs/v1_0`.
