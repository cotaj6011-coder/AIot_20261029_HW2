from __future__ import annotations

import numpy as np
from scipy.stats import t


def ols_prediction_intervals(model, X_train, y_train, X_new, alpha=.05):
    """Use the selected pipeline's exact transformed feature space; never calibrate on test residuals."""
    prep, selector, reg = (model.named_steps[name] for name in ("preprocessor", "selector", "regressor"))
    train = selector.transform(prep.transform(X_train))
    new = selector.transform(prep.transform(X_new))
    train_design = np.column_stack([np.ones(len(train)), train])
    new_design = np.column_stack([np.ones(len(new)), new])
    beta = np.r_[reg.intercept_, reg.coef_]
    fitted = train_design @ beta
    residuals = np.asarray(y_train) - fitted
    rank = np.linalg.matrix_rank(train_design)
    dof = len(train_design) - rank
    if dof <= 0:
        raise ValueError("訓練樣本不足以估計預測區間。")
    mse = float(residuals @ residuals / dof)
    inverse = np.linalg.pinv(train_design.T @ train_design)
    predictions = new_design @ beta
    leverage = np.einsum("ij,jk,ik->i", new_design, inverse, new_design)
    margin = t.ppf(1 - alpha / 2, dof) * np.sqrt(mse * (1 + leverage))
    return predictions, predictions - margin, predictions + margin, {
        "method": "OLS observation prediction interval", "dof": dof, "rank": rank
    }

