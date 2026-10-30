# 多元線性回歸 Web 專案報告

> 本報告數值由 `scripts/generate_report_evidence.py` 實際重算，不是人工填造。GitHub、公開網站、部署截圖與 NotebookLM 比較研究已完成；正式提交前仍須補上對話 PDF。

## 1. Business Understanding

正式題目使用 Kaggle 的 **Human–AI Interaction** 合成教育資料，目標是根據人類因素、AI 系統表現、互動經驗及情境資訊，預測 0–100 的 `latent_trust_score`。資料為合成資料，因此結果只適合示範迴歸分析與討論欄位關聯，不代表真實使用者，也不能解讀為因果效果。

第二個預設題目是 50 Startups，根據研發、行政、行銷支出與州別預測 `Profit`。它用於展示題目切換與小型資料分析，不冒充正式 14–39 特徵 Kaggle 題。

## 2. Data Understanding

### Human–AI Interaction

- 來源：<https://www.kaggle.com/datasets/eshaalnmalik/human-ai-interaction>
- 授權：CC0 Public Domain。
- Shape：10,100 筆 × 21 欄。
- Target：`latent_trust_score`。
- 原始候選特徵：20，符合 `13 < n_features < 40`。
- 資料包含數值與類別欄位；Web 顯示資料預覽、型別、唯一值、缺失數/率、常數欄、重複列、敘述統計、target 分布及數值相關係數。

系統另檢查高缺失欄（門檻 50%）、完全重複特徵、疑似 ID／高唯一率欄及 target 缺失。疑似 ID 或洩漏欄只提出警示並交由使用者確認，不以欄位名稱猜測後靜默刪除。

## 3. Data Preparation

1. 先移除 target 缺失列。
2. 若有效資料超過 30,000 筆，以 `random_state=42` 固定抽樣並在畫面揭露原始與分析筆數。
3. 使用 `train_test_split(test_size=0.2, random_state=42)` 保留測試集。
4. 數值欄以訓練集中位數補值並標準化。
5. 類別欄以訓練集眾數補值，再做 One-Hot；第一類作為基準並設定 `handle_unknown='ignore'`。
6. Imputer、Scaler、Encoder 及 Selector 均在 sklearn Pipeline 中，只對訓練資料 fit。
7. 常數欄自動排除；ID、疑似洩漏及不使用欄位由 UI 明確選擇。

自動化測試會極端修改測試資料，再確認已 fit 的訓練 transformer 不變，以驗證測試資料沒有反向影響前處理。

## 4. Modeling

Baseline 與 Selected 均使用 `sklearn.linear_model.LinearRegression`：

- Baseline：全部合格且經編碼的特徵。
- Selected：`SelectKBest(f_regression)`。
- 候選 k：5、10、15、20 及全部（不超過實際編碼後維度）。
- k 的選擇依據：訓練集內、shuffle 且固定 seed 的 5-fold CV RMSE。
- 測試集只在模型選定後評估一次，不用測試分數選 k。

Human–AI 資料 One-Hot 後為 30 個特徵；CV 選出 15 個：

`technical_experience`、`cognitive_load`、`model_accuracy`、`bias_level`、`error_rate`、`feedback_quality`、`trust_history`、`regulatory_strictness`、`education_level_High School`、`education_level_PhD`、`prior_ai_exposure_Low`、`ui_complexity_Low`、`ui_complexity_Medium`、`domain_Healthcare`、`domain_Transportation`。

Web 同時顯示編碼後名稱、原始欄位對應、係數、截距、split、CV 與 estimator 設定。

## 5. Evaluation

### Human–AI Interaction 實測結果

| 模型 | MAE | MSE | RMSE | R² | Adjusted R² |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | 4.15073 | 26.88617 | 5.18519 | 0.68148 | 0.67657 |
| Selected | 4.15029 | 26.89273 | 5.18582 | 0.68140 | 0.67896 |

Selected 使用較少特徵並得到略低 MAE、略高 Adjusted R²，但 RMSE 與 R² 沒有超越 Baseline。這表示特徵精簡主要改善模型簡潔性，不能宣稱全面提升預測效能。

### 50 Startups 實測結果

| 模型 | MAE | MSE | RMSE | R² | Adjusted R² |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | 6,961.47781 | 82,010,363.04501 | 9,055.95732 | 0.89873 | 0.77213 |
| Selected | 6,961.47781 | 82,010,363.04501 | 9,055.95732 | 0.89873 | 0.77213 |

此資料 One-Hot 後只有 5 個特徵，CV 最終保留全部，因此兩模型相同。

### 95% 預測區間

使用 Selected Pipeline 完全相同的轉換與特徵空間，加入常數項後以訓練殘差估計 OLS observation prediction interval。矩陣反解使用 pseudo-inverse，並依有效 rank 計算自由度；沒有用測試殘差校準區間。兩題均實測滿足 `lower <= prediction <= upper`。

### 回歸假設診斷

Human–AI Selected 模型：

| 檢查 | 統計量 | 判定 |
| --- | ---: | --- |
| 線性關係：`|corr(ŷ, residual)|` | 0.02160 | 通過 |
| Durbin–Watson | 1.98235 | 通過 |
| Jarque–Bera p-value | 0.26403 | 通過 |
| Breusch–Pagan p-value | 0.55601 | 通過 |
| Maximum VIF | 16.47581 | 有疑慮 |

VIF 顯示部分特徵仍有多重共線性疑慮；係數方向與大小必須保守解讀。各門檻是診斷警示，不能證明統計假設必然成立。

50 Startups 的 Breusch–Pagan p-value 為 0.01245，顯示同質變異有疑慮；Maximum VIF 為 2.69894。由於測試集只有 10 筆，診斷與 Adjusted R² 對樣本大小敏感。

## 6. Deployment

本地執行：

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Web 已包含兩個預設題、Custom HTTPS CSV／上傳 fallback、資料品質、模型比較、下載與錯誤提示。Streamlit Community Cloud 可直接使用 `app.py` 與 `requirements.txt`。

- GitHub：[AIot_20261029_HW2](https://github.com/cotaj6011-coder/AIot_20261029_HW2)
- Live Web：[Regression Studio](https://aiot20261029hw2-te9ncekg3z38qqt5muuddj.streamlit.app/)
- 公開環境截圖：[`Dashboard 首頁`](screenshots/dashboard-home.png)、[`模型評估與預測圖表`](screenshots/model-evaluation-complete.png)

## 7. NotebookLM 比較研究

- NotebookLM 實際研究日期：**2026-10-31**
- 原始匯出佐證：[`Human–AI Trust 比較研究報告.md`](Human%E2%80%93AI%20Trust%20%E6%AF%94%E8%BC%83%E7%A0%94%E7%A9%B6%E5%A0%B1%E5%91%8A.md)
- 專案背景來源：[`HW2_NOTEBOOKLM_CONTEXT.md`](HW2_NOTEBOOKLM_CONTEXT.md)

原始 NotebookLM 匯出檔保留不覆寫；本節將其內容整理成正式 Markdown，並依 HW2 現行程式及 2026-10-31 重算結果校正數值與方法描述。

### NotebookLM 摘要

本研究旨在以多元線性回歸評估人機信任（Human–AI Trust）之預測效能與限制。依人類信任 AI 的實證回顧與信任自動化整合模型，信任會受到系統效能、呈現形式、個人特質、情境與習得經驗共同影響（Glikson & Woolley, 2020；Hoff & Bashir, 2015）。NIST AI RMF 則從風險治理角度提出有效可靠、安全、可解釋、公平與偏誤管理等可信 AI 特性（NIST, 2023）；它是管理框架，而不是人類信任形成機制的實證研究。HW2 依循 scikit-learn 的資料洩漏防範原則，以 Pipeline 整合缺失值補值、標準化、One-Hot 編碼與特徵選擇，並透過訓練集內 5-fold CV 選擇特徵數。實驗顯示，Selected 模型使用 15 個編碼特徵，R² 為 0.6814、Adjusted R² 為 0.6790；Baseline 使用 30 個編碼特徵，R² 為 0.6815、Adjusted R² 為 0.6766。兩者預測效能差異極小，在未做配對或重抽樣檢定前不可宣稱差異顯著，但 Selected 模型確實減少一半特徵並維持相近解釋力。Selected 模型 Maximum VIF 為 16.48，顯示多重共線性疑慮，個別係數需保守解讀。由於資料是合成教育資料，結果僅適合教學與關聯分析，不能賦予因果意義或直接外推至真實人群。後續可比較 Ridge／Lasso、RFECV，並在交換性條件成立時評估共形預測的邊際涵蓋率。

### 可信 AI 管理框架與人類信任實證研究的區分

- **人類信任的實證與理論整合**：Glikson 與 Woolley（2020）回顧人類信任 AI 的實證研究；Hoff 與 Bashir（2015）整合特質、情境與習得信任等影響因素。兩者可用來討論人類如何形成、調整或失去對自動化／AI 的信任。
- **可信 AI 的治理框架**：NIST AI RMF 1.0 描述 AI 系統在風險管理上應追求的可信特性與治理活動（NIST, 2023）。它可用來檢視有效可靠、安全、透明可解釋、隱私與公平等治理面向，但不能直接當作「這些特性必然提高人類主觀信任」的實證證據。
- **HW2 的定位**：HW2 使用合成資料預測 `latent_trust_score`，只能比較欄位與目標的統計關聯。即使欄位名稱與上述理論或治理構面相似，也不能據此主張心理機制或因果效果已被驗證。

### 外部研究與 HW2 實作比較表

| 研究議題 | 外部研究／技術觀點 | HW2 實際方法與結果 | 差異、限制與改善建議 |
| --- | --- | --- | --- |
| 信任影響因素與特徵構型 | Glikson 與 Woolley（2020）整理 AI 能力、呈現與人機互動相關實證；Hoff 與 Bashir（2015）提出特質、情境與習得信任層次。NIST（2023）則是可信 AI 風險管理框架，不是人類信任的實證模型。 | 使用 20 個原始特徵，涵蓋年齡、技術經驗、模型準確度、可解釋性、偏誤、錯誤率、認知負荷、任務風險與情境因素。 | 欄位名稱與部分理論／治理構面相似，但資料是合成資料且沒有經驗證的心理量表；未來應蒐集真實問卷與行為資料。 |
| 資料準備與資料洩漏 | scikit-learn 建議先切分資料，並以 Pipeline 確保前處理只在訓練資料 fit（scikit-learn developers, n.d.-b）。 | 10,100 列中有 201 列 Target 缺值；移除後 9,899 列，以固定 seed 切為 7,919 筆訓練與 1,980 筆測試。Imputer、Scaler、Encoder、Selector 全部位於 Pipeline。 | 符合主要資料洩漏防範原則；測試集不參與缺失值統計、編碼或 k 的選擇。 |
| 特徵選擇 | `SelectKBest`／`f_regression` 是單變量過濾方法；官方文件另列 model-based 與 sequential selection 方法（scikit-learn developers, n.d.-a）。 | 30 個編碼特徵以訓練集 5-fold CV 比較 k=5、10、15、20、30，選出 k=15。 | 單變量評分忽略聯合效應與交互作用；可比較 Lasso `SelectFromModel`、RFECV 或 SequentialFeatureSelector，但不能以測試集挑選方法。 |
| 模型效能 | 外部文獻提供信任因素與方法背景，不能取代本專案的測試集評估。 | Baseline：MAE 4.15073、RMSE 5.18519、R² 0.68148；Selected：MAE 4.15029、RMSE 5.18582、R² 0.68140。 | 指標差異極小，沒有統計檢定證據支持「Selected 顯著優於 Baseline」；可用重複交叉驗證或 bootstrap 比較穩定性。 |
| 多重共線性 | VIF 用於衡量設計矩陣欄位被其他欄位解釋的程度；statsmodels 文件說明 VIF 的計算與常用判讀（statsmodels developers, n.d.-b）。 | Selected 模型 Maximum VIF = 16.47581，高於專案門檻 5。 | 代表至少部分係數存在共線性疑慮與變異膨脹，但不能推論所有係數都無效；可比較 Ridge、Lasso、ElasticNet 或 PCA。 |
| 95% 預測區間 | OLS prediction API 可為新觀測提供預測結果與區間資訊（statsmodels developers, n.d.-a）。 | 使用 Selected Pipeline 的相同 15 維特徵空間，以訓練殘差計算 95% OLS observation prediction interval；rank=16、dof=7,903，未用測試殘差校準。 | 已驗證 `lower <= prediction <= upper`，但這只證明界線順序，不代表經驗涵蓋率等於 95%；應另外計算 coverage 與平均區間寬度。 |
| 共形預測 | 共形預測常被稱為 distribution-free／非參數式，但**並非完全無假設**；有限樣本的邊際涵蓋率保證要求校準樣本與待預測樣本具有交換性，i.i.d. 是常見的充分條件。 | HW2 目前沒有實作共形預測，只實作 OLS observation prediction interval。 | 未來若加入 split conformal，必須以訓練資料內部切出校準集，不可用測試殘差校準；若有時間序列、分布漂移或群組相依，交換性可能不成立，涵蓋率保證也可能失效。 |

### NotebookLM 限制分析與改善建議

#### 1. 實驗結果的客觀解讀

- Baseline 的 R² 為 0.68147596、RMSE 為 5.18518766；Selected 的 R² 為 0.68139830、RMSE 為 5.18581973。差異很小，未經推估統計檢定前不可宣稱有顯著差異。
- Selected 的 Adjusted R² 為 0.67896499，高於 Baseline 的 0.67657308；這表示在目前資料與公式下，較少特徵得到略高的複雜度調整分數，但不能證明已「消除雜訊」。
- Maximum VIF 16.47581 代表部分入選特徵仍有強烈線性相依疑慮，會影響係數穩定性；它不等於所有係數都不可靠。

#### 2. 資料來源與外部效度

- Kaggle Human–AI Interaction 資料共有 10,100 列；移除 201 列 Target 缺值後，有效建模資料為 9,899 列。資料為合成教育資料，數值關係不能視為真實人群的心理或社會機制。
- 多元線性回歸估計的是條件線性關聯，不能把係數解讀成因果效果，例如不能主張單獨提高可解釋性分數必然造成等幅信任提升。
- 20 個欄位不是經本專案驗證的心理量表；外部研究的理論概念與資料欄位只能做概念比較。

#### 3. 方法改善

- 可使用 Ridge、Lasso 或 ElasticNet 比較正則化對係數穩定性與泛化誤差的影響；仍須在訓練資料內完成調參。
- 可比較 Lasso `SelectFromModel`、RFECV 或 SequentialFeatureSelector，評估單變量特徵選擇是否遺漏聯合效應。
- 應報告預測區間的經驗涵蓋率與平均寬度，而非只檢查上下界順序。
- 若加入共形預測，應明確說明交換性假設、校準集來源及資料漂移風險；「非參數」或「分布無關」不代表不需要任何資料假設。

### 外部參考文獻

下列 7 筆來源依作者年份格式統一。兩篇期刊論文的 DOI、作者與標題已用 Crossref metadata 核對；五個技術／框架頁面為官方文件。`n.d.` 表示頁面沒有穩定的正式出版年份，不以目前套件版本或存取年份冒充出版年份。

1. Glikson, E., & Woolley, A. W. (2020). Human trust in artificial intelligence: Review of empirical research. *Academy of Management Annals, 14*(2), 627–660. <https://doi.org/10.5465/annals.2018.0057>
2. Hoff, K. A., & Bashir, M. (2015). Trust in automation: Integrating empirical evidence on factors that influence trust. *Human Factors, 57*(3), 407–434. <https://doi.org/10.1177/0018720814547570>
3. National Institute of Standards and Technology. (2023). *Artificial Intelligence Risk Management Framework (AI RMF 1.0): Characteristics of trustworthy AI systems*. <https://airc.nist.gov/airmf-resources/airmf/3-sec-characteristics/>
4. scikit-learn developers. (n.d.-a). *Feature selection*. <https://scikit-learn.org/stable/modules/feature_selection.html>
5. scikit-learn developers. (n.d.-b). *Common pitfalls and recommended practices*. <https://scikit-learn.org/stable/common_pitfalls.html>
6. statsmodels developers. (n.d.-a). *OLSResults.get_prediction*. <https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLSResults.get_prediction.html>
7. statsmodels developers. (n.d.-b). *variance_inflation_factor*. <https://www.statsmodels.org/stable/generated/statsmodels.stats.outliers_influence.variance_inflation_factor.html>

## 8. GPT 輔助內容

Codex 協助需求拆解、資料來源核實、Streamlit Dashboard、Pipeline、URL 安全、特徵選擇、區間估計、自動化測試、UI 重構、部署及除錯。GPT/Codex 也協助把 NotebookLM 匯出內容整理為 Markdown、統一引用格式、核對文獻 URL，以及把共形預測描述修正為須滿足交換性條件。模型數值由實際程式重算並以測試核實；外部研究結論以 NotebookLM 原始匯出與所列來源為依據，AI 文字不視為未經驗證的實驗證據。
