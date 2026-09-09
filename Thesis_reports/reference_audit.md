# 參考文獻稽核（thesistemplate-main-v3）

日期：2026-09-09。方法：以腳本抽出 content/*.tex 的全部 `\cite` 鍵，對照 `literature/references.bib` 與 `norms.bib`；每筆有 DOI 的條目向 Crossref 查證標題、年份、卷期、頁碼與作者姓名；arXiv 預印本以 arXiv API 查證。**尚未修改 .bib 或 .tex。**

## 0. 總結

| 項目 | 結果 |
|---|---|
| 引用鍵 | 44 個鍵被引用，全部存在於 bib，沒有缺漏 |
| 未被引用的條目 | 11 筆（第 3 節） |
| 標題、年份、卷期、頁碼 | 27 筆有 DOI 的條目全部與 Crossref 一致，例外見第 1 節 |
| 作者姓名 | 3 筆有錯（第 1 節） |
| 手打的作者年份 | 沒有，全部用 `\textcite` / `\parencite` |
| 工具與模型首次出現處 | 都有引用（第 4 節） |

## 1. 必須修正（確定有誤）

| 鍵 | 問題 | 修正 |
|---|---|---|
| `mayer2023dk` | 第二作者名字錯：bib 寫 Heilborn, Gabriel | Crossref 與論文首頁皆為 **Gregor** Heilborn |
| `garbasevschi2021` | 第二作者姓氏拆錯：bib 寫 Schmiedt, Jacob Estevam | 姓氏是雙姓 **Estevam Schmiedt**, Jacob；另第一作者 Crossref 為 "Oana M." Garbasevschi，bib 的全名 Oana Mihaela 可保留 |
| `zeng2024` | 兩位作者名字錯：Goo, Jan Mun；Wang, Mingyuan | Crossref：Goo, **June Moh**；Wang, **Meihui** |
| `dukai2021` | 標題與出版品不符，且缺 DOI：bib 標題 "Quality assessment of a large dataset containing automatically reconstructed 3D building models" | 正式標題 "Quality assessment of a nationwide data set containing automatically reconstructed 3D building models"；DOI `10.5194/isprs-archives-XLVI-4-W4-2021-17-2021` |
| `pan_nd` | 年份：bib 寫 2025，Crossref 出版日期 2026-01-28（ASCE Computing in Civil Engineering 2025 論文集於 2026 年出版） | 建議 `year = {2026}`，booktitle 維持 "Computing in Civil Engineering 2025"；鍵名可改 `pan2026`，改鍵要同步改 ch2 的兩處引用 |

## 2. 建議修正（格式或一致性）

| 鍵 | 問題 | 建議 |
|---|---|---|
| `oquab2023`、`chen2024` | 用 `@article` 並把 "arXiv:2304.07193" 當期刊名 | 改成與 `zhu2025` 相同的 `@misc` 加 `eprint`、`archiveprefix`、`primaryclass`、`doi`（arXiv API 已確認標題與年份正確） |
| `unep2026` | bib 標題是報告封面副標；Crossref 登記的正式標題為 "Building fast. Falling short. As climate risks rise and cities grow, we must rethink how we build to create better lives for all – Global Status Report for Buildings and Construction 2025/26" | 若保留此條目，改用正式標題 |
| `rvo2011`、`caepbd2020`、`courtofaudit2016` | 報告類條目沒有 URL 或 DOI | 補 URL，讀者才找得到 |
| `kadasterbag`、`threedbagdocs`、`openstreetmap` | `@online` 沒有 `date`/`year` 也沒有 `urldate` | 至少補 `urldate`，biblatex 才不會印 n.d. |
| `cbs`、`caepbdnl` | `year = {n.d.}` 是字串，會直接印出 | 改用 `date` 或刪除 year，並補 `urldate` |
| `rvo2011` 作者 "RVO (Netherlands Enterprise Agency)"；`cbs` 作者 "CBS (Statistics Netherlands)" | 與 `rvoeponline` 的 "Netherlands Enterprise Agency" 寫法不一致，參考文獻會排成兩個不同機構 | 統一為 `{{Netherlands Enterprise Agency}}`、`{{Statistics Netherlands}}` |
| `loga2013calculation` | `type = {{TABULA} Documentation}` 會取代「Report」字樣 | 可接受；若想印成 Report，把 TABULA Documentation 移到 `series` 或 `note` |
| `NTA8800` | 作者欄是標準代號 "NTA 8800"，institution 才是 NEN | 作者改為 `{{Nederlands Normalisatie-instituut}}`，number 放 `NTA 8800:2020`，與 `iso13789` 的寫法對齊 |
| `hettinga2023` | 作者 "Van 't Veer" 大寫 V | 期刊頁面為 "van ’t Veer"；荷蘭姓氏前綴在姓名中間時小寫，建議改 `van 't Veer` |
| `ke2017`、`pedregosa2011` | 沒有 DOI | NeurIPS 與 JMLR 本來就沒有 DOI，可補 URL，非必要 |

## 3. 未被引用的 11 筆

| 鍵 | 內容 | 建議 |
|---|---|---|
| `unep2026` | GSR 2025–2026，全球 28% 能源消耗 | 第 1 章已改為只引 IEA 與 EPBD；若不打算恢復全球數字，刪除 |
| `caepbd2020` | 荷蘭 EPC 覆蓋率 48% | 第 1 章的覆蓋率句已移除；若動機段不再提，刪除 |
| `caepbdnl` | CA EPBD 荷蘭國家頁 | 與上一筆重複用途，刪除 |
| `cbs` | CBS 住宅存量 | 刪除，或在 3.2 資料來源補引 |
| `courtofaudit2016` | 荷蘭審計院能源標籤報告 | 刪除，或在 limitations 談標籤品質時引用 |
| `tabula2012` | TABULA 最終報告 | 與 `loga2016`、`loga2013calculation` 功能重疊，刪除 |
| `zirak2020` | 建築年代資料品質 | 動機段若要回應 AD-06 多找文獻，可在 1.2 引；否則刪除 |
| `buckley2021` | Dublin UBEM 用 TABULA | 2.1 談 archetype 應用時可引；否則刪除 |
| `khayatian2016` | EPC 神經網路 | 2.2 reference route 可引；否則刪除 |
| `pang2020` | 敏感度分析綜述 | 附錄 C 的 WWR 敏感度可引一句；否則刪除 |
| `chen2024` | InternVL 2.5 | 論文用的是 InternVL3（`zhu2025`），刪除 |

biblatex 只印被引用的條目，未引用的不會出現在 References，所以留著不影響輸出，但交付的 repo 保持乾淨較好。

## 4. 首次出現處的引用檢查

| 對象 | 首次出現 | 引用 | 結果 |
|---|---|---|---|
| ResNet-50 | ch2:50 | `he2016` | 正確 |
| DINOv2 | ch2:52 | `oquab2023` | 正確 |
| InternVL3 | ch2:54 | `zhu2025` | 正確 |
| GPT-4o 零樣本 | ch2:54 | `pan_nd` | 正確 |
| BAG、3DBAG、EP-Online、Mapillary | ch1:38 | `kadasterbag`、`threedbagdocs`+`peters2022`+`dukai2021`、`rvoeponline`、`mapillary` | 正確 |
| OSM、Overture | ch3:56 | `openstreetmap`、`overturemaps` | 正確 |
| NTA 8800 | ch3:95 | `NTA8800` | 正確 |
| Grounding DINO | ch3:117 | `liu2024groundingdino` | 正確 |
| ZenSVI、Places365 | ch3:127 | 引用在下一行 ch3:128 | 可接受；建議把 `\parencite{ito_zensvi_2025,zhou2018places}` 移到 127 行句尾 |
| scikit-learn | ch3:174 | `pedregosa2011` | 正確 |
| LightGBM | ch3:397 | `ke2017` | 正確 |
| TABULA-NL、WebTool | ch1:25、ch3:12 | `loga2016`、`tabulawebtool` | 正確 |
| h_tr 計算 | ch3:378、ch4:73 | `loga2013calculation` | 正確 |
| 能源標籤門檻 | ch3:390–392 | `rvoenergielabel`、`rvoenergielabel2024` | 正確 |

## 5. 執行順序建議

1. 先改第 1 節五筆確定的錯誤（三個作者名、dukai 標題與 DOI、pan 年份）。
2. 決定第 3 節 11 筆要刪或要引，刪的直接移除。
3. 第 2 節的格式統一，一次改完後重新編譯，檢查 References 頁沒有 n.d. 與重複機構名。

要我直接改 .bib 的第 1 節與第 2 節，可以一次做完並附 diff。
