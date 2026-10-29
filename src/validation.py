from __future__ import annotations

import numpy as np
import pandas as pd

HIGH_MISSING_THRESHOLD = 0.50


def validate_analysis_data(frame: pd.DataFrame, target: str, excluded=()) -> tuple[list[str], list[str]]:
    if target not in frame.columns:
        raise ValueError("找不到指定 target。")
    if not pd.api.types.is_numeric_dtype(frame[target]):
        raise ValueError("target 必須是連續數值欄位。")
    usable = frame.dropna(subset=[target])
    if len(usable) < 20:
        raise ValueError("有效資料至少需要 20 筆。")
    features = [c for c in frame.columns if c != target and c not in excluded]
    if not features:
        raise ValueError("至少需要一個特徵欄位。")
    constants = [c for c in features if frame[c].nunique(dropna=True) <= 1]
    features = [c for c in features if c not in constants]
    if not features:
        raise ValueError("排除常數欄後沒有可用特徵。")
    if not np.isfinite(usable[target].astype(float)).all():
        raise ValueError("target 包含無限值。")
    return features, constants


def data_profile(frame: pd.DataFrame, target: str, features: list[str]) -> dict:
    return {
        "rows": len(frame),
        "columns": frame.shape[1],
        "raw_feature_count": len(features),
        "missing_cells": int(frame[features + [target]].isna().sum().sum()),
        "duplicate_rows": int(frame.duplicated().sum()),
        "target_missing": int(frame[target].isna().sum()),
    }


def column_quality(frame: pd.DataFrame, target: str, features: list[str]) -> pd.DataFrame:
    """Return reproducible column-level evidence used by the UI and report."""
    rows = []
    for column in features + [target]:
        missing = int(frame[column].isna().sum())
        unique = int(frame[column].nunique(dropna=True))
        rows.append({
            "欄位": column,
            "角色": "Target" if column == target else "Feature",
            "型別": str(frame[column].dtype),
            "缺失數": missing,
            "缺失率": missing / len(frame),
            "唯一值": unique,
            "常數欄": unique <= 1,
        })
    return pd.DataFrame(rows)


def duplicate_feature_groups(frame: pd.DataFrame, features: list[str]) -> list[list[str]]:
    groups: list[list[str]] = []
    used: set[str] = set()
    for index, left in enumerate(features):
        if left in used:
            continue
        matches = [right for right in features[index + 1:] if frame[left].equals(frame[right])]
        if matches:
            group = [left, *matches]
            groups.append(group)
            used.update(group)
    return groups


def suspected_identifier_columns(frame: pd.DataFrame, features: list[str]) -> list[str]:
    suspects = []
    for column in features:
        name = column.lower().replace("_", "").replace(" ", "")
        unique_ratio = frame[column].nunique(dropna=True) / max(len(frame), 1)
        if name in {"id", "index", "rowid", "userid", "recordid"} or unique_ratio > 0.98:
            suspects.append(column)
    return suspects


def quality_summary(frame: pd.DataFrame, target: str, features: list[str]) -> dict:
    quality = column_quality(frame, target, features)
    return {
        "columns": quality,
        "high_missing": quality.loc[
            (quality["角色"] == "Feature") & (quality["缺失率"] > HIGH_MISSING_THRESHOLD), "欄位"
        ].tolist(),
        "duplicate_feature_groups": duplicate_feature_groups(frame, features),
        "suspected_identifiers": suspected_identifier_columns(frame, features),
        "cleaning_strategy": pd.DataFrame([
            {"資料問題": "Target 缺失", "處理策略": "建模前移除該列", "Fit 範圍": "切分前僅移除無標籤列"},
            {"資料問題": "數值缺失", "處理策略": "中位數補值", "Fit 範圍": "僅訓練集"},
            {"資料問題": "類別缺失", "處理策略": "眾數補值", "Fit 範圍": "僅訓練集"},
            {"資料問題": "類別欄", "處理策略": "One-Hot 並刪除第一個基準類別；未知類別忽略", "Fit 範圍": "僅訓練集"},
            {"資料問題": "常數欄", "處理策略": "自動排除", "Fit 範圍": "分析前規則檢查"},
            {"資料問題": "疑似 ID／洩漏", "處理策略": "提示使用者確認並排除，不自動猜測", "Fit 範圍": "人工確認"},
        ]),
    }

