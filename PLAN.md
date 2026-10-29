HW2 多元線性回歸 Web 專案：VS Code 多根工作區與 Codex /goal 執行規格
> 用途：將本檔放在 VS Code **HW2 資料夾根目錄**，在已同時開啟 `HW2`、`HW1`、`20261014` 的多根工作區中，由 Codex `/goal` 持續執行。此檔是完整規格與驗收清單，不代表功能已完成。  
> 作業核心：Kaggle 公開資料集、原始輸入特徵 14–39 個、Linear Regression、Feature Selection、Model Evaluation、含區間的預測圖、CRISP-DM、GitHub + Web。  
> 加分：兩種 problem 的下拉選單（+1）；任意輸入 CSV Dataset 網址（+2）。
0. Codex 工作原則
0.1 多根工作區邊界（最高優先）
資料夾	角色	Codex 可做的事
`HW2/`	唯一主要開發目標	讀取、建立、修改、測試與整理 HW2 專案，保留使用者既有更動
`HW1/`	前次作業參考	唯讀：檢視程式、模型、UI、README、架構與可重用概念
`20261014/`	DIC2 參考專案	唯讀：研究 GitHub/Web 交付型態、UI、部署與資料呈現方式
其他工作區/父資料夾	非本任務	未取得明確授權前，不讀取非必要私有檔案、不修改
注意：即使 VS Code 三個根目錄位於不同實體路徑，也須依工作區根目錄名稱辨識，不可猜測相對父資料夾路徑。不要在 `HW1/` 或 `20261014/` 執行會產生或改寫檔案的安裝、測試、格式化、git commit 等動作。引用舊專案的概念可以，但複製程式時要檢查必要性、依賴、適用性與來源。
0.2 自動迭代規則
先盤點三個根目錄與各自 Git 狀態、README、部署設定；依 `HW1`、`20261014` 的已驗證做法延續一致體驗，若 `HW2` 空白才採用 Streamlit + Python 預設方案。不要直接認定三者必然相同技術。
`/goal` 啟動後，不用每個 Phase 都等待批准。依 Phase 0→6 連續執行；每階段驗證後更新進度與記錄，再進下一階段。
不要覆蓋既有使用者修改；小步提交變更與測試。發現問題先修復，再進入下一階段；不得只寫 TODO 就稱完成。
所有新功能與輸出必須在 `HW2/`。如需建立虛擬環境、快取、下載資料或部署設定，也都限於 `HW2/` 或安全的暫存路徑。
任一階段缺少必要外部資料或授權時，可完成其他互不依賴事項；真正無法前進時記錄證據、已試方法及要使用者提供的最小輸入，停止於 blocker。
未經使用者確認，不改任何現有遠端 Git repository、不推送、不對外發布、不進行會產生費用的雲端動作。可以把程式、部署設定與操作文件準備好；正式 Git push / Web publish 屬於人工確認關卡。
不得自行宣稱完成使用者才能做的 NotebookLM 研究、ChatGPT 對話匯出 PDF 或外部平台發布；準備模板及操作說明，將這些項目標成 `WAITING_FOR_USER`。
僅以本文件確認的需求為準。若 HW1 / DIC2 的 URL、架構或教師其他規範缺失，在 README 註記「待確認」，不可猜測。
研究摘要不可捏造 NotebookLM 的使用經過、來源及結論；ChatGPT 對話 PDF 必須由實際對話匯出。
API 金鑰、Kaggle Token 等不可提交 Git；需在 `.gitignore` 排除。發布前檢查授權、資料大小與敏感資訊。
0.3 Goal 進度紀錄與完成條件
在 `HW2/docs/GOAL_STATUS.md` 建立持續更新的狀態表，欄位：Phase、狀態（`TODO / IN_PROGRESS / DONE / BLOCKED / WAITING_FOR_USER`）、修改檔案、執行命令、測試結果、未解風險及下一步。
每個 Phase 記錄實際命令與結果；測試未跑不能標記通過。每次迭代先讀此檔、Git diff 與最新測試結果，避免重做已完成工作。
完成定義：HW2 本地專案已落實所有可由 Codex 完成的 P0、P1 需求，測試通過、兩種題目可運行、Custom URL 有測試、文件齊全；外部平台或人工研究項目明確列為等待使用者，而非偽稱完全交付。
停下條件：資料來源及合法存取均無可行方案、權限拒絕、外部發布確認、會覆寫使用者修改、重複嘗試仍無法修復的客觀阻礙、或所有可授權工作已驗收完成。
1. 需求及驗收矩陣
優先	項目	完成條件
P0	Kaggle 資料來源	至少一組可執行的 Kaggle 資料集；顯示名稱、連結、授權/限制及檢查後的特徵數
P0	14–39 原始 features	不包含 target、ID、洩漏欄位；正式選題確實符合 `13 < n_features < 40`，另記錄 One-Hot 後維度
P0	CRISP-DM	網頁及報告對應六階段，能重現資料理解、整理、建模、評估及部署
P0	多元線性回歸	`sklearn.linear_model.LinearRegression` 完整訓練與測試流程
P0	Feature Selection	至少比較全特徵基準與選特徵模型；只對訓練集 fit，列出入選特徵
P0	Evaluation	MAE、MSE、RMSE、R²；有條件計算 Adjusted R²，附殘差診斷
P0	預測圖及區間	測試集真實值 vs 預測值圖；另有清楚標記 95% 信賴區間或預測區間 的預測視覺化及計算方法
P0	GitHub + Web	公開/教師可存取 GitHub Repo、可開啟的部署網址及 README 操作步驟
P0	AI 使用揭露	報告明確標示「GPT 輔助內容」及「NotebookLM 摘要」；後者至少 100 個中文字並附來源
P0	對話 PDF	將實際 ChatGPT 對話匯出為 PDF；依教師規則附上或提供連結
P1	Problem 下拉選單 (+1)	至少兩個可運作且任務不同的預設回歸題目；切換時 target、說明、圖表、模型均更新
P1	任意 Dataset URL (+2)	使用者可貼公開可存取的 CSV HTTPS URL，預覽欄位、選 target、執行同一分析管線
P2	報告/資訊圖	可選擇匯出 HTML/PDF 報告、額外資訊圖或互動圖表；不影響 P0/P1
注意： 加分任意 URL 模式不保證資料有 14–39 個特徵；應顯示其特徵數和合規警告，但不要阻止一般 CSV 分析。正式提交仍需至少一組符合特徵數的 Kaggle 題目。
2. 題目與資料集規劃
Problem A（優先完整實作）：Flood Probability Prediction
Kaggle 官方競賽：Regression with a Flood Prediction Dataset
Kaggle 資料頁：Data
目標 `FloodProbability`，連續數值；預期 20 個因素特徵；`id` 不參與訓練。
此競賽資料為合成資料，不能宣稱是實際觀測的洪水發生率；模型只是教學上的風險分數預測。
優先將授權允許的訓練用 CSV 以外部下載、雲端可存取 URL 或小型合法樣本提供；大型資料集不可直接全部放 GitHub。Kaggle 若需登入或接受規則，README 應提供手動下載指引與本地路徑。
不得將 Kaggle test.csv 當作有標籤評估集；由具有 target 的 train.csv 做訓練/測試切分。
Problem B（候選，先核驗）：Human–AI Interaction
Kaggle：Human-AI Interaction
預定研究連續的信任/互動評分，但目前尚未確認實際 CSV 欄位、特徵數、target 名稱及使用條款。
Phase 1 必須讀取欄位，驗證 14–39 個原始特徵及連續數值 target；若不符合，改選另一個符合條件的 Kaggle 公開回歸資料集，更新此文件與 README 後才實作 Problem B。
不能僅在選單放標籤或圖表截圖；必須能真正訓練與評估。
URL 輸入加分模式
測試 URL：`https://raw.githubusercontent.com/Avik-Jain/100-Days-Of-ML-Code/master/datasets/50_Startups.csv`
此 CSV 僅為 URL 功能測試，並非正式 Kaggle 14–39 features 題目。
對任意合法公開 CSV 自動偵測型別，讓使用者選連續數值 target、排除 ID、挑選候選特徵；不適合回歸時顯示明確原因。
3. 技術架構（空白專案預設）
建議：Python 3.11+、Streamlit、pandas、numpy、scikit-learn、statsmodels、matplotlib 或 plotly、scipy、pytest。部署預設 Streamlit Community Cloud；若 HW1/DIC2 已有 Flask/FastAPI/其他框架，優先保留其架構。
```text
HW2/
├── app.py                       # Web UI 與三種資料來源模式
├── src/
│   ├── datasets.py              # 預設資料集設定、載入、CSV URL 安全驗證
│   ├── validation.py            # target/特徵數/資料品質檢查
│   ├── preprocessing.py         # split、ColumnTransformer、imputer、encoder
│   ├── modeling.py              # 基準模型、特徵選擇、模型比較
│   ├── evaluation.py            # 指標、殘差、回歸假設診斷
│   ├── intervals.py             # 區間估計與可重現計算
│   └── plots.py                 # 預測/殘差/特徵圖
├── data/                         # 僅放許可發布的小型資料；大檔由下載指南提供
├── tests/                        # 基本測試、資料洩漏、URL、安全與 UI smoke test
├── docs/
│   ├── REPORT.md                 # CRISP-DM、圖表、NotebookLM、GPT 標示
│   ├── NOTEBOOKLM_RESEARCH.md    # 使用者實際研究後填入的摘要與來源
│   └── SUBMISSION_CHECKLIST.md   # GitHub、Web、對話 PDF、截圖清單
│   └── GOAL_STATUS.md            # 每階段證據、結果及待使用者處理事項
├── requirements.txt
├── .gitignore
└── README.md
```
目錄是建議而非強制；不要為了遵守樹狀結構而破壞現存 HW1 架構。
4. 分階段實作流程
Phase 0 — 工作區盤點與需求鎖定
[ ] 盤點 `HW2/` 現狀與 Git；唯讀盤點 `HW1/` 與 `20261014/` 原始程式、部署方式、技術、README 與依賴，寫一份差異與可借鑑清單。
[ ] 建立需求追蹤清單；確認教師有無另外限定雲端平台、報告格式、資料授權。
[ ] 建立 README 中的「執行方式」、「資料來源」、「部署網址（待填）」欄位。
驗收： `python --version`、Git 狀態與專案結構可確認；不覆蓋舊版檔案。
Phase 1 — 資料驗證與兩個 Problem
[ ] 下載/載入 Problem A 有 target 的資料；記錄 shape、dtype、target、缺失率、重複資料與來源。
[ ] 用程式計算原始候選特徵數，排除 target / id / 明顯資料洩漏欄位，確認 14–39。
[ ] 實際查驗 Problem B；不符規範即更換，並記錄可重現來源。
[ ] 建立 dataset registry：`id`、顯示名稱、來源 URL、target、排除欄位、載入說明與授權註記。
[ ] 缺資料或 Kaggle 權限時顯示友善錯誤，不用未經驗證的假資料默默替代。
驗收： 兩題都能產生可重現的特徵清單；至少一題確實是 Kaggle 14–39 特徵。
Phase 2 — Data Understanding / Preparation
[ ] 顯示資料筆數/欄數、欄位型別、前幾筆、敘述統計、缺失值、target 分布、相關係數熱圖。
[ ] 固定 `random_state=42`，先 `train_test_split(test_size=0.2)`，嚴格保留測試集。
[ ] 使用 `Pipeline` + `ColumnTransformer`：數值缺失值補中位數；類別補眾數再 One-Hot（`handle_unknown='ignore'`）；需要時標準化。
[ ] 所有 imputer、encoder、scaler、feature selector 僅在訓練資料 fit，不得事先對整份資料 fit。
[ ] 檢查常數欄位、過高缺失率、重複特徵、疑似洩漏與目標缺值；處理策略列在報告。
驗收： 測試集未影響任何前處理學習；含類別欄位、缺值與未知類別也能預測。
Phase 3 — Modeling / Feature Selection
[ ] baseline：全部合格輸入特徵的 `LinearRegression`。
[ ] selected：以 `SelectKBest(f_regression)`、RFE 或 SequentialFeatureSelector 選出一組特徵（例如 14/15 個，候選不足時依資料實況調整）。
[ ] 透過 Pipeline + 訓練集內 5-fold CV 比較候選 k 或方法；最終測試集只評估一次，禁止以測試集分數挑 k。
[ ] 顯示選中特徵（若 One-Hot 後選取，顯示編碼後名稱及對應原始欄位）、係數、截距與模型設定。
[ ] 可選 Ridge/Lasso 作進階比較，但不得取代作業要求的 `LinearRegression`。
驗收： 畫面有 baseline vs selected 的比較表，且重跑結果可重現。
Phase 4 — Evaluation / 區間與診斷
[ ] 測試集計算 MAE、MSE、RMSE、R²；Adjusted R² 僅在 `n_test > p + 1` 且設計矩陣有效時提供，並標示 `p` 定義與限制。
[ ] 預測圖 1：真實值 vs 預測值散點圖（含理想 `y=x` 對角線）。
[ ] 預測圖 2：排序或按預測值呈現部分測試樣本的點估計及 95% 預測區間（明確標示該區間，而非把殘差 ±1 標準差說成 95%）。
[ ] 區間建議實作：選定最終線性模型後，對訓練資料使用 statsmodels OLS（加入常數項）計算新樣本 observation prediction interval；須驗證與主模型所用前處理、特徵完全一致，處理 rank deficiency、極端維度與記憶體問題。也可用訓練資料內部的保留校準集做 split conformal prediction interval，註明其分布無關的邊際涵蓋率假設；任何方法都不可用測試集殘差校準區間。
[ ] 實作殘差 vs 預測值、殘差 QQ plot、殘差分布，並檢查線性關係、誤差獨立性、同質變異、殘差近似常態、多重共線性（VIF）。各檢驗須附「通過/有疑慮/不適用」及方法限制，不宣稱檢定可完全證明假設。
[ ] 特別說明：連續的 `FloodProbability` 雖位於 0–1，但一般 OLS 預測值與區間可能超出界限；在圖中如實呈現並警告，不能私自裁切後仍聲稱是原 OLS 區間。
驗收： 指標、兩張核心預測圖、95% 區間與至少主要殘差診斷可在 Web 中重算；小樣本/奇異矩陣時有合理降級資訊。
Phase 5 — Web UI 與加分功能
[ ] 頁面頂部下拉：`Problem A — Flood`、`Problem B —（驗證後名稱）`、`Custom CSV URL`；若教師只計兩題，下拉仍明確可見兩個預設題目。
[ ] 切換 problem 時重置不相容的 target/特徵選擇狀態；UI 顯示目前來源、target 與原始特徵數。
[ ] Custom 模式包含 URL 輸入、載入按鈕、資料預覽、target 選擇、排除欄位、多元回歸分析按鈕。
[ ] URL 安全：僅 HTTPS；拒絕 localhost、私有/回環/連結本地 IP、內部 hostname 與重新導向後的私有目標；設定 timeout、大小上限（例如 10 MB）、列數/欄數上限、CSV MIME/內容檢查；錯誤可讀。部署環境若無法安全防 SSRF，改為只允許指定公開來源或提供 CSV 上傳 fallback，並在 README 說明限制。
[ ] 快取資料載入與分析結果，顯示執行狀態，避免大資料使免費 Web 超時；設定可重現的下採樣策略（只對資源限制使用並揭露）。
[ ] 結果清楚分成六個 CRISP-DM 區塊；可下載所選特徵清單、metrics.csv、測試集 predictions.csv。
驗收： 兩預設題可以切換並完整運算；提供的 50_Startups HTTPS CSV 可讀、能選 `Profit` 為 target 並完成回歸；非 CSV/無法存取/無效 target 不會造成整站崩潰。
Phase 6 — 報告、AI 研究及交付
[ ] `docs/REPORT.md` 依六階段記錄問題背景、來源、資料探索、清理策略、模型、選特徵方法、CV、測試集指標、預測區間、假設檢查、限制及 Deployment 截圖/連結。
[ ] 報告有獨立小節 「GPT 輔助內容」：列出 ChatGPT / Codex 協助哪些設計、程式、除錯與人工核實工作；不得把 AI 產物當成未經驗證實驗結果。
[ ] 使用者親自將同主題的網頁/研究來源加入 NotebookLM，取得研究結果；在 「NotebookLM 摘要」 撰寫不少於 100 個中文字的實際摘要（建議 150–250 字），附來源 URL、NotebookLM 研究日期、與自己方法的比較。Codex 可提供「待填模板」，不可冒充已做的 NotebookLM 研究。
[ ] 將與 ChatGPT 的相關對話使用瀏覽器列印成 PDF、pdfCrowd 或其他工具匯出；確認內容清晰、沒有暴露敏感資料。可放 `docs/chatgpt_conversation.pdf` 或交付連結，依教師規範提交。
[ ] README 加上 GitHub Repo、Live Web、資料下載/授權、安裝執行、操作流程、加分展示、測試指令與已知限制。
[ ] 完成部署所需配置、指令與檢查清單；僅在使用者明確授權且憑證/遠端目標已確認後才進行 Git push / Web 發布，發布後由使用者與 Codex 驗證網址。
驗收： 本地可運行且部署就緒；已獲授權發布時 GitHub、Web 兩連結可直接操作；未獲授權時在 `GOAL_STATUS.md` 明確記錄待發布。對話 PDF、NotebookLM 完成人工步驟前不可標記完成。
5. 測試清單（必須自動化的部分）
[ ] 預設資料集的 target 存在、原始特徵數檢查、ID 排除及資料非空。
[ ] 固定 seed 兩次執行，切分、入選特徵與測試指標一致。
[ ] 對測試值極端修改，訓練階段 imputer / selector 結果不變（避免 data leakage）。
[ ] `RMSE ≈ sqrt(MSE)`；各指標接受正常與退化案例。
[ ] 預測區間輸出樣本數與預測值一致，`lower <= prediction <= upper`（在所選方法適用的前提下），且沒有測試集校準洩漏。
[ ] Custom URL：有效 CSV、404、timeout、HTML 偽裝 CSV、缺 target、非數值 target、單欄、極小樣本、缺值、類別變數、超大檔、私有 IP/redirect 均有測試。
[ ] `pytest -q` 全數通過；`streamlit run app.py` 本地可啟動；Web 上手動點選兩題和 Custom 模式。
6. 完成定義（Definition of Done）
必交：至少一個正式 Kaggle 14–39 features 題目，完整 CRISP-DM、線性回歸、特徵選擇、模型評估、含 95% 區間預測圖；GitHub + 可用 Web 列為取得發布授權後的最終交付關卡。
加分 +1：下拉選單能切換兩個可運作的不同回歸 problem。
加分 +2：公開 HTTPS CSV URL 可選 target 並跑完整流程；能示範 50_Startups.csv。
AI 文件：GPT 輔助內容、真正的 NotebookLM 研究摘要（100+ 中文字）、實際對話 PDF。
品質：測試通過、固定 seed 可重現、不洩漏測試資料、不提交 token、頁面錯誤提示友善。
7. 建議執行順序及優先權
`Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6`。
若時間有限，優先完成 Problem A 的 P0 所有核心功能與 GitHub/Web，再做 Problem B (+1) 與 Custom CSV (+2)；NotebookLM 摘要及對話 PDF 必須留出人工操作時間。不可為了加分犧牲基本模型評估與區間圖。
8. 給 VS Code Codex 的 /goal 指令（可直接貼上）
```text
/goal 持續將 VS Code 多根工作區的 HW2/ 開發為可測試、可部署的 HW2 多元線性回歸 Web 專案，完整需求以 HW2/HW2_CODEX_IMPLEMENTATION_PLAN.md 為準。先盤點工作區與 Git 狀態，唯讀參考 HW1/ 和 20261014/（DIC2）之架構、介面與部署方式；只允許修改 HW2/，不得改動其他兩個資料夾或覆寫既有使用者更動。

依 Phase 0→6 自主持續執行，不必每階段等我回覆。每次實作都要實際跑相關測試、修復失敗、記錄證據，再決定下一步。以 HW2/docs/GOAL_STATUS.md 保存進度、測試命令/結果、已完成工作、剩餘風險與下一步，避免中斷後重做。無法核實的資料或模型結果不得編造。

成功條件：正式 Kaggle 題目原始輸入特徵介於 14–39；兩個不同且都可執行的 problem 下拉選項；Custom HTTPS CSV URL 可輸入並選擇連續 target；完整 CRISP-DM、無資料洩漏的前處理與特徵選擇、LinearRegression 基準與選特徵比較、MAE/MSE/RMSE/R²、清楚標示方法的 95% 預測區間圖、回歸假設診斷；README、報告模板及自動化測試齊備。使用提供的 50_Startups.csv 驗證 Custom URL，而非冒充正式 Kaggle 題目。

每階段若失敗，先依錯誤證據採取安全的局部修復並重跑測試；若欠缺 Kaggle 權限，優先嘗試合法公開替代資料來源或安排使用者手動匯入，不得繞過限制。NotebookLM 真實研究、ChatGPT 對話 PDF、Git push 和 Web 發布需由我提供資料或明確授權；先完成可做的部分，標註 WAITING_FOR_USER，不可假裝完成。

只有在所有可自主完成的工作經驗證通過，或遇到必須由我決策/授權且無其他安全工作可做的阻礙時才停止。最後回報：完成清單、實際測試證據、尚未完成與原因、待我處理的最少事項、可直接複製的執行與部署步驟。
```
Goal 控制指令與使用建議
```text
/goal          # 查看目前 Goal
/goal pause    # 暫停
/goal resume   # 繼續
/goal clear    # 清除
```
請在支援 Goals 的 Codex 版本及命令介面中執行（Codex 0.128.0 起支援）；若 VS Code 中未出現 `/goal`，先確認 Codex 的版本/功能可用性，再改用支援的 Codex CLI 或逐階段普通提示，不要把原始指令當程式碼執行。Goal 是同一個 Codex thread 的持續目標，不保證無限預算、持續背景運作或不需權限。
新對話或進度中斷時的恢復 Prompt
```text
請先讀 HW2/HW2_CODEX_IMPLEMENTATION_PLAN.md 與 HW2/docs/GOAL_STATUS.md，核對 HW2 的 git diff、已完成檔案及最近一次測試；只從第一個未通過的驗收項目繼續，勿重做已驗證內容。HW1 和 20261014 僅唯讀參考。若 Goal 仍有效就繼續依完成條件迭代；若因預算或權限暫停，先列出最少必要操作與下一個可驗證步驟。
```
9. 來源與待確認事項
Kaggle 官方競賽（Problem A）：https://www.kaggle.com/competitions/playground-series-s4e5
Kaggle Human–AI Interaction（Problem B 候選）：https://www.kaggle.com/datasets/eshaalnmalik/human-ai-interaction/data
自訂網址測試資料：https://raw.githubusercontent.com/Avik-Jain/100-Days-Of-ML-Code/master/datasets/50_Startups.csv
[ ] 使用者補充 HW1/DIC2 的實際 repo 或程式碼時，調整本文件架構以承接原專案。
[ ] 核實 Problem B 欄位、特徵數、target、授權及下載方式。
[ ] 確認教師「對話 PDF」是否必交（題目中的 AI 協助要求為必須，繳交列表又列 optional；先保守準備）。
[ ] 確認 GitHub / Web 平台與報告繳交格式。

10. 實作狀態（2026-10-29 實測）

> 本節是目前工作樹的實際狀態；上方 `[ ]` 保留為原始規格清單。逐項命令與結果見 `docs/GOAL_STATUS.md`。

| 範圍 | 狀態 | 實際證據 |
| --- | --- | --- |
| Phase 0 工作區盤點 | DONE | 三根目錄、Git、技術、UI、資料流與部署方式已盤點；只修改 HW2 |
| Phase 1 兩題與正式 Kaggle 題 | DONE | Human–AI：10,100 × 21、20 原始特徵、CC0；50 Startups 可完整運算 |
| Phase 2 資料理解與準備 | DONE | 型別、敘述統計、缺失率、重複特徵、疑似 ID、清理策略及無洩漏 Pipeline |
| Phase 3 Modeling | DONE | LinearRegression Baseline／Selected、訓練集 5-fold CV、特徵對應、係數與截距 |
| Phase 4 Evaluation | DONE | 全部指標、兩張核心圖、95% OLS prediction interval、殘差與五項診斷 |
| Phase 5 Web／加分 | DONE | 兩題下拉、Custom HTTPS CSV／上傳、快取、狀態重置、抽樣揭露及三種下載 |
| Phase 6 可自主文件 | DONE | README、實測 REPORT、研究模板、提交清單與部署步驟 |
| 本機 UI 視覺驗收 | DONE | 實際渲染 `ui-desktop.png`（1,440 × 1,100）與 `ui-mobile.png`（430 × 932）；桌面與響應式版型人工檢視通過 |
| NotebookLM 真實研究 | WAITING_FOR_USER | 必須由使用者在 NotebookLM 實際研究並填入 100+ 中文字 |
| ChatGPT 對話 PDF | WAITING_FOR_USER | 必須由實際對話匯出 |
| GitHub push／公開 Web | WAITING_FOR_USER | 未取得遠端目標與發布授權，不虛構完成 |

Flood 競賽不是教師指定必選題；匿名 Kaggle API 實測 HTTP 401。正式 14–39 特徵 Kaggle 條件已由 Human–AI Interaction 的 20 個原始特徵滿足，因此 Flood 權限不阻礙本地完成定義。
