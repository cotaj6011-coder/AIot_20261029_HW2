# 多元線性回歸 Web 專案報告

> 本報告數值由 `scripts/generate_report_evidence.py` 在 2026-10-29 實際重算，不是人工填造。正式提交前請補上部署網址、截圖、NotebookLM 真實摘要與對話 PDF。

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

- GitHub：`WAITING_FOR_USER`
- Live Web：`WAITING_FOR_USER`
- 公開環境截圖：`WAITING_FOR_USER`

## 研究限制

- Human–AI 資料是合成資料，外部效度有限。
- `f_regression` 是單變量特徵評分，不能識別所有交互作用。
- OLS 假設診斷只提供警示；共線性會降低係數穩定性。
- Custom URL 的欄位語意與授權由使用者確認。
- 大於 30,000 筆時的固定抽樣是部署資源策略，結果可能與全資料模型不同。
- 本作業比較的核心模型保持 `LinearRegression`，沒有用更複雜模型取代作業要求。

## GPT 輔助內容

Codex 協助需求拆解、資料來源核實、Streamlit Dashboard、Pipeline、URL 安全、特徵選擇、區間估計、自動化測試、UI 重構及除錯。數值由程式重算並以測試核實；AI 文字不視為未驗證實驗證據。

## NotebookLM 摘要

`WAITING_FOR_USER`：請本人將同主題研究來源加入 NotebookLM，填入至少 100 個中文字的真實摘要、來源 URL、研究日期及與本專案方法的比較。不可用此欄位冒充已完成研究。
