"""
ai_insights.py
--------------
The AI-powered page. Trains (and caches) a real GradientBoosting
classifier to predict cancellation risk, shows model performance and
feature importances, and offers an interactive "what-if" predictor
where a manager can enter a hypothetical booking and get a live risk
score.
"""

import streamlit as st
import pandas as pd

from components import ui_elements as ui
from components import charts
from data.model import train_cancellation_model, predict_single


@st.cache_resource(show_spinner=False)
def _get_model_bundle(df: pd.DataFrame):
    return train_cancellation_model(df)


def render(df):
    ui.page_header(
        "AI Insights",
        "A trained machine learning model that predicts booking cancellation risk in real time.",
        badge="AI-POWERED",
    )

    with st.spinner("Training cancellation risk model on the cleaned dataset..."):
        bundle = _get_model_bundle(df)

    metrics = bundle["metrics"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        ui.kpi_card("Accuracy", f"{metrics['accuracy']*100:.1f}%", "On held-out test data", icon="target")
    with c2:
        ui.kpi_card("Precision", f"{metrics['precision']*100:.1f}%", "Of predicted cancellations", icon="search")
    with c3:
        ui.kpi_card("Recall", f"{metrics['recall']*100:.1f}%", "Of true cancellations caught", icon="radio")
    with c4:
        ui.kpi_card("ROC-AUC", f"{metrics['roc_auc']:.3f}", "Overall model quality", icon="bolt")

    st.markdown("<div style='height:1.4rem'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.3, 1])
    with col1:
        ui.glass_card_open()
        ui.section_title("What Drives Cancellation Risk", icon="bar-chart")
        st.plotly_chart(charts.feature_importance_chart(bundle["importances"].head(10)),
                         use_container_width=True, config={"displayModeBar": False})
        ui.glass_card_close()
    with col2:
        ui.glass_card_open()
        ui.section_title("Model Performance", icon="shield")
        tab_a, tab_b = st.tabs(["Confusion Matrix", "ROC Curve"])
        with tab_a:
            st.plotly_chart(charts.confusion_heatmap(metrics["confusion_matrix"]),
                             use_container_width=True, config={"displayModeBar": False})
        with tab_b:
            st.plotly_chart(charts.roc_curve_chart(metrics["fpr"], metrics["tpr"], metrics["roc_auc"]),
                             use_container_width=True, config={"displayModeBar": False})
        ui.glass_card_close()

    top_feature = bundle["importances"].index[0]
    ui.glass_card_open("margin-top:1rem;")
    st.markdown(f"""
    **Smart Insight:** The single strongest predictor of cancellation is **`{top_feature}`**.
    This is trained on {len(df):,} cleaned booking records, using a Gradient Boosting classifier
    with {metrics['roc_auc']:.2f} ROC-AUC — meaning it reliably separates bookings that will cancel
    from those that won't, far better than random guessing (0.50).
    """)
    ui.glass_card_close()

    st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)

    ui.section_title("Live Cancellation Risk Predictor", icon="cpu")
    ui.glass_card_open()
    st.markdown("<p style='color:#b8a9d9; margin-top:-0.4rem;'>Enter a hypothetical booking to get an instant AI-generated cancellation risk score.</p>",
                unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns(4)
    with f1:
        hotel = st.selectbox("Hotel Type", sorted(df["hotel"].unique()))
        lead_time = st.slider("Lead Time (days)", 0, 500, 60)
        month = st.selectbox("Arrival Month", sorted(df["arrival_date_month"].unique(),
                                                        key=lambda m: list(df["arrival_date_month"].unique()).index(m)))
    with f2:
        weekend_nights = st.slider("Weekend Nights", 0, 10, 1)
        weekday_nights = st.slider("Weekday Nights", 0, 20, 2)
        adults = st.slider("Adults", 1, 6, 2)
    with f3:
        deposit_type = st.selectbox("Deposit Type", sorted(df["deposit_type"].unique()))
        customer_type = st.selectbox("Customer Type", sorted(df["customer_type"].unique()))
        market_segment = st.selectbox("Market Segment", sorted(df["market_segment"].unique()))
    with f4:
        adr = st.slider("Average Daily Rate ($)", 0, 500, 110)
        special_requests = st.slider("Special Requests", 0, 5, 0)
        prior_cancellations = st.slider("Previous Cancellations", 0, 10, 0)

    if st.button("Predict Cancellation Risk", use_container_width=True):
        input_row = {
            "hotel": hotel, "lead_time": lead_time, "arrival_date_month": month,
            "stays_in_weekend_nights": weekend_nights, "stays_in_weekdays_nights": weekday_nights,
            "adults": adults, "children": 0, "babies": 0, "meal": "Breakfast",
            "market_segment": market_segment, "distribution_channel": "TA/TO",
            "is_repeated_guest": 0, "previous_cancellations": prior_cancellations,
            "previous_bookings_not_canceled": 0, "booking_changes": 0,
            "deposit_type": deposit_type, "days_in_waiting_list": 0,
            "customer_type": customer_type, "adr": adr,
            "required_car_parking_spaces": 0, "total_of_special_requests": special_requests,
        }
        risk = predict_single(bundle, input_row) * 100

        tone = "danger" if risk >= 60 else ("warning" if risk >= 30 else "success")
        label = "HIGH RISK" if risk >= 60 else ("MODERATE RISK" if risk >= 30 else "LOW RISK")

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        rc1, rc2 = st.columns([1, 2])
        with rc1:
            ui.kpi_card("Cancellation Risk", f"{risk:.1f}%", "AI-predicted probability", icon="dice",
                         glow_color="#ff3b5c" if risk >= 60 else "#ffd166" if risk >= 30 else "#3ddc97")
        with rc2:
            ui.status_pill(f"● {label}", tone=tone)
            st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
            if risk >= 60:
                st.markdown("Consider requiring a deposit, sending a confirmation reminder, or offering a flexible reschedule to retain this booking.")
            elif risk >= 30:
                st.markdown("Worth a soft-touch reminder closer to arrival. No immediate action required.")
            else:
                st.markdown("Low risk booking — no action needed.")

    ui.glass_card_close()
