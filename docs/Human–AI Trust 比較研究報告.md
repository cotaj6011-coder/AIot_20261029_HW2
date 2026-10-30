# Human–AI Trust 比較研究報告

本報告以 **HW2 多元線性回歸專案背景與實驗紀錄**（HW2\_NOTEBOOKLM\_CONTEXT.md） 為實作分析對象，對照 **Glikson & Woolley (2020)**、**Hoff & Bashir (2015)**、**NIST AI RMF (2023)** 以及 **scikit-learn** 與 **statsmodels** 官方技術規範，進行 Human–AI Trust Prediction 之研究方法與實驗結果比較分析。

## A. NotebookLM 研究摘要

本研究旨在以多元線性回歸評估人機信任（Human–AI Trust）之預測效能與限制。參照 Glikson & Woolley (2020) 與 Hoff & Bashir (2015) 之信任層級架構，以及 NIST (2023) 之可信 AI 規範，人機信任受系統效能、可解釋性、偏誤與個人/情境因素綜合驅動。HW2 實作依循 scikit-learn 最佳實踐，採用 Pipeline 整合預處理以嚴格防範資料洩漏，並透過 5-fold CV 進行特徵選擇。實驗結果顯示，Selected 模型（15 個編碼特徵，R²=0.6814，Adjusted R²=0.6790）與 Baseline 模型（30 個編碼特徵，R²=0.6815，Adjusted R²=0.6766）之預測效能差異極小，在未做統計檢定下不可宣稱具顯著差異，但成功實現模型結構精簡。診斷顯示 Selected 模型 Maximum VIF 達 16.48，反映多重共線性疑慮，導致部分係數估計之標準誤膨脹。由於 HW2 採用合成資料，研究結果僅具關聯分析與教學價值，不可賦予因果解釋或直接外推至真實人群。未來建議導入 Ridge/Lasso 正則化迴歸或共形預測／共形校準以優化模型實用性。

## B. 外部研究方法與 HW2 實作比較表

研究議題,外部研究觀點,HW2 實際方法,差異與改善建議  
信任影響因素與特徵構型,Glikson & Woolley (2020) 將 AI 信任劃分為系統呈現形式與智慧水準；Hoff & Bashir (2015) 提出特質、情境與習得信任三層架構；NIST AI RMF (2023) 強調有效性、可靠性、可解釋性、公平性與偏誤管理等維度。,納入 20 個原始特徵（涵蓋年齡、技術經驗、AI 模型準確度、可解釋性分數、偏誤程度、認知負荷與任務風險等）。,特徵欄位與理論構面大致吻合，但合成資料缺乏真實心理測量指標；建議未來收集真實使用者之主觀信任問卷與行為數據。  
資料準備與資料洩漏防範,"scikit-learn 官方規範強調必須先進行 Train/Test 切分，且所有預處理轉換器（Imputer, Scaler, Encoder）僅能於訓練集 fit，嚴格禁止測試集資訊洩漏至訓練過程。","將 9,899 筆有效資料切分為 7,919 筆訓練集與 1,980 筆測試集，使用 Pipeline 與 ColumnTransformer 串接預處理，僅在訓練集 fit。",做法符合主要資料洩漏防範原則。  
特徵選擇機制,scikit-learn 指出單變量篩選（如 SelectKBest）僅評估單一特徵與目標之獨立線性關係；多變量情境建議採用 Lasso (L1) 懲罰之 SelectFromModel、RFECV 或 SequentialFeatureSelector。,在訓練集內以 5-fold CV 搭配 SelectKBest(score\_func=f\_regression)，自 30 個編碼特徵中選出 15 個最佳特徵。,單變量評分忽視了特徵間之組合效應與多重共線性；建議改採 Lasso 正則化（SelectFromModel）或 RFECV 進行多變量特徵篩選。  
多重共線性與模型診斷,statsmodels 技術文件指明 VIF \> 5 代表存在高程度多重共線性，會導致迴歸估計值之標準誤膨脹、敏感度增加。,Selected 模型經診斷其設計矩陣之 Maximum VIF 為 16.48（高於 5 之常用門檻）。,建模前未預先處理解降維。VIF 高代表部分高度相關特徵存在共線性疑慮，致個別係數不確定性增加；建議採用 Ridge/Lasso 迴歸懲罰或 PCA 降維。  
不確定性區間估計,statsmodels 透過 OLS 計算新觀測值之 Observation Prediction Interval，同時涵蓋參數估計變異與隨機誤差變異。,建構 95% OLS Observation Prediction Interval，並確認測試集所有預測值均符合 lower \<= prediction \<= upper 之順序。,僅驗證數值上下界順序邏輯，未實測經驗涵蓋率（Empirical Coverage Rate）；建議導入共形預測／共形校準（Conformal Prediction / Conformal Calibration）評估真實涵蓋率（在滿足資料可交換性等前提下提供邊際涵蓋率保證）。

## C. HW2 的研究限制與改善建議

### 1\. 學術表述修正與實驗結果客觀解讀

* **預測效能差異極小**：HW2 實驗中，Baseline 模型（30 個編碼特徵）在測試集的 R² 為 0.6815、RMSE 為 5.1852；Selected 模型（15 個編碼特徵）測試集 R² 為 0.6814、RMSE 為 5.1858。兩者 R² 差異極微（僅 0.0001），在未進行推估統計檢定（如 Paired t-test 或 Bootstrap 檢定）之前，應客觀描述為預測效能差異極小，**不可**逕自宣稱具顯著差異。  
* **模型精簡非證明消除雜訊**：Selected 模型的 Adjusted R² 由 0.6766 微幅上升至 0.6790。這僅代表在特徵數量減少 50% 的情況下，模型實現了結構上的精簡（符合 Occam's Razor 原則）並維持相當的解釋力，**不能**直接證明其完全消除了數據雜訊。  
* **多重共線性之合理推論**：Selected 模型的最大 VIF 為 16.48，高於常用評估門檻 5。這反映入選的 15 個特徵間仍存在強烈的線性相依，會導致部分迴歸係數之標準誤膨脹。但這**不代表所有係數都不可靠**，僅意味著不可將單一係數直接解讀為獨立的邊際影響力，需謹慎看待個案估計值的穩定性。

### 2\. 資料來源與外部效度限制

* **合成資料限制**：HW2 使用之 Kaggle 資料集（human\_ai\_interaction.csv）為 10,100 筆（有效建模 9,899 筆）之**合成教育資料**。變數間之數值關係由統計生成演算法設定，無法反映真實人群在真實情境下的心理、情境與社會動態機制。因此，本研究結果**無法外推**至真實使用者對 AI 的信任行為。  
* **相關性不等於因果關係**：多元線性回歸所估計之迴歸係數僅代表變數間之統計關聯，**絕不可**賦予因果解釋（例如不能推論「提高可解釋性分數必能直接等幅提升真實信任」）。

### 3\. 方法論改善建議

* **特徵選擇方法升級**：目前使用的 SelectKBest(score\_func=f\_regression) 為單變量過濾法，忽視了特徵之間的交互作用。建議未來改用具備多變量感知能力的方法，例如結合 Lasso L1 懲罰之 SelectFromModel、RFECV 或 SequentialFeatureSelector。  
* **共線性與多變量結構處置**：針對 VIF 高達 16.48 的多重共線性問題，建議採用正則化迴歸（Ridge 或 ElasticNet）約束係數變異，或以主成分分析（PCA）轉換為正交特徵後再行建模。  
* **區間估計驗證**：目前針對 95% OLS Prediction Interval 僅檢驗數值邊界順序。建議未來導入經驗涵蓋率（Empirical Coverage Rate）之實證計算，或使用符合非母數假設之\*\*共形預測／共形校準（Conformal Prediction / Conformal Calibration）\*\*技術，在滿足資料可交換性（Exchangeability）等前提下，提供邊際涵蓋率（Marginal Coverage）保證的不確定性量化。

## D. 外部參考文獻清單

1. **Glikson, E., & Woolley, A. W. (2020).** Human Trust in Artificial Intelligence: Review of Empirical Research. *Academy of Management Annals*, 14(2), 627–660.URL: https\://doi.org/10.5465/annals.2018.0057 (Figshare 典藏連結: https\://doi.org/10.1184/R1/19500545)  
2. **Hoff, K. A., & Bashir, M. (2015).** Trust in Automation: Integrating Empirical Evidence on Factors That Influence Trust. *Human Factors*, 57(3), 407–434.URL: https\://doi.org/10.1177/0018720814547570  
3. **NIST (2023).** Artificial Intelligence Risk Management Framework (AI RMF 1.0): AI Risks and Trustworthiness. *National Institute of Standards and Technology*, U.S. Department of Commerce.URL: https\://airc.nist.gov/airmf-resources/airmf/3-sec-characteristics/  
4. **scikit-learn developers (2026).** 1.13. Feature selection — scikit-learn 1.9.1 documentation.URL: https\://scikit-learn.org/stable/modules/feature\_selection.html  
5. **scikit-learn developers (2026).** 12\. Common pitfalls and recommended practices — scikit-learn 1.9.1 documentation.URL: https\://scikit-learn.org/stable/common\_pitfalls.html  
6. **statsmodels developers (2025).** statsmodels.regression.linear\_model.OLSResults.get\_prediction — statsmodels 0.15.0 documentation.URL: https\://www\.statsmodels.org/stable/generated/statsmodels.regression.linear\_model.OLSResults.get\_prediction.html  
7. **statsmodels developers (2023).** statsmodels.stats.outliers\_influence.variance\_inflation\_factor — statsmodels 0.14.6 documentation.URL: https\://www\.statsmodels.org/v0.14.6/generated/statsmodels.stats.outliers\_influence.variance\_inflation\_factor.html

