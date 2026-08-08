"""
charts.py
---------
Reusable, consistently-themed Plotly chart builders. Every chart uses
the same dark transparent background, neon pink/purple/orange palette,
and hover styling so that the whole dashboard feels like one cohesive
product rather than a stack of default plots.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import (
    COLORS, GRADIENT_SEQUENTIAL, HOTEL_COLOR_MAP, STATUS_COLOR_MAP, PLOTLY_TEMPLATE
)

FONT = dict(family="Poppins, sans-serif", color=COLORS["text_primary"])


def _base_layout(fig: go.Figure, height: int = 380, title: str = "") -> go.Figure:
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=FONT,
        height=height,
        margin=dict(l=20, r=20, t=50 if title else 20, b=20),
        title=dict(text=title, font=dict(size=16, color="#fff", family="Space Grotesk, sans-serif")),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text_muted"])),
        hoverlabel=dict(bgcolor="#1a0533", bordercolor=COLORS["pink"], font=dict(color="#fff")),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.08)"),
        transition=dict(duration=400, easing="cubic-in-out"),
    )
    return fig


def hotel_share_donut(df: pd.DataFrame) -> go.Figure:
    counts = df["hotel"].value_counts().reset_index()
    counts.columns = ["hotel", "bookings"]
    fig = go.Figure(
        data=[go.Pie(
            labels=counts["hotel"], values=counts["bookings"], hole=0.62,
            marker=dict(colors=[HOTEL_COLOR_MAP.get(h, COLORS["purple"]) for h in counts["hotel"]],
                        line=dict(color="#0d0221", width=3)),
            textinfo="label+percent", textfont=dict(color="#fff", size=13),
            pull=[0.03] * len(counts),
        )]
    )
    fig.add_annotation(text=f"{len(df):,}<br><span style='font-size:11px;color:#b8a9d9'>Total Bookings</span>",
                        showarrow=False, font=dict(size=20, color="#fff"), align="center")
    return _base_layout(fig, height=360, title="Booking Share by Hotel Type")


def monthly_booking_trend(df: pd.DataFrame) -> go.Figure:
    order = ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"]
    grouped = df.groupby(["arrival_date_month", "hotel"]).size().reset_index(name="bookings")
    grouped["arrival_date_month"] = pd.Categorical(grouped["arrival_date_month"], categories=order, ordered=True)
    grouped = grouped.sort_values("arrival_date_month")

    fig = go.Figure()
    for hotel, color in HOTEL_COLOR_MAP.items():
        sub = grouped[grouped["hotel"] == hotel]
        fig.add_trace(go.Scatter(
            x=sub["arrival_date_month"], y=sub["bookings"], name=hotel,
            mode="lines", line=dict(width=3, color=color, shape="spline"),
            fill="tozeroy", fillcolor=color.replace(")", ", 0.15)").replace("rgb", "rgba") if "rgb" in color else _hex_to_rgba(color, 0.18),
        ))
    return _base_layout(fig, height=400, title="Monthly Booking Trend by Hotel Type")


def _hex_to_rgba(hex_color: str, alpha: float) -> str:
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def cancellation_rate_by_hotel(df: pd.DataFrame) -> go.Figure:
    rate = df.groupby("hotel")["is_canceled"].mean().reset_index()
    rate["is_canceled"] = rate["is_canceled"] * 100
    fig = go.Figure(go.Bar(
        x=rate["hotel"], y=rate["is_canceled"],
        marker=dict(color=[HOTEL_COLOR_MAP.get(h, COLORS["purple"]) for h in rate["hotel"]],
                    line=dict(color="rgba(255,255,255,0.2)", width=1)),
        text=[f"{v:.1f}%" for v in rate["is_canceled"]], textposition="outside",
        textfont=dict(color="#fff", size=14),
    ))
    fig.update_yaxes(title="Cancellation Rate (%)")
    return _base_layout(fig, height=360, title="Cancellation Rate by Hotel Type")


def cancellation_by_stay_length(df: pd.DataFrame) -> go.Figure:
    grouped = df.groupby(["stay_length_bucket", "hotel"], observed=True)["is_canceled"].mean().reset_index()
    grouped["is_canceled"] *= 100
    fig = go.Figure()
    for hotel, color in HOTEL_COLOR_MAP.items():
        sub = grouped[grouped["hotel"] == hotel]
        fig.add_trace(go.Scatter(
            x=sub["stay_length_bucket"], y=sub["is_canceled"], name=hotel,
            mode="lines+markers", line=dict(width=3, color=color, shape="spline"),
            marker=dict(size=9, color=color, line=dict(color="#fff", width=1)),
        ))
    fig.update_yaxes(title="Cancellation Rate (%)")
    fig.update_xaxes(title="Length of Stay")
    return _base_layout(fig, height=400, title="Cancellation Rate vs. Length of Stay")


def cancellation_by_lead_time(df: pd.DataFrame) -> go.Figure:
    grouped = df.groupby(["lead_time_bucket", "hotel"], observed=True)["is_canceled"].mean().reset_index()
    grouped["is_canceled"] *= 100
    fig = go.Figure()
    for hotel, color in HOTEL_COLOR_MAP.items():
        sub = grouped[grouped["hotel"] == hotel]
        fig.add_trace(go.Bar(
            x=sub["lead_time_bucket"], y=sub["is_canceled"], name=hotel,
            marker=dict(color=color, line=dict(color="rgba(255,255,255,0.2)", width=1)),
        ))
    fig.update_layout(barmode="group")
    fig.update_yaxes(title="Cancellation Rate (%)")
    fig.update_xaxes(title="Lead Time (days before arrival)")
    return _base_layout(fig, height=400, title="Cancellation Rate vs. Lead Time")


def market_segment_bar(df: pd.DataFrame) -> go.Figure:
    counts = df["market_segment"].value_counts().reset_index()
    counts.columns = ["segment", "bookings"]
    counts = counts.sort_values("bookings", ascending=True)
    fig = go.Figure(go.Bar(
        y=counts["segment"], x=counts["bookings"], orientation="h",
        marker=dict(
            color=counts["bookings"], colorscale=[[i / (len(GRADIENT_SEQUENTIAL) - 1), c]
                                                    for i, c in enumerate(GRADIENT_SEQUENTIAL)],
            line=dict(color="rgba(255,255,255,0.15)", width=1),
        ),
        text=counts["bookings"], textposition="outside", textfont=dict(color="#fff"),
    ))
    return _base_layout(fig, height=420, title="Bookings by Market Segment")


def adr_distribution(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for hotel, color in HOTEL_COLOR_MAP.items():
        sub = df[df["hotel"] == hotel]
        fig.add_trace(go.Violin(
            y=sub["adr"], name=hotel, box_visible=True, meanline_visible=True,
            line_color=color, fillcolor=_hex_to_rgba(color, 0.35), opacity=0.85,
        ))
    fig.update_yaxes(title="Average Daily Rate (ADR)")
    return _base_layout(fig, height=400, title="ADR Distribution by Hotel Type")


def guest_funnel(df: pd.DataFrame) -> go.Figure:
    total = len(df)
    checked_out = (df["reservation_status"] == "Check-Out").sum()
    repeat = (df["is_repeated_guest"] == 1).sum()
    special = (df["total_of_special_requests"] > 0).sum()

    fig = go.Figure(go.Funnel(
        y=["Total Bookings", "Completed Stays", "Special Requests Made", "Repeat Guests"],
        x=[total, checked_out, special, repeat],
        marker=dict(color=[COLORS["red"], COLORS["orange"], COLORS["pink"], COLORS["purple"]]),
        textinfo="value+percent initial",
        textfont=dict(color="#fff"),
        connector=dict(line=dict(color="rgba(255,255,255,0.15)", width=1)),
    ))
    return _base_layout(fig, height=380, title="Guest Journey Funnel")


def feature_importance_chart(importances: pd.Series) -> go.Figure:
    importances = importances.sort_values(ascending=True)
    fig = go.Figure(go.Bar(
        y=importances.index, x=importances.values, orientation="h",
        marker=dict(
            color=importances.values,
            colorscale=[[i / (len(GRADIENT_SEQUENTIAL) - 1), c] for i, c in enumerate(GRADIENT_SEQUENTIAL)],
            line=dict(color="rgba(255,255,255,0.15)", width=1),
        ),
    ))
    fig.update_xaxes(title="Relative Importance")
    return _base_layout(fig, height=420, title="What Drives Cancellation Risk")


def confusion_heatmap(cm: np.ndarray, labels=("Not Canceled", "Canceled")) -> go.Figure:
    fig = go.Figure(go.Heatmap(
        z=cm, x=list(labels), y=list(labels),
        colorscale=[[0, "#1a0533"], [0.5, "#8b2fe0"], [1, "#ff2ea6"]],
        text=cm, texttemplate="%{text}", textfont=dict(color="#fff", size=16),
        showscale=False,
    ))
    fig.update_yaxes(title="Actual", autorange="reversed")
    fig.update_xaxes(title="Predicted")
    return _base_layout(fig, height=340, title="Model Confusion Matrix")

def roc_curve_chart(fpr, tpr, auc_score: float) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", name=f"AUC = {auc_score:.3f}",
                              line=dict(color=COLORS["pink"], width=3),
                              fill="tozeroy", fillcolor=_hex_to_rgba(COLORS["pink"], 0.15)))
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Random baseline",
                              line=dict(color="rgba(255,255,255,0.3)", width=1, dash="dash")))
    fig.update_xaxes(title="False Positive Rate")
    fig.update_yaxes(title="True Positive Rate")
    return _base_layout(fig, height=380, title="ROC Curve")


def deposit_type_treemap(df: pd.DataFrame) -> go.Figure:
    grouped = df.groupby(["deposit_type", "booking_status"]).size().reset_index(name="count")
    fig = px.treemap(
        grouped, path=["deposit_type", "booking_status"], values="count",
        color="booking_status", color_discrete_map=STATUS_COLOR_MAP,
    )
    fig.update_traces(marker=dict(line=dict(color="#0d0221", width=2)), textfont=dict(color="#fff"))
    return _base_layout(fig, height=420, title="Deposit Type vs. Booking Outcome")
