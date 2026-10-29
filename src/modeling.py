from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline

from .preprocessing import build_preprocessor
from .validation import validate_analysis_data

RANDOM_STATE = 42
MAX_ANALYSIS_ROWS = 30_000


@dataclass
class AnalysisResult:
    baseline: Pipeline
    selected: Pipeline
    comparison: pd.DataFrame
    selected_names: list[str]
    coefficients: pd.DataFrame
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series
    baseline_predictions: np.ndarray
    predictions: np.ndarray
    intercept: float
    transformed_feature_count: int
    raw_feature_map: pd.DataFrame
    source_rows: int
    analysis_rows: int
    sampled: bool


def _pipeline(frame, features, k="all") -> Pipeline:
    return Pipeline([
        ("preprocessor", build_preprocessor(frame, features)),
        ("selector", SelectKBest(score_func=f_regression, k=k)),
        ("regressor", LinearRegression()),
    ])


def original_feature_name(transformed_name: str, features: list[str]) -> str:
    clean = transformed_name.split("__", 1)[-1]
    exact = [feature for feature in features if clean == feature]
    if exact:
        return exact[0]
    categorical = [feature for feature in features if clean.startswith(f"{feature}_")]
    return max(categorical, key=len) if categorical else clean


def run_analysis(frame: pd.DataFrame, target: str, excluded=()) -> AnalysisResult:
    features, _ = validate_analysis_data(frame, target, excluded)
    clean = frame.dropna(subset=[target]).copy()
    source_rows = len(clean)
    if source_rows > MAX_ANALYSIS_ROWS:
        clean = clean.sample(MAX_ANALYSIS_ROWS, random_state=RANDOM_STATE).sort_index()
    sampled = len(clean) < source_rows
    X, y = clean[features], clean[target].astype(float)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )
    cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    probe = build_preprocessor(frame, features).fit(X_train)
    transformed_count = len(probe.get_feature_names_out())
    candidates = sorted(set([min(k, transformed_count) for k in (5, 10, 15, 20, transformed_count)]))
    rows = []
    for k in candidates:
        model = _pipeline(frame, features, k)
        scores = -cross_val_score(model, X_train, y_train, cv=cv,
                                  scoring="neg_root_mean_squared_error")
        rows.append({"k": k, "CV RMSE": scores.mean(), "CV RMSE SD": scores.std()})
    best_k = min(rows, key=lambda row: row["CV RMSE"])["k"]
    baseline, selected = _pipeline(frame, features), _pipeline(frame, features, best_k)
    baseline.fit(X_train, y_train)
    selected.fit(X_train, y_train)
    baseline_predictions = baseline.predict(X_test)
    predictions = selected.predict(X_test)
    all_names = selected.named_steps["preprocessor"].get_feature_names_out()
    mask = selected.named_steps["selector"].get_support()
    selected_names = all_names[mask].tolist()
    raw_feature_map = pd.DataFrame({
        "編碼後特徵": selected_names,
        "原始欄位": [original_feature_name(name, features) for name in selected_names],
    })
    coefficients = pd.DataFrame({
        "feature": selected_names,
        "coefficient": selected.named_steps["regressor"].coef_,
    }).sort_values("coefficient", key=abs, ascending=False)
    comparison = pd.DataFrame(rows)
    comparison["selected"] = comparison["k"].eq(best_k)
    return AnalysisResult(baseline, selected, comparison, selected_names, coefficients,
                          X_train, X_test, y_train, y_test,
                          baseline_predictions, predictions,
                          float(selected.named_steps["regressor"].intercept_),
                          transformed_count, raw_feature_map, source_rows, len(clean), sampled)

