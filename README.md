# HW2 多元線性回歸 Web 專案

以 Streamlit 實作現代化 ML Dashboard 與完整 CRISP-DM 流程，包含兩個可執行預設回歸題、任意公開 HTTPS CSV、`LinearRegression`、訓練集內 5-fold CV 特徵選擇、MAE/MSE/RMSE/R²、95% OLS prediction interval 與殘差/假設診斷。

## Dashboard 功能

- Hero、深色 Sidebar、六階段 CRISP-DM Tabs、KPI 卡與響應式版型。
- 資料型別、敘述統計、缺失率、重複特徵、疑似 ID、常數欄及清理策略。
- Baseline／Selected 比較、CV 選 k 紀錄、原始與編碼後特徵對應、係數及截距。
- 統一 Plotly 視覺主題、95% 預測區間、殘差圖與五項診斷卡。
- 快取內建資料、公開 URL 與模型結果；切換 Problem 會清除不相容狀態。
- 超過 30,000 筆時固定 seed 抽樣並明確揭露，避免免費部署資源耗盡。

## 執行方式

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## 資料來源

- Problem A：[Human–AI Interaction（Kaggle）](https://www.kaggle.com/datasets/eshaalnmalik/human-ai-interaction)，CC0、合成教育資料。10,100 筆、20 個原始特徵、target `latent_trust_score`，是正式符合 14–39 特徵的 Kaggle 回歸題。
- Problem B：[50 Startups](https://raw.githubusercontent.com/Avik-Jain/100-Days-Of-ML-Code/master/datasets/50_Startups.csv)，沿用 DIC2 設計，target `Profit`。它只有 4 個原始特徵，不宣稱符合正式選題門檻。
- 原規格 Flood competition 需要登入並接受 Kaggle 規則，官方 API 匿名下載實測為 HTTP 401，因此未將未授權鏡像或假資料默默替代。若取得 `train.csv`，可由 Custom 模式上傳並選 `FloodProbability`。

## 操作

選 Problem → 檢視來源與資料 → 確認 target/排除欄 → 執行完整回歸分析 → 查看模型比較、區間與診斷 → 下載 CSV。Custom URL 僅接受公開 HTTPS，拒絕私有位址、重新導向至私有位址、HTML、超限資料；另提供 CSV 上傳 fallback。

完整實測數值與限制見 [`docs/REPORT.md`](docs/REPORT.md)，逐階段證據見 [`docs/GOAL_STATUS.md`](docs/GOAL_STATUS.md)。

本機視覺驗收截圖：[`ui-desktop.png`](ui-desktop.png)（桌面版）與 [`ui-mobile.png`](ui-mobile.png)（430px 響應式版）。

指定驗證 URL：

`https://raw.githubusercontent.com/Avik-Jain/100-Days-Of-ML-Code/master/datasets/50_Startups.csv`

## 部署

Streamlit Community Cloud：建立 GitHub repo、將 `app.py` 設為入口、使用 `requirements.txt`。部署後依 `docs/SUBMISSION_CHECKLIST.md` 以無痕視窗驗證。

- GitHub Repo：[AIot_20261029_HW2](https://github.com/cotaj6011-coder/AIot_20261029_HW2)
- Live Web：`WAITING_FOR_USER`

## 已知限制

- VIF 在高維或奇異設計矩陣會標示不適用。
- OLS prediction interval 使用所選模型的相同前處理/特徵空間與訓練殘差，不以測試殘差校準。
- Custom URL 的 DNS 安全檢查仍受部署平台網路與 DNS 行為影響；受限環境請改用上傳。
- Human–AI Selected 模型的 VIF 仍顯示共線性疑慮；畫面與報告均如實呈現。
- 大於 30,000 筆資料會以固定 seed 抽樣；畫面會顯示原始與實際分析筆數。

