# HW2 多元線性回歸專案：NotebookLM 研究背景

> 本文件供 Google NotebookLM 作為專案背景來源。所有資料形狀、模型指標、入選特徵與診斷統計量，均由目前 HW2 程式碼及 `scripts/generate_report_evidence.py` 實際執行取得；不是推測或虛構數值。

## 1. 專案目標

本專案建立一個以 Streamlit 實作的多元線性回歸 Web 應用，依循 CRISP-DM 的商業理解、資料理解、資料準備、建模、評估與部署流程。正式題目使用 Human–AI Interaction 資料，目標是根據人的背景、AI 系統表現、互動經驗與使用情境，預測 0–100 的人機信任分數。

核心研究重點如下：

- 使用 `LinearRegression` 建立可解釋的多元線性回歸模型。
- 以訓練集內 5-fold cross-validation 選擇特徵數量，避免使用測試集挑選模型。
- 比較全部特徵的 Baseline 與 `SelectKBest` 精簡後的 Selected 模型。
- 評估 MAE、MSE、RMSE、R²、Adjusted R²、95% prediction interval 與回歸假設。
- 將結果視為教學與關聯性分析，不宣稱因果關係。

## 2. Kaggle 資料來源與授權

- 資料集：Human–AI Interaction
- Kaggle URL：<https://www.kaggle.com/datasets/eshaalnmalik/human-ai-interaction>
- 專案內資料檔：`data/human_ai_interaction.csv`
- 授權註記：CC0 Public Domain
- 資料性質：合成教育資料，並非真人觀測資料
- 實際載入形狀：10,100 列 × 21 欄
- 原始輸入特徵：20 個
- Target：1 個
- 全表缺失格：4,245
- 完全重複列：100
- Target 缺值列：201
- 移除 Target 缺值後的實際建模列數：9,899

## 3. Target

- 欄位名稱：`latent_trust_score`
- 資料型別：`float64`
- 實際最小值：38.37438472536405
- 實際最大值：100.0
- 意義：人類對 AI 系統的潛在信任分數，數值越高代表信任程度越高。

## 4. 20 個原始特徵

| # | 欄位 | 實際型別 | 專案中的概念 |
|---:|---|---|---|
| 1 | `age` | float64 | 年齡 |
| 2 | `education_level` | categorical/string | 教育程度 |
| 3 | `technical_experience` | float64 | 技術經驗 |
| 4 | `cognitive_load` | float64 | 認知負荷 |
| 5 | `prior_ai_exposure` | categorical/string | 過往 AI 接觸程度 |
| 6 | `model_accuracy` | float64 | AI 模型準確度 |
| 7 | `explainability_score` | float64 | 可解釋性分數 |
| 8 | `bias_level` | float64 | 偏誤程度 |
| 9 | `decision_latency` | float64 | 決策延遲 |
| 10 | `error_rate` | float64 | 錯誤率 |
| 11 | `interaction_frequency` | float64 | 互動頻率 |
| 12 | `ui_complexity` | categorical/string | 使用者介面複雜度 |
| 13 | `feedback_quality` | float64 | 回饋品質 |
| 14 | `trust_history` | float64 | 過往信任紀錄 |
| 15 | `override_frequency` | float64 | 使用者覆寫 AI 決策的頻率 |
| 16 | `task_risk` | categorical/string | 任務風險 |
| 17 | `domain` | categorical/string | 應用領域 |
| 18 | `time_pressure` | float64 | 時間壓力 |
| 19 | `cultural_factor` | categorical/string | 文化因素 |
| 20 | `regulatory_strictness` | float64 | 法規嚴格程度 |

## 5. 資料前處理與防止資料洩漏

程式先移除 201 筆 Target 缺值列，再以 `random_state=42` 執行 `train_test_split(test_size=0.2)`。9,899 筆有效建模資料的實際切分為 7,919 筆訓練資料與 1,980 筆測試資料。

前處理使用 scikit-learn `Pipeline` 與 `ColumnTransformer`：

- 數值欄：`SimpleImputer(strategy="median")` 補中位數，再以 `StandardScaler` 標準化。
- 類別欄：`SimpleImputer(strategy="most_frequent")` 補眾數，再使用 `OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False)`。
- `drop="first"` 以第一個類別為基準，降低完整 dummy variables 造成的線性相依。
- Imputer、Scaler、One-Hot Encoder、Feature Selector 與迴歸器全部包在 Pipeline 中，只對訓練資料 fit。
- Target 缺值會在建模前移除；資料超過 30,000 筆時才以 `random_state=42` 固定抽樣。本正式資料只有 10,100 筆，因此本次沒有抽樣。

20 個原始特徵經前處理後形成 30 個編碼特徵。

## 6. LinearRegression 與 Feature Selection

Baseline 與 Selected 模型都使用 `sklearn.linear_model.LinearRegression`，並保留截距：

- Baseline：使用全部 30 個編碼後特徵。
- Selected：使用 `SelectKBest(score_func=f_regression)` 選取特徵。
- 候選 k：5、10、15、20、30。
- 模型選擇：只在 7,919 筆訓練資料上使用 `KFold(n_splits=5, shuffle=True, random_state=42)`。
- 評分依據：5-fold CV 的 RMSE，平均 RMSE 最低的 k 為最終選擇。
- 實際最佳 k：15。
- 最終 1,980 筆測試資料只用於一次最終評估，不參與 k 的選擇。

實際入選的 15 個編碼後特徵：

1. `num__technical_experience`
2. `num__cognitive_load`
3. `num__model_accuracy`
4. `num__bias_level`
5. `num__error_rate`
6. `num__feedback_quality`
7. `num__trust_history`
8. `num__regulatory_strictness`
9. `cat__education_level_High School`
10. `cat__education_level_PhD`
11. `cat__prior_ai_exposure_Low`
12. `cat__ui_complexity_Low`
13. `cat__ui_complexity_Medium`
14. `cat__domain_Healthcare`
15. `cat__domain_Transportation`

## 7. 實際模型指標

以下數值來自固定 seed 的 1,980 筆測試資料：

| 模型 | MAE | MSE | RMSE | R² | Adjusted R² |
|---|---:|---:|---:|---:|---:|
| Baseline（30 個編碼特徵） | 4.15072879 | 26.88617104 | 5.18518766 | 0.68147596 | 0.67657308 |
| Selected（15 個編碼特徵） | 4.15029288 | 26.89272629 | 5.18581973 | 0.68139830 | 0.67896499 |

Selected 模型的 MAE 略低、Adjusted R² 略高，但 MSE、RMSE 與 R² 沒有優於 Baseline。這代表特徵精簡主要降低模型複雜度，不能宣稱整體預測能力全面提升。

## 8. 95% Prediction Interval

專案計算的是 **95% OLS observation prediction interval**，不是平均反應的 confidence interval，也不是以測試集殘差校準的區間。

方法如下：

1. 使用 Selected Pipeline 完全相同的 Imputer、Scaler、One-Hot 與 15 個入選特徵轉換訓練集及測試集。
2. 加入常數項後，以訓練資料估計殘差變異。
3. 使用 Moore–Penrose pseudo-inverse 處理可能的秩問題。
4. 以 t 分布臨界值及新觀測的 leverage 計算 observation prediction interval。

本次實際結果：

- 方法：OLS observation prediction interval
- 設計矩陣 rank：16（15 個特徵加截距）
- 殘差自由度 dof：7,903
- 所有測試預測值皆符合 `lower <= prediction <= upper`。

最後一項只驗證區間上下界的數值順序正確，不代表真實涵蓋率必然等於 95%。

## 9. 回歸假設檢驗

診斷使用 Selected 模型的測試殘差；VIF 使用 Selected 模型的訓練設計矩陣。

| 檢查 | 實際統計量 | 專案判定 | 程式門檻 |
|---|---:|---|---|
| 線性關係 | 0.02160070 | 通過 | `abs(corr(prediction, residual)) < 0.2` |
| 誤差獨立性 | 1.98235097 | 通過 | Durbin–Watson 介於 1.5–2.5 |
| 殘差近似常態 | 0.26403450 | 通過 | Jarque–Bera p-value > 0.05 |
| 同質變異 | 0.55600672 | 通過 | Breusch–Pagan p-value > 0.05 |
| 多重共線性 | 16.47580712 | 有疑慮 | Maximum VIF < 5 才判定通過 |

線性關係統計量是預測值與殘差相關係數的絕對值；常態與同質變異欄位為檢定 p-value。Maximum VIF 明顯高於 5，因此部分入選特徵仍具有多重共線性疑慮，個別係數的方向與大小必須保守解讀。

## 10. 模型限制

- Human–AI Interaction 是合成教育資料，不能直接推論真實使用者或特定族群。
- 觀察性／合成資料中的線性關聯不等於因果關係。
- `f_regression` 是單變量線性評分，可能忽略交互作用與非線性關係。
- `LinearRegression` 假設關係近似線性；若真實資料具有非線性、界限效果或複雜交互作用，預測能力會受限。
- Selected 模型 Maximum VIF 為 16.47580712，顯示係數穩定性仍有疑慮。
- 統計檢定的「通過」只表示在目前資料、門檻與樣本下未發現明顯警訊，不能證明假設必然成立。
- 95% prediction interval 依賴線性模型與殘差假設；本專案沒有另外估計實際區間涵蓋率。
- Selected 與 Baseline 的測試指標非常接近，不能誇大 feature selection 的效能改善。
- Web 的 Custom CSV 功能可分析其他公開資料，但外部資料的欄位語意、品質與授權需由使用者確認。

## 11. 可供 NotebookLM 比較的外部研究方向

NotebookLM 可利用外部論文或可信來源，比較下列議題：

1. 人類信任 AI 的主要影響因素：準確度、可解釋性、偏誤、錯誤率、回饋品質與既有經驗。
2. 多元線性回歸在 Human–AI Trust 研究中的解釋能力與限制。
3. Filter-based feature selection（例如 F-test／SelectKBest）與 wrapper、embedded 方法的差異。
4. 多重共線性對線性迴歸係數、p-value 與可解釋性的影響。
5. Prediction interval 與 confidence interval 的差異，以及 observation prediction interval 的假設。
6. 合成資料研究結果的外部效度、偏誤與倫理限制。

## 12. 專案連結

- GitHub Repository：<https://github.com/cotaj6011-coder/AIot_20261029_HW2>
- Live Demo：<https://aiot20261029hw2-te9ncekg3z38qqt5muuddj.streamlit.app/>
- 公開站首頁截圖：`docs/screenshots/dashboard-home.png`
- 公開站模型評估截圖：`docs/screenshots/model-evaluation-complete.png`

## 13. 數值重現方式

在 HW2 專案根目錄執行：

```powershell
.\.venv\Scripts\python.exe scripts\generate_report_evidence.py
.\.venv\Scripts\python.exe -m pytest -q
```

證據腳本會輸出資料形狀、原始／編碼／入選特徵數、入選特徵名稱、Baseline 與 Selected 指標、五項診斷，以及 prediction interval 的方法、自由度、rank 與上下界順序檢查。
