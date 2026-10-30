# HW2 最終驗收報告

驗收日期：2026-10-31（Asia/Taipei）  
規格基準：專案實際存在的 [`PLAN.md`](../PLAN.md)（即 HW2 Codex implementation plan）及其中整理的老師原始要求與加分標準。  
判定原則：只有程式碼、資料、測試輸出或公開網站實際操作可支持的項目才標記 `PASS`。

## 結論

- 必要項目：**22 / 23，95.7%**。唯一未完成項目是必須由本人從真實對話匯出的 ChatGPT/Codex 對話 PDF，因此為 `BLOCKED`。
- 可由程式與文件完成的必要項目：**22 / 22，100%**。
- 加分預估：**+3 / +3**（兩個 Problem 下拉 +1；任意公開 HTTPS CSV URL +2）。
- GitHub：<https://github.com/cotaj6011-coder/AIot_20261029_HW2>
- Live Demo：<https://aiot20261029hw2-te9ncekg3z38qqt5muuddj.streamlit.app/>

## 逐項驗收矩陣

| 類別 | 驗收項目 | 狀態 | 實際驗證證據 |
|---|---|---:|---|
| 基本 | Kaggle 公開回歸資料 | PASS | `data/human_ai_interaction.csv` 實讀為 10,100 × 21；README 與報告連到 Kaggle Human–AI Interaction，授權標示 CC0。 |
| 基本 | 14–39 個原始特徵 | PASS | 證據腳本實算：排除 target 後為 20 個原始特徵；有效樣本 9,899。Problem B 的 4 個特徵有明確標示不符合正式門檻，不冒充主題目。 |
| 基本 | LinearRegression | PASS | `src/modeling.py` 的 baseline 與 selected pipeline 均使用 `sklearn.linear_model.LinearRegression`；公開站 Modeling 頁實際顯示 estimator。 |
| 基本 | Feature Selection | PASS | `SelectKBest(f_regression)` 候選 k=5/10/15/20/all，只在 80% 訓練集進行 5-fold CV；Human–AI 由 30 個編碼特徵選出 15 個。 |
| 基本 | Model Evaluation | PASS | 測試集輸出 MAE/MSE/RMSE/R²/Adjusted R²，並呈現 baseline/selected 比較。Human–AI selected：4.15029 / 26.89273 / 5.18582 / 0.68140 / 0.67896。 |
| 基本 | 95% 預測區間 | PASS | `src/intervals.py` 以訓練殘差和 selected transformed space 計算 OLS observation prediction interval；測試驗證 `lower <= prediction <= upper`。公開站實見區間圖、dof=7903、rank=16。此處是單筆觀測的預測區間，不誤稱平均反應信賴區間。 |
| 基本 | CRISP-DM 六階段 | PASS | 公開站實際呈現 Business Understanding、Data Understanding、Preparation、Modeling、Evaluation、Deployment 六頁；`docs/REPORT.md` 同步記錄完整流程。 |
| AI／報告 | NotebookLM 100 字以上摘要 | PASS | `docs/REPORT.md` 有明確「NotebookLM 摘要」、實際研究日期 2026-10-31；摘要超過 100 字，原始匯出保留於 `docs/Human–AI Trust 比較研究報告.md`。 |
| AI／報告 | 外部文獻與引用 | PASS | 正式報告保留 7 篇外部來源，統一作者年份格式；NIST 可信 AI 管理框架與人類信任實證研究分開描述；共形預測明列交換性條件。 |
| AI／報告 | GPT 輔助內容 | PASS | `docs/REPORT.md` 有獨立「GPT 輔助內容」章節，區分程式重算結果、NotebookLM 研究與 GPT/Codex 文字協助。 |
| AI／報告 | 正式報告 | PASS | `docs/REPORT.md` 含研究目標、CRISP-DM、模型結果、診斷、限制、AI 揭露與參考文獻；數值與證據腳本一致。 |
| AI／報告 | 真實對話 PDF | BLOCKED | `docs/` 實際搜尋沒有 PDF。依規格不得用生成或偽造檔代替，須由本人從真實 ChatGPT/Codex 對話匯出。 |
| GitHub／Web | README 完整性 | PASS | 文件開頭有 Live Demo、GitHub URL 與兩張相對路徑截圖；另含資料來源、安裝、測試、功能、限制與部署說明。 |
| GitHub／Web | GitHub Repository | PASS | 已設定 `origin/main`；本次同步前先 fetch 並確認無遠端衝突，最終 SHA 以本次提交為準。 |
| GitHub／Web | Live Demo 可存取 | PASS | Playwright 實際開啟公開 URL，頁面標題為 `Regression Studio · Streamlit`，應用完整載入且無可見 app exception。 |
| GitHub／Web | 完整截圖 | PASS | `docs/screenshots/dashboard-home.png` 與 `model-evaluation-complete.png` 實際存在；README 相對路徑正確，第二張包含模型評估、95% 區間與診斷。 |
| GitHub／Web | 公開站核心功能 | PASS | 公開站實跑 Problem A；Problem B 顯示 Encoded 5 / Selected 5；Custom URL 載入指定 50_Startups.csv、選 Profit 並完成分析；部署頁顯示三個 CSV 下載按鈕。 |
| 品質 | 自動化測試 | PASS | `pytest -q`：32 passed、1 expected warning；涵蓋 deterministic split、leakage、interval、metrics、URL 安全、資料品質、列欄上限及無效 target。 |
| 品質 | 模型數據正確性 | PASS | `scripts/generate_report_evidence.py` 從現行資料與程式重算兩題結果；RMSE²=MSE 與區間順序有測試鎖定。 |
| 品質 | 無資料洩漏 | PASS | split 先於 preprocessing/selection；CV 僅用 X_train/y_train；測試集只在選定 k 後評估。`test_feature_selection_does_not_use_test_target` 實測通過。 |
| 品質 | 錯誤處理 | PASS | 自訂 URL 僅允許公開 HTTPS，驗證 DNS/private IP/redirect/timeout/HTTP/HTML/空檔/單欄/10 MB/100,000 列/200 欄；target 驗證數值、有限值、缺失及至少 20 筆。 |
| 品質 | UI/UX | PASS | Hero、狀態卡、六階段 tabs、互動圖、警示與下載均已在公開站實際操作；切換資料來源時內容、target 與模型結果更新。 |
| 品質 | 手機版 | PASS | Playwright 將公開站 viewport 設為 430 × 932，實測 `scrollWidth=clientWidth=430`，無水平溢位、無可見錯誤。 |

## 加分項目

| 項目 | 狀態 | 預估 | 實際證據 |
|---|---:|---:|---|
| 兩種 Problem 下拉選單 | PASS | +1 | 公開站實際切換並執行 Problem A 與 Problem B；題目、target、特徵數和模型結果均更新。 |
| 任意公開 HTTPS CSV URL | PASS | +2 | 公開站使用指定 `50_Startups.csv` URL，載入後選擇 `Profit`，成功跑完模型、評估、區間與匯出流程。 |

## 實際模型重算結果

| 題目 | 模型 | MAE | MSE | RMSE | R² | Adjusted R² |
|---|---|---:|---:|---:|---:|---:|
| Human–AI Trust | Baseline | 4.15073 | 26.88617 | 5.18519 | 0.68148 | 0.67657 |
| Human–AI Trust | Selected | 4.15029 | 26.89273 | 5.18582 | 0.68140 | 0.67896 |
| 50 Startups | Selected | 6,961.47781 | 82,010,363.04501 | 9,055.95732 | 0.89873 | 0.77213 |

Human–AI 回歸假設診斷：殘差與預測值相關 0.02160（通過）、Durbin–Watson 1.98235（通過）、Jarque–Bera p=0.26403（通過）、Breusch–Pagan p=0.55601（通過）、最大 VIF=16.47581（有疑慮）。因此模型可用於課堂預測示範，但不可把統計關聯解讀為因果，係數亦須配合共線性風險審慎解讀。

## 修正內容與測試證據

本輪新增資料列／欄上限、target 缺失與非有限值自動測試，補足 URL 大型資料及 target 邊界驗收。實際命令：

```text
.\.venv\Scripts\python.exe -m pytest -q
32 passed, 1 warning

.\.venv\Scripts\python.exe -m pip check
No broken requirements found.

.\.venv\Scripts\python.exe -m compileall -q app.py src tests scripts
exit 0

.\.venv\Scripts\python.exe scripts\generate_report_evidence.py
exit 0；兩題模型指標、特徵、診斷及區間均成功重算
```

唯一 warning 是測試刻意輸入未知類別時，scikit-learn 依 `handle_unknown='ignore'` 以全零編碼，屬預期行為。

公開網站以 Playwright 實際操作驗收：Problem A、Problem B、指定 Custom URL、Profit target、模型評估、95% 區間、殘差診斷、三個下載按鈕及 430px 手機版均通過。瀏覽器 console 的 Streamlit hosting wrapper/analytics 訊息不會在應用畫面形成錯誤；本報告以「使用者可見 app exception」作為功能判定。

## 尚未完成項目與優先順序

1. **P0／BLOCKED — 對話 PDF**：本人在真實 ChatGPT/Codex 對話頁選擇列印或匯出 PDF，保存為 `docs/chatgpt_conversation.pdf`，開啟確認內容與頁面完整後再提交。

## 最終提交前待辦清單

- [x] 正式 Kaggle 題目符合 14–39 個原始特徵
- [x] LinearRegression、訓練集內 Feature Selection、模型比較及五項指標
- [x] 95% observation prediction interval、殘差與回歸假設診斷
- [x] CRISP-DM 六階段
- [x] Problem A／B 下拉與指定 Custom HTTPS CSV URL
- [x] NotebookLM 摘要、7 篇文獻、GPT 揭露與正式報告
- [x] README、GitHub、Live Demo、完整截圖與手機版
- [x] 32 項自動化測試、依賴與語法檢查
- [ ] 本人匯出並人工開啟檢查 `docs/chatgpt_conversation.pdf`
