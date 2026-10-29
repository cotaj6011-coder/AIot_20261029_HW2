import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

COLORS = {"navy": "#162B4D", "blue": "#3974E8", "teal": "#16A6A1", "amber": "#F2A93B", "red": "#E25B67"}


def apply_theme(fig, height=430):
    fig.update_layout(
        template="plotly_white", height=height,
        font=dict(family="Inter, Noto Sans TC, sans-serif", color=COLORS["navy"]),
        title=dict(font=dict(size=20, color=COLORS["navy"]), x=0.02),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,250,253,.9)",
        margin=dict(l=45, r=25, t=65, b=45), legend=dict(orientation="h", y=1.08),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E7ECF4", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#E7ECF4", zeroline=False)
    return fig


def actual_vs_predicted(y, predictions):
    frame = pd.DataFrame({"實際值": y, "預測值": predictions})
    fig = px.scatter(frame, x="實際值", y="預測值", title="測試集：實際值 vs 預測值", color_discrete_sequence=[COLORS["blue"]])
    low, high = frame.min().min(), frame.max().max()
    fig.add_trace(go.Scatter(x=[low, high], y=[low, high], mode="lines", name="理想 y=x"))
    return apply_theme(fig)


def interval_plot(y, prediction, lower, upper, limit=100):
    order = np.argsort(prediction)[:limit]
    x = np.arange(len(order))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=upper[order], line=dict(width=0), showlegend=False))
    fig.add_trace(go.Scatter(x=x, y=lower[order], fill="tonexty", name="95% 預測區間", line=dict(width=0)))
    fig.add_trace(go.Scatter(x=x, y=prediction[order], mode="lines+markers", name="預測值"))
    fig.add_trace(go.Scatter(x=x, y=np.asarray(y)[order], mode="markers", name="實際值"))
    fig.update_layout(title="排序測試樣本與 95% OLS 預測區間", xaxis_title="排序後樣本")
    return apply_theme(fig)


def residual_plot(predictions, residuals):
    fig = px.scatter(x=predictions, y=residuals, labels={"x":"預測值", "y":"殘差"}, title="殘差 vs 預測值")
    fig.add_hline(y=0)
    return apply_theme(fig)


def qq_plot(residuals):
    theoretical, ordered = stats.probplot(residuals, dist="norm", fit=False)
    fig = px.scatter(x=theoretical, y=ordered, labels={"x":"理論常態分位數", "y":"樣本殘差"}, title="殘差 QQ Plot")
    return apply_theme(fig)
