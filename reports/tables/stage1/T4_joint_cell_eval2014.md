# Table 4 — Joint TABULA-cell assignment (hold-out)

Cell = (size class x TABULA period). Joint = type AND period both correct.
majority_cell = always predicting the most frequent TRUE cell (baseline).
macro_cell_recall = unweighted mean recall over occupied cells.

| model | n | type_acc | period_acc | joint_acc | majority-cell baseline | macro-cell recall | cells |
|---|---:|---:|---:|---:|---:|---:|---:|
| DINOv2 frozen | 2014 | 0.9017 | 0.9022 | 0.8262 | 0.7915 | 0.1888 | 20 |
| ResNet-50 ft | 2014 | 0.9156 | 0.8928 | 0.8267 | 0.7915 | 0.1348 | 20 |
| InternVL3 (ZS) | 2014 | 0.4945 | 0.7691 | 0.3416 | 0.7915 | 0.1683 | 20 |

## DINOv2 frozen — per-cell recall (true cells, by support)

| true cell | support | recall |
|---|---:|---:|
| AB|NL.01 | 1594 | 0.932 |
| TH|NL.01 | 166 | 0.789 |
| AB|NL.03 | 97 | 0.247 |
| AB|NL.04 | 52 | 0.077 |
| SFH|NL.01 | 21 | 0.524 |
| AB|NL.05 | 17 | 0.059 |
| TH|NL.04 | 12 | 0.167 |
| TH|NL.03 | 11 | 0.182 |
| AB|NL.02 | 10 | 0.100 |
| TH|NL.05 | 10 | 0.200 |
| MFH|NL.01 | 5 | 0.000 |
| AB|NL.06 | 3 | 0.000 |
| TH|NL.02 | 3 | 0.000 |
| MFH|NL.03 | 3 | 0.000 |
| MFH|NL.02 | 2 | 0.000 |
| MFH|NL.04 | 2 | 0.000 |
| TH|NL.06 | 2 | 0.500 |
| SFH|NL.05 | 2 | 0.000 |
| SFH|NL.02 | 1 | 0.000 |
| SFH|NL.04 | 1 | 0.000 |

### DINOv2 frozen — top confusion pairs (true -> pred, joint errors)

| true cell | pred cell | count |
|---|---|---:|
| AB|NL.01 | TH|NL.01 | 93 |
| AB|NL.03 | AB|NL.01 | 27 |
| TH|NL.01 | AB|NL.01 | 23 |
| AB|NL.03 | AB|NL.02 | 21 |
| AB|NL.04 | AB|NL.01 | 18 |
| AB|NL.04 | AB|NL.03 | 13 |
| TH|NL.01 | SFH|NL.01 | 10 |
| AB|NL.04 | AB|NL.02 | 10 |

## ResNet-50 ft — per-cell recall (true cells, by support)

| true cell | support | recall |
|---|---:|---:|
| AB|NL.01 | 1594 | 0.947 |
| TH|NL.01 | 166 | 0.699 |
| AB|NL.03 | 97 | 0.227 |
| AB|NL.04 | 52 | 0.154 |
| SFH|NL.01 | 21 | 0.238 |
| AB|NL.05 | 17 | 0.059 |
| TH|NL.04 | 12 | 0.000 |
| TH|NL.03 | 11 | 0.273 |
| AB|NL.02 | 10 | 0.100 |
| TH|NL.05 | 10 | 0.000 |
| MFH|NL.01 | 5 | 0.000 |
| AB|NL.06 | 3 | 0.000 |
| TH|NL.02 | 3 | 0.000 |
| MFH|NL.03 | 3 | 0.000 |
| MFH|NL.02 | 2 | 0.000 |
| MFH|NL.04 | 2 | 0.000 |
| TH|NL.06 | 2 | 0.000 |
| SFH|NL.05 | 2 | 0.000 |
| SFH|NL.02 | 1 | 0.000 |
| SFH|NL.04 | 1 | 0.000 |

### ResNet-50 ft — top confusion pairs (true -> pred, joint errors)

| true cell | pred cell | count |
|---|---|---:|
| AB|NL.01 | TH|NL.01 | 60 |
| TH|NL.01 | AB|NL.01 | 40 |
| AB|NL.03 | AB|NL.01 | 39 |
| AB|NL.04 | AB|NL.01 | 24 |
| AB|NL.03 | AB|NL.02 | 14 |
| SFH|NL.01 | TH|NL.01 | 13 |
| AB|NL.03 | AB|NL.04 | 10 |
| AB|NL.01 | AB|NL.02 | 10 |

## InternVL3 (ZS) — per-cell recall (true cells, by support)

| true cell | support | recall |
|---|---:|---:|
| AB|NL.01 | 1594 | 0.385 |
| TH|NL.01 | 166 | 0.229 |
| AB|NL.03 | 97 | 0.216 |
| AB|NL.04 | 52 | 0.000 |
| SFH|NL.01 | 21 | 0.286 |
| AB|NL.05 | 17 | 0.059 |
| TH|NL.04 | 12 | 0.000 |
| TH|NL.03 | 11 | 0.091 |
| AB|NL.02 | 10 | 0.600 |
| TH|NL.05 | 10 | 0.000 |
| MFH|NL.01 | 5 | 0.000 |
| AB|NL.06 | 3 | 0.000 |
| MFH|NL.03 | 3 | 0.000 |
| TH|NL.02 | 3 | 0.000 |
| MFH|NL.02 | 2 | 0.000 |
| MFH|NL.04 | 2 | 0.000 |
| SFH|NL.05 | 2 | 0.500 |
| TH|NL.06 | 2 | 0.000 |
| SFH|NL.02 | 1 | 1.000 |
| SFH|NL.04 | 1 | 0.000 |

### InternVL3 (ZS) — top confusion pairs (true -> pred, joint errors)

| true cell | pred cell | count |
|---|---|---:|
| AB|NL.01 | TH|NL.01 | 754 |
| AB|NL.01 | AB|NL.03 | 87 |
| AB|NL.01 | AB|NL.02 | 66 |
| AB|NL.01 | SFH|NL.01 | 40 |
| TH|NL.01 | SFH|NL.01 | 35 |
| AB|NL.03 | AB|NL.01 | 32 |
| AB|NL.03 | AB|NL.02 | 32 |
| TH|NL.01 | SFH|NL.03 | 23 |
