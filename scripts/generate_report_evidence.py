"""Print verified built-in dataset evidence for REPORT.md; does not modify artifacts."""
from pathlib import Path
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.datasets import load_builtin
from src.evaluation import diagnostics, regression_metrics
from src.intervals import ols_prediction_intervals
from src.modeling import run_analysis


for dataset_id in ("human_ai", "startups"):
    frame, spec = load_builtin(dataset_id)
    result = run_analysis(frame, spec.target)
    train_design = result.selected.named_steps["selector"].transform(
        result.selected.named_steps["preprocessor"].transform(result.X_train)
    )
    diagnosis, _ = diagnostics(result.y_test, result.predictions, train_design)
    baseline = regression_metrics(result.y_test, result.baseline_predictions, result.transformed_feature_count)
    selected = regression_metrics(result.y_test, result.predictions, len(result.selected_names))
    _, lower, upper, interval = ols_prediction_intervals(
        result.selected, result.X_train, result.y_train, result.X_test
    )
    print(f"DATASET={dataset_id}")
    print(f"SHAPE={frame.shape[0]}x{frame.shape[1]}")
    print(f"RAW_FEATURES={frame.shape[1] - 1}; ENCODED={result.transformed_feature_count}; SELECTED={len(result.selected_names)}")
    print("SELECTED_NAMES=" + "|".join(result.selected_names))
    for model, metrics in (("BASELINE", baseline), ("SELECTED", selected)):
        print(model + "=" + ";".join(f"{key}:{value:.8f}" for key, value in metrics.items()))
    print("DIAGNOSTICS=" + "|".join(
        f"{row['檢查']}:{row['統計量']:.8f}:{row['判定']}" for row in diagnosis.to_dict("records")
    ))
    print(f"INTERVAL={interval}; LOWER_OK={(lower <= result.predictions).all()}; UPPER_OK={(result.predictions <= upper).all()}")
