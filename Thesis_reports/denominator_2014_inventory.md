# 評估集統一為 2,014 棟：影響盤點與 repo 整理提案

日期：2026-09-05。範圍：只盤點 `thesistemplate-main-v3` 有指名的表格與圖，以及產生它們的腳本。尚未執行任何重跑或搬移。

## 0. 三個問題的直接回答

1. **所有實驗的 holdout 可以控制在 2,014 棟嗎？** 可以。2,014 = fixed holdout set 2,018 減去四棟：Rotterdam 兩棟（`0599100000240334`、`0599100000647213`）InternVL3 沒有回傳有效紀錄，另外兩棟沒有有效的 3DBAG 重建面積。這四棟互不重疊，排除原因都與模型表現無關。做法是新增一份 `evaluation_pand_ids.parquet`（含 checksum），所有指標腳本以它為唯一輸入。
2. **可以寫 split by building at approximately 80:20 嗎？** 可以。10,086 棟依建築切成 8,068 / 2,018，比例 79.99 : 20.01。建議寫法：`split by building at approximately 80:20 (8,068 development, 2,018 holdout); four holdout buildings without valid outputs or geometry are excluded from all evaluations, leaving an evaluation set of 2,014 buildings`。
3. **計算的表格要改嗎？** 要。第 4 章七張結果表中有五張會變，附錄 C 兩張都會變，第 4 章三張結果圖會變。變動幅度在小數第三位，結論不會變，但數字必須重算重印，正文與結論引用的數字也要同步。

## 1. 論文指名的表格：是否受影響

| 論文表 | 內容 | 資料來源 | 產生方式 | 受 2,014 影響 | 動作 |
|---|---|---|---|---|---|
| tab:city_composition | 各研究區域的 dev / holdout 棟數與影像數 | `reports/tables/stage1/T1_per_city_train_holdout.md` | notebook 04 | 否（切分不變） | 註記加一句「evaluation set 2,014」 |
| tab:class_consistency | 證書一致性（10,086 棟） | `reports/tables/stage2/T2d_label_entropy.md` | `src/stage2/label_entropy.py` | 否 | 另案：10,093 vs 10,086 的問題 |
| tab:upstream_attributes | 三模型屬性指標（acc、F1、MAE、R²、period acc） | `T2_*_holdout_headline.md`、`T3_model_comparison.md`、`reports/stage1/r2_holdout.json` | notebook 05、06、07、08 加 `scripts/compute_stage1_r2.py` | **是**，三個模型都變 | 以 2,014 過濾 `holdout_preds.parquet` 後重算 |
| tab:joint_cell | joint accuracy、macro cell recall | `reports/tables/stage1/T4_joint_cell.md` | `src/stage1/joint_cell_eval.py`，已有 `--restrict` | **是** | `--restrict evaluation_pand_ids.parquet` |
| tab:htr_metrics | h_tr MAE、R²、面積加權相對差 | `reports/tables/stage3/T7_htr_instrument.md` | `src/stage3/htr_instrument.py` | **是**，監督式兩列由 2,016 變 2,014；InternVL3 不變 | 加 id 過濾後重跑 |
| tab:binary_conditions | 二分類八個條件 | `reports/tables/stage3/T3_main_binary.md` 與各 `*_binary_metrics.json` | `src/stage3/run_stage3.py --task binary`，已有 `--holdout` | **是**，2,016 變 2,014 | `--holdout evaluation_pand_ids.parquet` |
| tab:sevenclass_conditions | 七分類八個條件 | `reports/tables/stage3/T3_main.md` | `src/stage3/run_stage3.py`（7class） | **是** | 同上 |
| tab:feature_ablation | dev set 特徵移除 | `reports/tables/stage2/T2b_leave_one_out*.md` | `src/stage2/run_ablation.py` | 否（用 8,068 dev OOF） | 不動 |
| tab:wwr_sensitivity（附錄 C） | WWR 0.15 / 0.25 / 0.35 的 h_tr MAE | `T7_htr_instrument.md` 掃描段 | `src/stage3/htr_instrument.py` | **是** | 隨 T7 重跑 |
| tab:binary_perclass（附錄 C） | 二分類逐類 P、R、F1 | `reports/stage3/binary_prf_htr_r2.json` | `scripts/compute_binary_prf_htr_r2.py`，讀 stage3 的 metrics JSON | **是** | 在 stage3 重跑之後再跑 |

第 3 章與附錄 A、B 的表格（資料來源、篩選條件、模型配置、type 對應、U 值、超參數）都不含 holdout 指標，不受影響。

## 2. 論文指名的圖：是否受影響

| 論文圖 | 檔案 | 腳本 | 受影響 | 動作 |
|---|---|---|---|---|
| fig:svi_examples（3.4） | `fig_3_4_examples` | 手工挑選 | 否 | 不動 |
| fig:distributions（4.1） | `fig_4_1_distributions` | `scripts/fig_ch4_1_label_distributions.py` | 否（10,086） | 不動 |
| fig:type_confusion（4.2） | `fig_4_2_type_confusion` | `scripts/fig_ch4_2_type_confusion.py` | **是**，格內棟數會變 | 加 id 過濾重畫 |
| fig:year_floor（4.4） | `fig_4_4_pred_vs_true_r2` | `scripts/fig_ch4_4_pred_vs_true_r2.py` | **是**，R² 會變 | 加 id 過濾重畫 |
| fig:attribute_examples | `Thesis_reports/fig_ch4_svi_examples.png`（或新版 `_simple`） | `scripts/fig_ch4_svi_examples_simple.py` | 否，六棟都不在排除名單 | 不動 |
| fig:cell_recall（4.3） | `fig_4_3_cell_recall_heatmap` | `scripts/fig_ch4_3_cell_recall_heatmap.py` | **是**，n 與 recall 會變 | 加 id 過濾重畫 |
| （候選）建造期 Sankey | `F4_3_period_sankey` | `scripts/fig_ch4_3_period_sankey.py` | **是** | 若採用則重畫 |

第 1、2、3 章的圖都是概念圖或資料流程圖，不受影響。

## 3. 正文中會跟著變的數字

重算後需要逐一核對的位置：

- `04_experiments.tex`：Experiment I 段落（0.901、0.520、9.45、0.679、0.377 等）、E1a 混淆矩陣段（12 棟 MFH、0.92 AB recall）、E2a 段（0.825、0.826、1,595 / 2,018、0.790、0.042）、E2b 段（0.150、0.806、+10.0%、+16.6%）、Experiment III 全部段落（0.597、0.492、96.0%、9.8% 等）、三處表格 Note 的分母說明。
- `05_conclusions.tex`：九處含小數指標的句子。
- `00c_abstract.tex`：一處。
- 附錄 C 兩張表的說明文字（1,415 棟 A 到 C 等分母數字）。

建議做法：重算後先產生「舊值 → 新值」對照表，再用它逐句替換，避免漏改。

## 4. 需要修改或新增的腳本

| 項目 | 現況 | 要做的事 |
|---|---|---|
| 評估集定義 | 無 | 新增 `src/stage1/evaluation_set.py`：讀 holdout ids、InternVL3 預測檔、3DBAG 面積，排除四棟，寫出 `data/processed/evaluation_pand_ids.parquet` 與 checksum，並印出排除原因 |
| Stage 1 headline 指標 | 由四本 notebook 產生，無法自動化 | 新增 `scripts/make_stage1_tables.py`：過濾三個 `holdout_preds.parquet`，呼叫 `src/stage1/evaluate.py` 的函式重算 T2、T3 與 bootstrap CI |
| `scripts/compute_stage1_r2.py` | 直接讀整份預測檔 | 加 id 過濾 |
| `src/stage1/joint_cell_eval.py` | 已有 `--restrict` | 直接用 |
| `src/stage3/htr_instrument.py` | 只以面積是否有效篩選 | 加 id 過濾參數 |
| `src/stage3/run_stage3.py` | 已有 `--holdout` | 直接用，binary 與 7class 各跑一次 |
| `scripts/compute_binary_prf_htr_r2.py` | 讀 stage3 JSON | stage3 重跑後再跑 |
| 三個 `scripts/fig_ch4_*.py` | 讀整份預測檔 | 加共用的 id 過濾函式 |

不需要重新訓練或重新推論任何模型，全部是對既有預測檔的過濾與重算，估計一個下午可完成。

## 5. Repo 整理提案（最終交付版）

原則：交付的 repo 只留「能從原始資料重現論文每一張表與圖」所需的東西，其餘搬到 `archive/`，不刪除。以下是建議，**尚未執行**。

### 5.1 保留

- `src/`、`scripts/`（下列除外）、`configs/`、`config.yaml`、`pyproject.toml`、`uv.lock`、`README.md`、`tests/`
- `data/processed/` 中已追蹤的小型產物（切分 id、checksum、TABULA 表、manifest）
- `reports/stage1`、`reports/stage2`、`reports/stage3` 的預測檔與 metrics JSON
- `reports/tables/` 中論文引用的表：`T1_per_city_train_holdout`、`T2_*_holdout_headline`、`T3_model_comparison`、`T4_joint_cell`、`T2b_leave_one_out*`、`T2d_label_entropy`、`T3_main*`、`T7_htr_instrument`，以及 `reports/tables/audit/` 全部（資料稽核的證據）
- `thesistemplate-main-v3/`
- `Thesis_reports/` 中論文使用的最終圖與其腳本產物：`fig_ch4_svi_examples*`、`fig_3_2_record_structure_uml*`、`full_manuscript_terminology_audit*.md`、本文件
- `doc_processed/`（內層 git，研究日誌）

### 5.2 搬到 `archive/`

| 來源 | 原因 |
|---|---|
| `thesistemplate-main-v2/` 整個目錄，含 `.aux`、`.log`、`.bbl` 等編譯殘檔 | 已被 v3 取代 |
| `notebooks/04` 到 `09` 六本 ipynb、`notebooks/archived/`、`notebooks/figs_*.py`、`_stage1_plot.py`、`_stage3_plot.py` | 探索期產物；表格改由 `scripts/make_stage1_tables.py` 產生後就不再需要。若想保留研究過程，搬到 `archive/notebooks/` |
| `reports/tables/stage1/T5_loco_pool_composition`、`T9_loco_control`、所有 `*_loco_amsterdam.md`；`reports/tables/stage3/T3_error_propagation*`、`T3reg_*`、`T6_*`、`T8_*`、`T3_ordinal_collapse*`、`T3_full_comparison*`；`reports/stage3/*loco*`、`M1-reg*`、`M3-*-reg*`、`M2-DINOv2-frozenprobe*`、`M2-VLM-binprompt*` | v3 論文沒有引用 LOCO、迴歸、序數折疊、操作點等實驗 |
| `data/processed/loco_amsterdam/`、`fold_indices_delft.parquet`、`legacy/`、`legacy_ep_kwh_plain.parquet`、`mvp_vlm_testing_data_gmini/`、`phase_2_openfacade_vlm_pipeline/` | 早期或未採用的實驗資料 |
| `scripts/markdown_to_thesis.py`、`scripts/compute_cell_oracle.py` | 一次性轉換工具與未引用的 oracle 分析 |
| `Thesis_reports/CH3/` 的中間 html、`fig_ch4_svi_examples_candidates/`、`Thesis_reports/fig/`（四個檔名含全形字元與 em dash 的舊圖） | 中間產物；後者的檔名在 Windows 以外會出問題 |
| `logs/step1_*_v2.log`、`*_v3.log` 等重複訓練日誌 | 保留最終一份即可 |
| `tmp/pdfs/`、`output/pdf/` | 暫存 |
| `models/stage1`、`models/stage3` 的 checkpoint | 若未被 git 追蹤，留在本機即可；README 註明如何取得 |

### 5.3 需要你決定

1. Notebook 是搬走還是整本刪除？搬走最安全。
2. LOCO Amsterdam 的實驗 v3 完全沒提，但目標 3 原本有「transfer to Amsterdam」。若之後要放回論文，LOCO 檔案就要留在 `reports/` 而不是 archive。
3. `reports/tables/audit/` 有七份稽核表，論文只間接用到 A03、A04 的結論。建議整組保留，作為資料品質的證據。

## 6. 建議執行順序

1. 你確認第 5 節的搬移清單，我先做搬移並 commit（純 `git mv`，可還原）。
2. 新增 `evaluation_set.py`，產生 2,014 的 id 檔與 checksum，commit。
3. 依第 4 節修改腳本並重跑，產生新的表與圖，commit。
4. 產生「舊值 → 新值」對照表，逐句更新 `04_experiments.tex`、`05_conclusions.tex`、`00c_abstract.tex`，並改寫切分與評估集的定義句。
5. 更新 `full_manuscript_terminology_audit.md` 第 3 節的層級表：`comparison subset` 與兩個 `thermal evaluation subset` 合併為一個 `evaluation set (2,014)`。
