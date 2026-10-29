# Goal Status

更新：2026-10-29（Asia/Taipei）

## Phase 0 — COMPLETE

- 盤點：HW2 起初僅有 `PLAN.md`；HW1 為 Streamlit + SQLite；DIC2 為 Python 分析輸出靜態 GitHub Pages。
- Git：三個根目錄皆不是 Git repository；未覆蓋既有 HW2 修改，未建立 branch/commit/push。
- 延續：採 HW1 的簡潔 Streamlit UI，延續 DIC2 的 CRISP-DM、固定 split、訓練集 CV、模型比較及診斷概念。
- 修改檔案：`README.md`、`requirements.txt`、`.gitignore`、`docs/GOAL_STATUS.md`。
- 驗證：`python --version` → Python 3.11.9；三個根目錄 `git status --short --branch` → 非 Git repository。
- 剩餘：GitHub/Web 平台與教師最終格式由使用者確認。
- 下一步：資料來源核實與 registry。

## Phase 1 — COMPLETE

- Kaggle Human–AI Interaction：公開 API metadata 核實 CC0，下載檔實測 10,100 × 21；20 個原始特徵，target `latent_trust_score`，符合 14–39。
- Problem B：延續 DIC2 的 50 Startups，可完整運算；清楚標示僅 4 特徵、非正式 Kaggle 選題。
- Flood：官方 competition API 匿名下載實測 HTTP 401；依規格不以假資料或未授權鏡像替代。可取得合法 train.csv 後用 Custom 上傳。
- 修改檔案：`data/human_ai_interaction.csv`、`data/50_Startups.csv`、`src/datasets.py`、`src/validation.py`、`README.md`。
- 驗證：`pytest -q` 的 registry 測試確認 target、資料非空與 Human–AI 20 features。
- 剩餘：Flood 官方原檔需使用者 Kaggle 授權（非完成必要，正式 Kaggle 題已由 Human–AI 滿足）。
- 下一步：無洩漏前處理。

## Phase 2 — COMPLETE

- 先 split，再由 Pipeline 對訓練資料 fit median/mode imputer、StandardScaler、OneHotEncoder；未知類別可預測。
- UI 顯示 shape、缺失、重複、target 分布、相關熱圖、前 20 筆及特徵合規警告。
- 修改檔案：`src/preprocessing.py`、`src/validation.py`、`app.py`、`tests/test_modeling.py`。
- 驗證：缺值/未知類別測試、極端修改測試資料後訓練 transformer 不變測試通過。
- 剩餘：無。
- 下一步：baseline 與訓練集 CV selection。

## Phase 3 — COMPLETE

- Baseline 與 selected 均為 `LinearRegression`；`SelectKBest(f_regression)` 在 Pipeline 內。
- k 僅用訓練資料 5-fold CV RMSE 選擇；測試集只評估一次。顯示編碼後入選名稱與係數。
- 修改檔案：`src/modeling.py`、`app.py`、`tests/test_modeling.py`。
- 驗證：固定 seed 重跑之 split、入選特徵及預測一致；Human–AI 與 Startups 完整分析通過。
- 剩餘：無。
- 下一步：指標、區間與診斷。

## Phase 4 — COMPLETE

- 指標：MAE、MSE、RMSE、R²、條件式 Adjusted R²。
- 圖：實際值 vs 預測值含 y=x；排序樣本含 95% OLS observation prediction interval；殘差 vs 預測、QQ、殘差分布。
- 診斷：線性關係、Durbin–Watson、Breusch–Pagan、Jarque–Bera、VIF，含通過/有疑慮/不適用與限制。
- 區間沿用 selected pipeline 完全相同的轉換/特徵，只用訓練殘差，使用 pseudo-inverse 處理 rank deficiency。
- 修改檔案：`src/evaluation.py`、`src/intervals.py`、`src/plots.py`、`app.py`。
- 驗證：RMSE identity、退化案例、區間長度與 `lower <= prediction <= upper` 自動測試通過。
- 剩餘：無。
- 下一步：Web 與 Custom URL。

## Phase 5 — COMPLETE

- 下拉有兩個可執行 Problem 與 Custom CSV URL；切換後 target/來源/特徵均更新。
- Custom 支援公開 HTTPS URL、target、排除欄、上傳 fallback、完整分析與三種 CSV 下載。
- URL 防護：HTTPS、DNS/public IP、redirect 最終 URL、timeout、10 MB、100,000 列、200 欄、HTML/CSV 內容、最小欄數。
- 修改檔案：`src/datasets.py`、`app.py`、`tests/test_datasets.py`、`tests/test_app.py`。
- 驗證：指定 50_Startups URL 實測輸出 `(50, 5) 10 6`；Streamlit `/_stcore/health` → HTTP 200 `ok`；有效/404 類型、timeout、HTML、單欄、私有 IP/redirect 等自動測試。
- 剩餘：公開部署需使用者操作。
- 下一步：交付文件與最終重測。

## Phase 6 — COMPLETE（可自主部分）

- 完成 README、CRISP-DM 報告模板、NotebookLM 待填模板、提交清單、GPT 輔助揭露及部署步驟。
- 修改檔案：`README.md`、`docs/REPORT.md`、`docs/NOTEBOOKLM_RESEARCH.md`、`docs/SUBMISSION_CHECKLIST.md`、`docs/GOAL_STATUS.md`。
- 驗證：`pip check` → No broken requirements；`compileall` 通過；完整 pytest 結果見下節。
- GitHub repository 已建立並同步；`WAITING_FOR_USER`：NotebookLM 真實研究、ChatGPT 對話 PDF、Streamlit 公開部署、無痕公開網址驗證。
- 下一步：使用者依提交清單完成外部操作。

## 最終測試證據

- `.\.venv\Scripts\python.exe -m pytest -q` → `25 passed, 2 warnings in 6.31s`。兩項 warning 均來自 Human–AI 設計矩陣的 VIF 病態/秩不足提示；Web 診斷會如實顯示共線性疑慮，不影響模型、區間及其他測試通過。
- `.\.venv\Scripts\python.exe -m pip check` → `No broken requirements found.`
- `.\.venv\Scripts\python.exe -m compileall -q app.py src tests` → exit 0。
- 指定 Custom URL 完整管線 → 50 列 × 5 欄、10 筆測試預測、6 個 One-Hot 後入選特徵。
- Streamlit health → HTTP 200 `ok`。

## WAITING_FOR_USER

1. 在 NotebookLM 完成真實研究並填寫 100+ 中文字摘要與來源。
2. 將本次實際 ChatGPT/Codex 對話匯出 PDF，確認無敏感資訊。
3. 在 Streamlit Community Cloud 部署 `app.py`，填入 README/報告連結。
4. 用無痕瀏覽器逐一驗證兩題及指定 Custom URL，保存截圖。

## 2026-10-29 Goal 延續 — DONE（可自主部分）

### 功能補強

- 修改檔案：`src/validation.py`、`src/modeling.py`、`src/preprocessing.py`、`app.py`。
- 新增欄位型別、唯一值、缺失數/率、高缺失欄、完全重複特徵、疑似 ID／高唯一率、常數欄與資料清理策略。
- 新增編碼後特徵到原始欄位對應、模型截距、完整設定與 Baseline／Selected 圖表比較。
- One-Hot 改用第一類為基準，解除全 dummy 導致的 rank deficiency；Human–AI Maximum VIF 實測降為 16.47581，仍標示「有疑慮」。

### 效能與可靠性

- `st.cache_data` 快取內建資料及公開 URL；`st.cache_resource` 快取模型分析結果。
- Problem 切換時清除 custom frame、來源與分析狀態。
- 超過 30,000 筆時以 `random_state=42` 固定抽樣，畫面揭露來源與分析筆數。
- 保留 10 MB、100,000 列、200 欄的 URL 載入限制，補上空 chunk 與可讀下載錯誤。

### UI／UX

- 建立 Hero、深色 Sidebar、六階段 CRISP-DM Tabs、KPI 卡、資料來源摘要、模型設定卡及診斷卡。
- 統一 Plotly 字型、色彩、背景、格線、圖例與間距；加入窄螢幕 media query。
- UI 自動測試會實際載入預設題並點擊完整分析；本機 Streamlit health endpoint 另行驗證。
- 已以本機 Streamlit 實際渲染並保存 `ui-desktop.png`（1,440 × 1,100）與 `ui-mobile.png`（430 × 932）。人工檢視確認桌面版 Hero／Sidebar／KPI／Tabs 對齊正常，手機版側欄收合、卡片直向排列、標題與說明文字換行正常，未見水平溢位。
- Windows Computer Use 因無法可靠判定瀏覽器 URL 而依安全機制停止；本機 UI 證據改由實際渲染截圖、AppTest 點擊完整分析及 HTTP runtime 三者交叉驗證。公開部署後的網址與截圖仍列 `WAITING_FOR_USER`。

### 報告與實測數據

- 修改檔案：`docs/REPORT.md`、`scripts/generate_report_evidence.py`、`README.md`、`PLAN.md`。
- Human–AI Selected：MAE 4.15029、MSE 26.89273、RMSE 5.18582、R² 0.68140、Adjusted R² 0.67896。
- Human–AI 30 個編碼後特徵由 CV 選出 15 個；報告列出全部名稱及五項診斷。
- 50 Startups Selected：MAE 6,961.47781、RMSE 9,055.95732、R² 0.89873。
- 上述數值由 `.\.venv\Scripts\python.exe scripts\generate_report_evidence.py` 實際重算。

### 測試命令與結果

- `.\.venv\Scripts\python.exe -m pytest -q` → `29 passed, 1 warning`；warning 是測試刻意輸入未知類別時 sklearn 告知以全零編碼，符合 `handle_unknown='ignore'` 預期行為。
- `.\.venv\Scripts\python.exe scripts\generate_report_evidence.py` → 兩題指標、特徵、診斷與區間順序全部輸出成功。
- `ui-desktop.png`、`ui-mobile.png` → 本機實際渲染視覺驗收通過；桌面與 430px 響應式版型均可閱讀。
- 最終驗收修正 `scripts/generate_report_evidence.py` 的 Windows CP950 輸出問題，明確將 stdout 設為 UTF-8；重跑後 exit 0，`R²` 與中文診斷皆完整輸出。
- `.\.venv\Scripts\python.exe -m pip check` → `No broken requirements found.`；`.\.venv\Scripts\python.exe -m compileall -q app.py src tests scripts` → exit 0；Streamlit `/_stcore/health` → HTTP 200 `ok`。
- 剩餘人工事項：NotebookLM、對話 PDF、Streamlit 公開部署與公開網址截圖。

## 2026-10-30 GitHub 同步

- Repository：`https://github.com/cotaj6011-coder/AIot_20261029_HW2.git`，追蹤分支 `origin/main`。
- 推送前執行 `git fetch --prune origin`，本機與遠端分歧為 `0 0`，未覆蓋遠端變更。
- 驗證：`29 passed, 1 warning`、`pip check` 通過、`compileall` exit 0、兩題證據重算 exit 0、Streamlit health HTTP 200 `ok`。

