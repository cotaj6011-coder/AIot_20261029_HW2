from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson


def regression_metrics(y_true, predictions, p: int) -> dict:
    mse = mean_squared_error(y_true, predictions)
    n = len(y_true)
    r2 = r2_score(y_true, predictions)
    adjusted = np.nan if n <= p + 1 else 1 - (1 - r2) * (n - 1) / (n - p - 1)
    return {"MAE": mean_absolute_error(y_true, predictions), "MSE": mse,
            "RMSE": np.sqrt(mse), "R²": r2, "Adjusted R²": adjusted}


def diagnostics(y_true, predictions, design_train: np.ndarray) -> tuple[pd.DataFrame, np.ndarray]:
    residuals = np.asarray(y_true) - np.asarray(predictions)
    rows = []
    corr = np.corrcoef(predictions, residuals)[0, 1] if len(residuals) > 2 else np.nan
    rows.append(("線性關係", abs(corr), "通過" if abs(corr) < .2 else "有疑慮", "|corr(ŷ, residual)| < 0.2"))
    dw = durbin_watson(residuals)
    rows.append(("誤差獨立性", dw, "通過" if 1.5 <= dw <= 2.5 else "有疑慮", "Durbin–Watson 1.5–2.5"))
    jb = stats.jarque_bera(residuals)
    rows.append(("殘差近似常態", jb.pvalue, "通過" if jb.pvalue > .05 else "有疑慮", "Jarque–Bera p > 0.05"))
    try:
        exog = np.column_stack([np.ones(len(predictions)), predictions])
        bp = het_breuschpagan(residuals, exog)
        rows.append(("同質變異", bp[1], "通過" if bp[1] > .05 else "有疑慮", "Breusch–Pagan p > 0.05"))
    except ValueError:
        rows.append(("同質變異", np.nan, "不適用", "樣本不足"))
    try:
        matrix = np.asarray(design_train, dtype=float)
        vifs = [variance_inflation_factor(matrix, i) for i in range(matrix.shape[1])]
        max_vif = float(np.nanmax(vifs))
        rows.append(("多重共線性", max_vif, "通過" if max_vif < 5 else "有疑慮", "Maximum VIF < 5"))
    except Exception:
        rows.append(("多重共線性", np.nan, "不適用", "設計矩陣奇異或維度不適用"))
    return pd.DataFrame(rows, columns=["檢查", "統計量", "判定", "準則/限制"]), residuals

