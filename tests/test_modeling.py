import numpy as np
import pandas as pd
import pytest

from src.datasets import load_builtin
from src.evaluation import regression_metrics
from src.intervals import ols_prediction_intervals
from src.modeling import MAX_ANALYSIS_ROWS, run_analysis
from src.validation import quality_summary, validate_analysis_data


@pytest.fixture(scope="module")
def startup_result():
    frame, spec = load_builtin("startups")
    return frame, spec, run_analysis(frame, spec.target)


def test_reproducible_split_features_and_metrics():
    frame, spec = load_builtin("startups")
    first = run_analysis(frame, spec.target)
    second = run_analysis(frame, spec.target)
    assert first.X_test.index.tolist() == second.X_test.index.tolist()
    assert first.selected_names == second.selected_names
    assert np.allclose(first.predictions, second.predictions)


def test_formal_kaggle_problem_runs_complete_analysis():
    frame, spec = load_builtin("human_ai")
    result = run_analysis(frame, spec.target)
    metrics = regression_metrics(result.y_test, result.predictions, len(result.selected_names))
    prediction, lower, upper, _ = ols_prediction_intervals(
        result.selected, result.X_train, result.y_train, result.X_test
    )
    assert 14 <= len([c for c in frame if c != spec.target]) <= 39
    assert set(("MAE", "MSE", "RMSE", "R²")) <= metrics.keys()
    assert len(prediction) == len(lower) == len(upper) == len(result.y_test)


def test_pipeline_handles_missing_and_unknown_category():
    frame, spec = load_builtin("startups")
    frame.loc[0, "Administration"] = np.nan
    result = run_analysis(frame, spec.target)
    new = result.X_test.iloc[:1].copy()
    new["State"] = "Unknown State"
    prediction = result.selected.predict(new)
    assert np.isfinite(prediction).all()


def test_extreme_test_values_do_not_change_fitted_training_transformers(startup_result):
    _, _, result = startup_result
    before = result.selected.named_steps["preprocessor"].transform(result.X_train)
    changed_test = result.X_test.copy()
    changed_test.loc[:, "R&D Spend"] = 1e15
    result.selected.predict(changed_test)
    after = result.selected.named_steps["preprocessor"].transform(result.X_train)
    assert np.allclose(before, after)


def test_metrics_rmse_identity_and_degenerate():
    metrics = regression_metrics([1, 2, 3], [1, 2, 3], 1)
    assert metrics["RMSE"] == pytest.approx(np.sqrt(metrics["MSE"]))
    assert metrics["R²"] == 1


def test_prediction_intervals_are_ordered_and_aligned(startup_result):
    _, _, result = startup_result
    prediction, lower, upper, info = ols_prediction_intervals(
        result.selected, result.X_train, result.y_train, result.X_test
    )
    assert len(prediction) == len(result.y_test)
    assert np.all(lower <= prediction)
    assert np.all(prediction <= upper)
    assert info["dof"] > 0


@pytest.mark.parametrize("frame,target", [
    (pd.DataFrame({"x": range(20), "y": ["a"] * 20}), "y"),
    (pd.DataFrame({"target": range(19), "x": range(19)}), "target"),
    (pd.DataFrame({"target": range(20)}), "target"),
])
def test_invalid_targets_and_shapes(frame, target):
    with pytest.raises(ValueError):
        validate_analysis_data(frame, target)


def test_missing_and_nonfinite_target_are_rejected():
    frame = pd.DataFrame({"feature": range(20), "target": np.arange(20, dtype=float)})
    with pytest.raises(ValueError, match="找不到指定 target"):
        validate_analysis_data(frame, "missing")
    frame.loc[0, "target"] = np.inf
    with pytest.raises(ValueError, match="target 包含無限值"):
        validate_analysis_data(frame, "target")


def test_quality_summary_finds_missing_identifier_constant_and_duplicate():
    frame = pd.DataFrame({
        "id": range(20), "a": [*range(10), *([np.nan] * 10)],
        "a_copy": [*range(10), *([np.nan] * 10)], "constant": [3] * 20,
        "target": range(20),
    })
    features, constants = validate_analysis_data(frame, "target")
    summary = quality_summary(frame, "target", features)
    assert constants == ["constant"]
    assert summary["suspected_identifiers"] == ["id"]
    assert summary["duplicate_feature_groups"] == [["a", "a_copy"]]


def test_large_data_sampling_is_deterministic():
    rows = MAX_ANALYSIS_ROWS + 100
    rng = np.random.default_rng(7)
    frame = pd.DataFrame({"x1": rng.normal(size=rows), "x2": rng.normal(size=rows)})
    frame["target"] = 3 * frame["x1"] - frame["x2"] + rng.normal(scale=.1, size=rows)
    first = run_analysis(frame, "target")
    second = run_analysis(frame, "target")
    assert first.sampled and first.analysis_rows == MAX_ANALYSIS_ROWS
    assert first.X_test.index.tolist() == second.X_test.index.tolist()

