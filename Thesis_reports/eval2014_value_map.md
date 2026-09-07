# 2,014 評估集：論文數字對照表（舊值 → 新值）

日期：2026-09-07。資料來源：`reports/**/*_eval2014*`（commit `bc93937`）。舊值為目前 `thesistemplate-main-v3` 稿中的數字。
**尚未修改任何 .tex。** 請先審這份表，確認後我一次替換。

重現檢查：用同一套程式在原本的 2,018 / 2,016 棟上重算，所有已發表數字都能完全重現，因此新舊差異只來自排除的四棟。

## 0. 需要你決定的四件事（定性敘述受影響）

| # | 位置 | 現況 | 新值 | 影響 |
|---|---|---|---|---|
| 1 | `04_experiments.tex:516` | "Macro cell recall below 0.18" | DINOv2 0.189 | 句子不再成立，建議改為 "below 0.19" 或 "at most 0.19" |
| 2 | `04_experiments.tex:501`、`05_conclusions.tex:25` | 換成預測屬性使七分類 macro F1 降 "approximately 0.022" | 0.1705 − 0.1514 = 0.019 | 改為 0.019；方向與結論不變 |
| 3 | `04_experiments.tex:328` | 相對多數格基線的改善 "0.035 for DINOv2 and 0.036 for ResNet-50" | 0.035 與 0.035 | 兩者相同，句子可簡化 |
| 4 | Fig. 4.3 heatmap | 佔用格數 21 | 20 | 被排除的四棟中有一棟是 SFH \| 75–91 唯一的建築，該格變成灰色。正文沒有提 21 格，但 macro cell recall 的分母因此改變，這是 0.180 → 0.189 的主因，建議在圖說或正文加半句說明 |

排名檢查：所有表格的粗體（最佳值）位置都不變；Experiment I「DINOv2 六個指標中最佳」仍成立；Experiment III 各條件的排序不變。

## 1. 表格

### tab:upstream_attributes（`04_experiments.tex:279–281`）

| 列 | 欄 | 舊 | 新 |
|---|---|---|---|
| DINOv2 | Type acc | 0.901 | 0.902 |
| DINOv2 | Type macro F1 | 0.520 | 0.522 |
| DINOv2 | Year MAE | 9.45 | 9.40 |
| DINOv2 | Year R² | 0.679 | 0.681 |
| DINOv2 | Period acc | 0.901 | 0.902 |
| DINOv2 | Floor MAE | 0.377 | 0.375 |
| DINOv2 | Floor R² | 0.569 | 0.558 |
| ResNet-50 | Type acc | 0.915 | 0.916 |
| ResNet-50 | Type macro F1 | 0.492 | 0.495 |
| ResNet-50 | Year MAE | 11.82 | 11.75 |
| ResNet-50 | Year R² | 0.549 | 0.551 |
| ResNet-50 | Period acc | 0.892 | 0.893 |
| ResNet-50 | Floor MAE | 0.428 | 0.425 |
| ResNet-50 | Floor R² | 0.551 | 0.542 |
| InternVL3-2B | Type acc / macro F1 / Year MAE / Period acc / Floor MAE | 0.495 / 0.246 / 30.65 / 0.769 / 0.708 | 不變 |
| InternVL3-2B | Year R² | −0.543 | −0.547 |
| InternVL3-2B | Floor R² | 0.042 | 0.010 |

Note（286 行）改為：`All metrics are computed on the 2,014-building evaluation set.`

### tab:joint_cell（`04_experiments.tex:345–347`）

| 列 | Joint accuracy | Macro cell recall |
|---|---|---|
| DINOv2 | 0.825 → 0.826 | 0.180 → 0.189 |
| ResNet-50 | 0.826 → 0.827 | 0.128 → 0.135 |
| InternVL3-2B | 0.341 → 0.342 | 0.168 → 0.168 |

Note（352 行）改為：`n = 2,014. Expected uniform accuracy is 0.042; the majority cell baseline is 0.791.`

### tab:htr_metrics（`04_experiments.tex:383–385`）

| 列 | MAE | R² | 面積加權相對差 |
|---|---|---|---|
| DINOv2 | 0.150 → 0.149 | 0.806 → 0.810 | +10.0% → +9.8% |
| ResNet-50 | 0.157 → 0.155 | 0.771 → 0.775 | +10.5% → +10.2% |
| InternVL3-2B | 0.474 | 0.439 | +16.6% |（不變）

Note（390 行）改為：`n = 2,014 for all configurations.`

### tab:binary_conditions（`04_experiments.tex:421–428`）

| 列 | Macro P | Macro R | Macro F1 |
|---|---|---|---|
| Uniform random | 0.500 | 0.500 | 0.479 |（不變）
| Reference attribute | 0.612 | 0.529 | 0.492 |（不變；0.6115 四捨五入仍為 0.612）
| Direct DINOv2 | 0.595 | 0.600 → **0.601** | 0.597 |
| Direct ResNet-50 | 0.566 | 0.566 | 0.566 |（不變）
| Direct InternVL3-2B | 0.149 | 0.500 | 0.230 |（不變）
| Predicted DINOv2 | 0.566 | 0.522 | 0.490 |（不變）
| Predicted ResNet-50 | 0.550 | 0.519 → **0.518** | 0.488 |
| Predicted InternVL3-2B | 0.527 | 0.528 | 0.528 → **0.527** |

Caption：`($n=2{,}016$)` → `($n=2{,}014$)`。

### tab:sevenclass_conditions（`04_experiments.tex:453–460`）

| 列 | Macro F1 | Exact acc | ±1 acc |
|---|---|---|---|
| Uniform random | 0.127 | 0.143 | 0.390 |（不變）
| Reference attribute | 0.172 → **0.171** | 0.356 → **0.358** | 0.655 → **0.660** |
| Direct DINOv2 | 0.213 | 0.266 | 0.544 |（不變）
| Direct ResNet-50 | 0.201 | 0.263 | 0.570 |（不變）
| Direct InternVL3-2B | 0.015 | 0.046 | 0.167 |（不變）
| Predicted DINOv2 | 0.150 → **0.151** | 0.292 → **0.297** | 0.589 |
| Predicted ResNet-50 | 0.149 → **0.148** | 0.282 → **0.284** | 0.587 → **0.588** |
| Predicted InternVL3-2B | 0.137 → **0.131** | 0.278 → **0.277** | 0.591 → **0.596** |

Caption：`($n=2{,}016$)` → `($n=2{,}014$)`。

### tab:feature_ablation、tab:city_composition、tab:class_consistency

不變（dev set 或 10,086 棟資料集層級）。tab:city_composition 的註記可加一句：`Four holdout buildings are excluded from all evaluations (Section 4.1), leaving 2,014 evaluated buildings: Amsterdam 1,594, Rotterdam 283, Utrecht 103, Delft 34.`

### 附錄 C tab:wwr_sensitivity（`zc_appendix_c.tex:30–32`）

| 列 | 0.15 | 0.25 | 0.35 |
|---|---|---|---|
| DINOv2 | 0.150 → 0.149 | 0.150 → 0.149 | 0.150 → 0.149 |
| ResNet-50 | 0.157 → 0.155 | 0.157 → 0.155 | 0.157 → 0.155 |
| InternVL3-2B | 0.495 / 0.474 / 0.453 |（不變）

### 附錄 C tab:binary_perclass（`zc_appendix_c.tex:65–72`）

| 列 | A–C P / R / F1 | D–G P / R / F1 |
|---|---|---|
| Uniform random | 0.702 / 0.500 / 0.584 | 0.298 / 0.500 / 0.373 |（不變）
| Reference attribute | 0.715 → **0.714** / 0.960 / 0.819 | 0.509 / 0.098 / 0.165 |
| Direct DINOv2 | 0.764 / 0.731 → **0.732** / 0.748 | 0.426 → **0.427** / 0.469 / 0.447 |
| Direct ResNet-50 | 0.741 → **0.740** / 0.741 / 0.741 | 0.390 / 0.391 / 0.391 |
| Direct InternVL3-2B | 0.000 / 0.000 / 0.000 | 0.298 / 1.000 / 0.459 → **0.460** |
| Predicted DINOv2 | 0.712 / 0.936 / 0.809 | 0.419 / 0.108 / 0.172 |（不變）
| Predicted ResNet-50 | 0.710 / 0.927 / 0.804 | 0.391 / 0.110 / 0.171 |（不變；D–G P = 0.3905 四捨五入仍 0.391）
| Predicted InternVL3-2B | 0.719 / 0.698 → **0.697** / 0.708 | 0.335 / 0.359 / 0.347 |

Caption（52 行）：`2,016 buildings, with 1,415 in classes A to C and 601` → `2,014 buildings, with 1,413 in classes A to C and 601`。

## 2. 正文句子

| 檔案:行 | 舊 | 新 |
|---|---|---|
| `04:291` | 0.014；0.92；12 MFH；0.774；0.538；0.711；0.308 | 0.014；0.92；12；0.774；**0.560**；0.711；**0.320** |
| `04:301` | 9.45；0.679；11.82；0.549；30.65；0.901, 0.892, 0.769 | **9.40**；**0.681**；**11.75**；**0.551**；30.65；**0.902, 0.893**, 0.769 |
| `04:304` | 0.377；0.428；0.708；0.569, 0.551, 0.042 | **0.375**；**0.425**；0.708；**0.558, 0.542, 0.010** |
| `04:328` | 0.825 and 0.826；0.042；0.790；1,595 of the 2,018；0.035 / 0.036；0.341 on its 2,016 valid predictions | **0.826 and 0.827**；0.042；**0.791**；**1,594 of the 2,014**；**0.035 for both**；**0.342**（刪去分母子句） |
| `04:356` | 0.180；0.128；0.168；0.932；0.789；0.25 | **0.189**；**0.135**；0.168；0.932；0.789；0.25 |
| `04:366` | 0.150；0.806；0.157 and 0.771；0.474 and 0.439；3.2 | **0.149**；**0.810**；**0.155 and 0.775**；0.474 and 0.439；3.2 |
| `04:394` | +10.0%；+16.6%；0.150 and 0.157；0.495 to 0.453 | **+9.8%**；+16.6%；**0.149 and 0.155**；0.495 to 0.453 |
| `04:401` | on the 2,016-building comparison subset | on the 2,014-building evaluation set |
| `04:404` | 0.597；0.600；0.566；0.492；0.490 and 0.488 | 0.597；**0.601**；0.566；0.492；0.490 and 0.488 |
| `04:433` | 96.0%；9.8%；10.8% and 11.0%；46.9%；0.230 | 不變 |
| `04:436` | 0.213；0.201；0.172；0.137 to 0.150；0.356 and 0.655 | 0.213；0.201；**0.171**；**0.131 to 0.151**；**0.358 and 0.660** |
| `04:465` | 0.612；99% | 不變（0.6122；98.8%） |
| `04:501` | less than 0.005；approximately 0.022 | less than 0.005；**approximately 0.019** |
| `04:512` | R² of 0.679 | **0.681** |
| `04:516` | above 0.82；0.790；below 0.18 | above 0.82；**0.791**；**below 0.19** |
| `05:18` | 0.825 and 0.826；0.790 | **0.826 and 0.827**；**0.791** |
| `05:19` | 0.180 and 0.128 | **0.189 and 0.135** |
| `05:22` | 10.0% and 10.5%；16.6% | **9.8% and 10.2%**；16.6% |
| `05:25` | 0.002；0.022 | 0.002；**0.019** |
| `05:27` | 0.597；0.213 | 不變 |
| `05:46` | "produced predictions for all 2,018 holdout buildings, while two invalid InternVL3-2B records were excluded from its metrics. This design … same denominator." | 改寫為：所有配置都在同一個 2,014 棟評估集上評估 |
| `05:54` | 2,016-building comparison subset | 2,014-building evaluation set |
| `00c_abstract:5` | 9.45 years；approximately 10% higher | **9.40 years**；approximately 10% higher（9.8% 仍成立） |
| `zc_appendix_c:38` | 0.495 to 0.453 | 不變 |
| `zc_appendix_c:47` | 2,016-building comparison subset … | 2,014-building evaluation set |
| `zc_appendix_c:77–78` | 0.927 to 0.960；0.098 to 0.110；0.469 | 不變 |

## 3. 新增的定義句（放在 4.1 evaluation setup 的分母段，取代原本 39 行）

> The experimental dataset was split by building at approximately 80:20 into a development set (8,068 buildings) and a fixed holdout set (2,018 buildings). Four holdout buildings could not be evaluated under every condition: two lack a valid InternVL3-2B building-level record and two lack valid 3DBAG reconstructed areas. These four buildings are excluded from all evaluations, so every table and figure in this chapter reports results on the same evaluation set of 2,014 buildings (Appendix A lists the four identifiers).

附錄 A 加一小段列出四個 pand_id 與原因（見 `data/processed/evaluation_pand_ids.checksum.txt`）。

## 4. 圖

| 論文圖 | 新檔 |
|---|---|
| fig_4_2_type_confusion | `reports/figures/ch4/F4_2_type_confusion_eval2014.png` |
| fig_4_3_cell_recall_heatmap | `reports/figures/ch4/F4_3_cell_recall_heatmap_eval2014.png` |
| fig_4_4_pred_vs_true_r2 | `reports/figures/ch4/F4_3_pred_vs_true_r2_eval2014.png` |
| （候選）建造期 Sankey | `reports/figures/ch4/F4_3_period_sankey_eval2014.png` |

## 5. 替換時的規則

- 只改上表列出的數字與分母句；其他文字不動。
- 第 0 節四項依你的決定改寫，改寫的句子會在 commit 訊息與這份表的附錄列出。
- 替換後重跑一次全文 grep，確認 `2,016`、`comparison subset`、`0.180`、`0.022` 等舊值不再出現。
