from __future__ import annotations

import hashlib
import pandas as pd
import plotly.express as px
import streamlit as st

from src.datasets import DATASETS, load_builtin, load_csv_url
from src.evaluation import diagnostics, regression_metrics
from src.intervals import ols_prediction_intervals
from src.modeling import MAX_ANALYSIS_ROWS, RANDOM_STATE, run_analysis
from src.plots import COLORS, actual_vs_predicted, apply_theme, interval_plot, qq_plot, residual_plot
from src.validation import data_profile, quality_summary, validate_analysis_data

st.set_page_config(page_title="Regression Studio", page_icon="◈", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+TC:wght@400;500;600;700&display=swap');
:root{--navy:#162B4D;--blue:#3974E8;--teal:#16A6A1;--line:#E4EAF3}
.stApp{background:linear-gradient(180deg,#F7F9FD 0%,#EEF3F9 100%);color:var(--navy)}
html,body,[class*="css"]{font-family:Inter,"Noto Sans TC",sans-serif}
[data-testid="stSidebar"]{background:#102440;border-right:1px solid rgba(255,255,255,.08)}
[data-testid="stSidebar"] *{color:#EFF5FF}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p{color:#F8FAFC!important;font-weight:650;letter-spacing:.01em}
[data-testid="stSidebar"] input{color:#1E293B!important;caret-color:#2563EB!important}
[data-testid="stSidebar"] input::placeholder{color:#64748B!important;opacity:1!important}
[data-testid="stSidebar"] [data-testid="stTextInputRootElement"],
[data-testid="stSidebar"] [role="group"]:has(input[role="combobox"]),
[data-testid="stSidebar"] [data-baseweb="input"]>div,
[data-testid="stSidebar"] [data-baseweb="select"]>div{background:#FFFFFF!important;border:1px solid #CBD5E1!important;border-radius:10px!important;transition:border-color .16s ease,box-shadow .16s ease,background .16s ease}
[data-testid="stSidebar"] [data-testid="stTextInputRootElement"]:hover,
[data-testid="stSidebar"] [role="group"]:has(input[role="combobox"]):hover,
[data-testid="stSidebar"] [data-baseweb="select"]>div:hover,
[data-testid="stSidebar"] [data-baseweb="input"]>div:hover{border-color:#60A5FA!important}
[data-testid="stSidebar"] [data-testid="stTextInputRootElement"]:focus-within,
[data-testid="stSidebar"] [role="group"]:has(input[role="combobox"]):focus-within,
[data-testid="stSidebar"] [data-baseweb="select"]>div:focus-within,
[data-testid="stSidebar"] [data-baseweb="input"]>div:focus-within{border-color:#3B82F6!important;box-shadow:0 0 0 3px rgba(59,130,246,.26)!important}
[data-testid="stSidebar"] [role="group"]:has(input[role="combobox"]) button,
[data-testid="stSidebar"] [role="group"]:has(input[role="combobox"]) svg,
[data-testid="stSidebar"] [data-baseweb="select"] input,
[data-testid="stSidebar"] [data-baseweb="select"] [role="combobox"],
[data-testid="stSidebar"] [data-baseweb="select"] svg{color:#1E293B!important;fill:#475569!important}
[data-testid="stSidebar"] [data-baseweb="tag"]{background:#E0F2FE!important;border:1px solid #BAE6FD!important}
[data-testid="stSidebar"] [data-baseweb="tag"] span,
[data-testid="stSidebar"] [data-baseweb="tag"] svg{color:#0C4A6E!important;fill:#0C4A6E!important}
[data-baseweb="popover"] [role="option"]{color:#1E293B!important;background:#FFFFFF!important}
[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] [aria-selected="true"]{color:#0F3B67!important;background:#E0F2FE!important}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"]{background:#FFFFFF!important;border:1px dashed #94A3B8!important;border-radius:10px!important;padding:.75rem!important}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"]:hover{border-color:#3B82F6!important;background:#F8FAFC!important}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] *,
[data-testid="stSidebar"] [data-testid="stFileUploaderFile"] *{color:#334155!important}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] small{color:#64748B!important}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button{color:#1E3A5F!important;background:#EFF6FF!important;border:1px solid #BFDBFE!important}
[data-testid="stSidebar"] input:disabled,
[data-testid="stSidebar"] [aria-disabled="true"]{color:#64748B!important;-webkit-text-fill-color:#64748B!important;opacity:.82!important}
[data-testid="stSidebar"] .stButton{margin:.12rem 0 .25rem}
[data-testid="stSidebar"] .stButton button{width:100%;min-height:2.55rem;background:linear-gradient(135deg,#3974E8,#16A6A1);color:white!important;border:0;border-radius:10px;font-weight:700;transition:transform .16s ease,box-shadow .16s ease,filter .16s ease}
[data-testid="stSidebar"] .stButton button:hover{filter:brightness(1.07);box-shadow:0 8px 18px rgba(22,166,161,.22);transform:translateY(-1px)}
[data-testid="stSidebar"] .stButton button:focus-visible{outline:3px solid rgba(147,197,253,.75);outline-offset:2px}
.hero{padding:2.2rem 2.4rem;border-radius:24px;color:white;background:radial-gradient(circle at 90% 10%,rgba(79,205,199,.35),transparent 32%),linear-gradient(120deg,#132B4F,#285DAE);box-shadow:0 18px 45px rgba(23,48,88,.18);margin-bottom:1.25rem}
.hero .eyebrow{letter-spacing:.14em;font-weight:700;font-size:.76rem;opacity:.72}.hero h1{margin:.35rem 0 .45rem;font-size:2.35rem;line-height:1.14}.hero p{max-width:780px;color:#DCE9FF;margin:0}
.badge{display:inline-block;padding:.28rem .65rem;border-radius:999px;background:rgba(255,255,255,.12);margin:.85rem .35rem 0 0;font-size:.78rem}
.section-kicker{color:#3974E8;font-size:.74rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;margin-bottom:.1rem}
.insight{padding:1rem 1.1rem;border:1px solid var(--line);border-radius:16px;background:white;box-shadow:0 8px 22px rgba(30,52,87,.06);min-height:100px}.insight strong{display:block;font-size:1.35rem;margin-top:.15rem;color:var(--navy)}
[data-testid="stMetric"]{background:white;border:1px solid var(--line);padding:1rem 1.15rem;border-radius:16px;box-shadow:0 8px 22px rgba(30,52,87,.06)}[data-testid="stMetricValue"]{color:var(--navy);font-weight:750}
[data-testid="stTabs"] [role="tablist"],.stTabs [data-baseweb="tab-list"]{display:flex;flex-wrap:nowrap;gap:10px!important;background:#E8EEF7;padding:6px!important;border-radius:14px;overflow-x:auto!important;scrollbar-width:thin;scrollbar-color:#9DB0CA transparent}
[data-testid="stTabs"] [role="tablist"]::-webkit-scrollbar,.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar{height:6px}[data-testid="stTabs"] [role="tablist"]::-webkit-scrollbar-thumb,.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb{background:#9DB0CA;border-radius:99px}
[data-testid="stTab"],.stTabs [data-baseweb="tab"]{flex:0 0 auto!important;min-width:max-content;min-height:44px;border-radius:10px;padding:10px 14px!important;color:#334155!important;font-weight:650;line-height:1.2;transition:color .16s ease,background .16s ease,box-shadow .16s ease,transform .16s ease}
[data-testid="stTab"] p,.stTabs [data-baseweb="tab"] p{color:inherit!important;white-space:nowrap;margin:0}
[data-testid="stTab"]:hover,[data-testid="stTab"][data-hovered="true"],.stTabs [data-baseweb="tab"]:hover{color:#1E3A8A!important;background:#EFF6FF!important;transform:translateY(-1px)}
[data-testid="stTab"]:focus-visible,[data-testid="stTab"][data-focused="true"],.stTabs [data-baseweb="tab"]:focus-visible{outline:3px solid rgba(59,130,246,.3)!important;outline-offset:1px}
[data-testid="stTab"][aria-selected="true"],.stTabs [aria-selected="true"]{color:#1E3A8A!important;background:#DBEAFE!important;box-shadow:0 3px 10px rgba(30,64,175,.12),inset 0 -3px 0 #2563EB}
[data-testid="stTab"] .react-aria-SelectionIndicator{display:none!important;background:#2563EB!important;border-color:#2563EB!important;color:#2563EB!important}
[data-testid="stDownloadButton"] button{min-height:2.65rem;background:#1E40AF!important;border:1px solid #1E40AF!important;border-radius:10px!important;color:#FFFFFF!important;font-weight:700!important;transition:background .16s ease,border-color .16s ease,box-shadow .16s ease,transform .16s ease}
[data-testid="stDownloadButton"] button *{color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important}
[data-testid="stDownloadButton"] button:hover{background:#1D4ED8!important;border-color:#1D4ED8!important;box-shadow:0 8px 18px rgba(30,64,175,.2)!important;transform:translateY(-1px)}
[data-testid="stDownloadButton"] button:focus-visible{background:#1E40AF!important;border-color:#93C5FD!important;outline:3px solid rgba(37,99,235,.32)!important;outline-offset:2px}
[data-testid="stDownloadButton"] button:active{background:#1E3A8A!important;border-color:#1E3A8A!important;transform:none}
[data-testid="stDownloadButton"] button:disabled,[data-testid="stDownloadButton"] button[aria-disabled="true"]{background:#94A3B8!important;border-color:#94A3B8!important;color:#F8FAFC!important;box-shadow:none!important;opacity:1!important;transform:none}
[data-testid="stAlertContainer"]:has([data-testid="stAlertContentSuccess"]){background:#DCFCE7!important;border:1px solid #BBF7D0!important;border-radius:10px!important;color:#166534!important}
[data-testid="stAlertContainer"]:has([data-testid="stAlertContentSuccess"]) *{color:#166534!important;fill:#166534!important;-webkit-text-fill-color:#166534!important}
[data-testid="stDataFrame"],[data-testid="stPlotlyChart"]{border:1px solid var(--line);border-radius:16px;overflow:hidden;background:white}
@media(max-width:700px){.hero{padding:1.4rem}.hero h1{font-size:1.75rem}[data-testid="stTabs"] [role="tablist"],.stTabs [data-baseweb="tab-list"]{gap:8px!important;padding:5px!important}[data-testid="stTab"],.stTabs [data-baseweb="tab"]{padding:9px 12px!important;min-height:42px}}
</style>
""", unsafe_allow_html=True)


def reset_source_state() -> None:
    for key in ("custom_frame", "custom_source", "analysis_ready", "last_signature"):
        st.session_state.pop(key, None)


@st.cache_data(show_spinner=False)
def cached_builtin(dataset_id: str):
    return load_builtin(dataset_id)


@st.cache_data(ttl=3600, show_spinner=False)
def cached_url(url: str):
    return load_csv_url(url)


@st.cache_resource(show_spinner=False)
def cached_analysis(frame: pd.DataFrame, target: str, excluded: tuple[str, ...]):
    return run_analysis(frame, target, excluded)


labels = {spec.label: key for key, spec in DATASETS.items()}
with st.sidebar:
    st.markdown("## ◈ Regression Studio")
    st.caption("可重現的多元線性回歸工作台")
    mode = st.selectbox("資料來源", [*labels, "Custom CSV URL"], key="dataset_mode", on_change=reset_source_state)
    st.markdown("---")

frame = target = description = source = license_note = None
excluded_default: list[str] = []
load_error = None
try:
    if mode in labels:
        frame, spec = cached_builtin(labels[mode])
        target, description, source, license_note = spec.target, spec.description, spec.source_url, spec.license_note
        excluded_default = list(spec.excluded)
    else:
        with st.sidebar:
            url = st.text_input("公開 HTTPS CSV", "https://raw.githubusercontent.com/Avik-Jain/100-Days-Of-ML-Code/master/datasets/50_Startups.csv")
            uploaded = st.file_uploader("或上傳 CSV", type="csv", help="部署環境無法連外時使用")
            load_clicked = st.button("載入資料", type="primary")
        if uploaded is not None:
            frame = pd.read_csv(uploaded)
            source, description, license_note = "使用者上傳", "自訂回歸資料", "授權由上傳者確認。"
        elif load_clicked:
            with st.spinner("驗證公開位址與 CSV 內容…"):
                st.session_state["custom_frame"] = cached_url(url)
                st.session_state["custom_source"] = url
        if frame is None and "custom_frame" in st.session_state:
            frame = st.session_state["custom_frame"]
            source = st.session_state.get("custom_source", url)
        if frame is not None:
            source = source or url
            description = description or "自訂公開資料的多元線性回歸分析。"
            license_note = license_note or "資料授權由使用者確認。"
            numeric_targets = [c for c in frame.columns if pd.api.types.is_numeric_dtype(frame[c])]
            with st.sidebar:
                target = st.selectbox("連續數值 Target", numeric_targets) if numeric_targets else None
except Exception as exc:
    load_error = str(exc)

st.markdown("""
<div class="hero"><div class="eyebrow">MULTIPLE LINEAR REGRESSION · CRISP-DM</div>
<h1>從資料品質到模型診斷，完整呈現每一步</h1>
<p>以訓練集內交叉驗證完成特徵選擇，保留獨立測試集，並用 95% 預測區間與回歸假設檢查解讀結果。</p>
<span class="badge">LinearRegression</span><span class="badge">5-Fold CV</span><span class="badge">No Leakage</span><span class="badge">95% Prediction Interval</span></div>
""", unsafe_allow_html=True)
if load_error:
    st.error(f"資料載入失敗：{load_error}")
if frame is None or target is None:
    st.info("請從左側載入公開 HTTPS CSV 或上傳 CSV；資料至少需要 20 筆、一個特徵與一個連續數值 target。")
    st.stop()

target_candidates = [c for c in frame.columns if c != target]
with st.sidebar:
    excluded = st.multiselect("排除 ID／洩漏／不使用欄位", target_candidates, default=excluded_default)
    analyze_clicked = st.button("執行完整分析", type="primary")
    st.caption(f"固定 seed {RANDOM_STATE} · 最多分析 {MAX_ANALYSIS_ROWS:,} 筆")

try:
    features, constants = validate_analysis_data(frame, target, excluded)
    profile = data_profile(frame, target, features)
    quality = quality_summary(frame, target, features)
except ValueError as exc:
    st.error(str(exc))
    st.stop()

signature = hashlib.sha256(f"{mode}|{target}|{'|'.join(sorted(excluded))}|{frame.shape}".encode()).hexdigest()
if analyze_clicked:
    st.session_state["analysis_ready"] = True
    st.session_state["last_signature"] = signature
analysis_ready = st.session_state.get("analysis_ready") and st.session_state.get("last_signature") == signature

top = st.columns([1.7, 1, 1])
with top[0]:
    st.markdown('<div class="section-kicker">CURRENT STUDY</div>', unsafe_allow_html=True)
    st.subheader(mode)
    st.write(description)
with top[1]:
    st.markdown(f'<div class="insight">Target<strong>{target}</strong><span>{profile["raw_feature_count"]} 個原始特徵</span></div>', unsafe_allow_html=True)
with top[2]:
    compliance = "符合正式門檻" if 14 <= len(features) <= 39 else "可分析／不符 14–39"
    st.markdown(f'<div class="insight">Feature Gate<strong>{compliance}</strong><span>正式 Kaggle 題另行標示</span></div>', unsafe_allow_html=True)
st.caption(f"資料來源：{source}　｜　{license_note}")

tabs = st.tabs(["01 商業理解", "02 資料理解", "03 資料準備", "04 建模", "05 評估診斷", "06 部署匯出"])
with tabs[0]:
    st.subheader("Business Understanding")
    st.write(description)
    st.info("模型用於教學與關聯性分析，不應解讀為因果證據。正式 Human–AI 題為合成教育資料，不代表真實個體。")

with tabs[1]:
    st.subheader("Data Understanding")
    cards = st.columns(5)
    values = [profile["rows"], profile["columns"], profile["raw_feature_count"], profile["missing_cells"], profile["duplicate_rows"]]
    for card, label, value in zip(cards, ["資料列", "總欄位", "原始特徵", "缺失格", "重複列"], values):
        card.metric(label, f"{value:,}")
    preview, summary = st.columns([1.15, .85])
    with preview:
        st.markdown("#### 資料預覽")
        st.dataframe(frame.head(20), hide_index=True, width="stretch")
    with summary:
        st.markdown("#### 敘述統計")
        st.dataframe(frame[features + [target]].describe(include="all").transpose(), width="stretch")
    st.markdown("#### 欄位品質與型別")
    st.dataframe(quality["columns"], hide_index=True, width="stretch",
                 column_config={"缺失率": st.column_config.ProgressColumn(format="%.1%%", min_value=0, max_value=1)})
    alerts = []
    if quality["high_missing"]:
        alerts.append(f"高缺失欄：{', '.join(quality['high_missing'])}")
    if quality["suspected_identifiers"]:
        alerts.append(f"疑似 ID／高唯一率：{', '.join(quality['suspected_identifiers'])}")
    if quality["duplicate_feature_groups"]:
        alerts.append("重複特徵組：" + "; ".join(" = ".join(group) for group in quality["duplicate_feature_groups"]))
    st.warning("\n\n".join(alerts)) if alerts else st.success("未發現高缺失、完全重複特徵或疑似 ID 欄位。")
    chart_left, chart_right = st.columns(2)
    with chart_left:
        st.plotly_chart(apply_theme(px.histogram(frame, x=target, title=f"Target 分布 · {target}", color_discrete_sequence=[COLORS["teal"]])), width="stretch")
    numeric = frame[features + [target]].select_dtypes("number")
    with chart_right:
        if numeric.shape[1] <= 30:
            st.plotly_chart(apply_theme(px.imshow(numeric.corr(), color_continuous_scale="RdBu_r", zmin=-1, zmax=1, title="數值欄位相關係數")), width="stretch")

with tabs[2]:
    st.subheader("Data Preparation")
    st.dataframe(quality["cleaning_strategy"], hide_index=True, width="stretch")
    if constants:
        st.warning(f"自動排除常數欄：{', '.join(constants)}")
    st.success("先以 random_state=42 切分 80/20；Imputer、Scaler、One-Hot（第一類為基準）與 Selector 全部包在 Pipeline，僅對訓練資料 fit。")
    st.caption(f"資源政策：來源超過 {MAX_ANALYSIS_ROWS:,} 筆時，以固定 seed 抽樣後分析並揭露；品質統計仍以載入資料為準。")

result = prediction = lower = upper = interval_info = diagnosis = residuals = metrics = None
if analysis_ready:
    try:
        with st.spinner("正在執行訓練集 5-fold CV、模型評估與診斷…"):
            result = cached_analysis(frame, target, tuple(excluded))
            prediction, lower, upper, interval_info = ols_prediction_intervals(result.selected, result.X_train, result.y_train, result.X_test)
            train_design = result.selected.named_steps["selector"].transform(result.selected.named_steps["preprocessor"].transform(result.X_train))
            diagnosis, residuals = diagnostics(result.y_test, result.predictions, train_design)
            baseline_metrics = regression_metrics(result.y_test, result.baseline_predictions, result.transformed_feature_count)
            selected_metrics = regression_metrics(result.y_test, result.predictions, len(result.selected_names))
            metrics = pd.DataFrame([baseline_metrics, selected_metrics], index=["Baseline", "Selected"])
    except Exception as exc:
        st.error(f"分析失敗：{exc}")

with tabs[3]:
    st.subheader("Modeling & Feature Selection")
    if result is None:
        st.info("按左側「執行完整分析」後顯示模型結果。")
    else:
        if result.sampled:
            st.warning(f"資源限制抽樣：原有效資料 {result.source_rows:,} 筆，本次固定 seed 分析 {result.analysis_rows:,} 筆。")
        setting_cols = st.columns(5)
        settings = [("Estimator", "LinearRegression"), ("Split", "80 / 20"), ("CV", "5-Fold"), ("Encoded", result.transformed_feature_count), ("Selected", len(result.selected_names))]
        for column, (label, value) in zip(setting_cols, settings):
            column.metric(label, value)
        st.markdown("#### 訓練集 CV 選擇紀錄")
        st.dataframe(result.comparison.style.format({"CV RMSE":"{:.4f}", "CV RMSE SD":"{:.4f}"}), hide_index=True, width="stretch")
        left, right = st.columns([.9, 1.1])
        with left:
            st.markdown("#### 模型參數")
            st.json({"estimator":"sklearn.linear_model.LinearRegression", "fit_intercept":True, "intercept":result.intercept,
                     "random_state":RANDOM_STATE, "test_size":.2, "cv_folds":5})
        with right:
            st.markdown("#### 編碼後特徵 → 原始欄位")
            st.dataframe(result.raw_feature_map, hide_index=True, width="stretch")
        st.markdown("#### Selected 模型係數")
        st.dataframe(result.coefficients, hide_index=True, width="stretch")

with tabs[4]:
    st.subheader("Evaluation & Diagnostics")
    if result is None:
        st.info("執行分析後顯示 Baseline／Selected 比較、預測區間與診斷。")
    else:
        st.markdown("#### Baseline vs Selected")
        st.dataframe(metrics.style.format("{:.5f}"), width="stretch")
        metric_plot = metrics.reset_index(names="Model").melt(id_vars="Model", value_vars=["MAE", "RMSE", "R²"], var_name="Metric", value_name="Value")
        st.plotly_chart(apply_theme(px.bar(metric_plot, x="Metric", y="Value", color="Model", barmode="group", title="模型測試集指標比較", color_discrete_map={"Baseline":"#9BAAC0", "Selected":COLORS["blue"]})), width="stretch")
        visual_left, visual_right = st.columns(2)
        visual_left.plotly_chart(actual_vs_predicted(result.y_test, result.predictions), width="stretch")
        visual_right.plotly_chart(interval_plot(result.y_test, prediction, lower, upper), width="stretch")
        st.caption(f"{interval_info['method']}；只用訓練殘差，dof={interval_info['dof']}、rank={interval_info['rank']}。")
        residual_left, residual_right = st.columns(2)
        residual_left.plotly_chart(residual_plot(result.predictions, residuals), width="stretch")
        residual_right.plotly_chart(qq_plot(residuals), width="stretch")
        st.plotly_chart(apply_theme(px.histogram(x=residuals, title="殘差分布", labels={"x":"殘差"}, color_discrete_sequence=[COLORS["teal"]]), height=360), width="stretch")
        st.markdown("#### 回歸假設診斷")
        diagnostic_cols = st.columns(len(diagnosis))
        for column, row in zip(diagnostic_cols, diagnosis.to_dict("records")):
            icon = "✓" if row["判定"] == "通過" else "!"
            column.metric(f"{icon} {row['檢查']}", row["判定"], f"{row['統計量']:.3g}" if pd.notna(row["統計量"]) else "N/A")
        st.dataframe(diagnosis, hide_index=True, width="stretch")
        st.caption("診斷門檻用於警示，不代表統計檢定能證明假設；共線或秩不足時須結合係數穩定性解讀。")

with tabs[5]:
    st.subheader("Deployment & Export")
    if result is None:
        st.info("執行分析後可下載 metrics、selected features 與 predictions。")
    else:
        predictions = pd.DataFrame({"actual":result.y_test, "predicted":result.predictions, "pi95_lower":lower, "pi95_upper":upper, "residual":residuals})
        downloads = st.columns(3)
        downloads[0].download_button("下載 metrics.csv", metrics.to_csv().encode("utf-8-sig"), "metrics.csv", "text/csv", width="stretch")
        downloads[1].download_button("下載 selected_features.csv", result.raw_feature_map.to_csv(index=False).encode("utf-8-sig"), "selected_features.csv", "text/csv", width="stretch")
        downloads[2].download_button("下載 predictions.csv", predictions.to_csv(index=False).encode("utf-8-sig"), "predictions.csv", "text/csv", width="stretch")
        st.success("分析與匯出已完成。公開 Web 已部署；NotebookLM 研究與對話 PDF 仍須由使用者完成。")
