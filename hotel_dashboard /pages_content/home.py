"""
home.py
-------
Landing page: hero KPI row, quick-glance charts (mirrors the mockup's
top KPI cards + main visual grid), and a welcome/status banner.
"""

import streamlit as st
import plotly.graph_objects as go

from components import ui_elements as ui
from components import charts
from config import COLORS


def render(df):
    ui.page_header(
        "Welcome back, Manager ✦",
        "Here's how Hotel Analytics is performing right now.",
        badge="LIVE",
    )

    total_bookings = len(df)
    cancel_rate = df["is_canceled"].mean() * 100
    avg_adr = df["adr"].mean()
    total_revenue = (df["adr"] * df["total_nights"]).sum()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        ui.kpi_card("Total Bookings", f"{total_bookings:,}", "Across 2017 – 2019", icon="calendar",
                     delta="Cleaned dataset", delta_positive=True, glow_color=COLORS["pink"])
    with c2:
        ui.kpi_card("Cancellation Rate", f"{cancel_rate:.1f}%", "Of all bookings", icon="alert",
                     delta="Monitor closely" if cancel_rate > 30 else "Healthy",
                     delta_positive=cancel_rate <= 30, glow_color=COLORS["red"])
    with c3:
        ui.kpi_card("Avg Daily Rate", f"${avg_adr:,.0f}", "Per booked night", icon="diamond",
                     delta="Premium tier", delta_positive=True, glow_color=COLORS["orange"])
    with c4:
        ui.kpi_card("Total Revenue", f"${total_revenue/1e6:,.2f}M", "Estimated, ADR × nights", icon="dollar",
                     delta="Strong performance", delta_positive=True, glow_color=COLORS["purple"])

    st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)

    col_left, col_mid, col_right = st.columns([1.1, 1.6, 1.1])

    with col_left:
        ui.glass_card_open()
        ui.section_title("Guest Journey", icon="route")
        st.plotly_chart(charts.guest_funnel(df), use_container_width=True, config={"displayModeBar": False})
        ui.glass_card_close()

    with col_mid:
        ui.glass_card_open()
        ui.section_title("Monthly Booking Trend", icon="trend-up")
        st.plotly_chart(charts.monthly_booking_trend(df), use_container_width=True, config={"displayModeBar": False})
        ui.glass_card_close()

    with col_right:
        ui.glass_card_open()
        ui.section_title("Booking Share", icon="pie")
        st.plotly_chart(charts.hotel_share_donut(df), use_container_width=True, config={"displayModeBar": False})
        ui.glass_card_close()

    st.markdown("<div style='height:1.4rem'></div>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1.4, 1])
    with col_a:
        ui.glass_card_open()
        ui.section_title("Cancellation Snapshot", icon="alert")
        col_x, col_y = st.columns(2)
        with col_x:
            st.plotly_chart(charts.cancellation_rate_by_hotel(df), use_container_width=True,
                             config={"displayModeBar": False})
        with col_y:
            repeat_rate = df["is_repeated_guest"].mean() * 100
            direct_rate = df["is_direct_booking"].mean() * 100
            special_rate = (df["total_of_special_requests"] > 0).mean() * 100
            parking_rate = (df["required_car_parking_spaces"] > 0).mean() * 100
            ui.animated_progress("Repeat Guests", repeat_rate, "Loyal, returning customers")
            ui.animated_progress("Direct Bookings", direct_rate, "No agent / company involved")
            ui.animated_progress("Special Requests", special_rate, "Guests requesting extras")
            ui.animated_progress("Needs Parking", parking_rate, "Requires car parking space")
        ui.glass_card_close()

    with col_b:
        ui.glass_card_open()
        ui.section_title("Market Segments", icon="layers")
        st.plotly_chart(charts.market_segment_bar(df), use_container_width=True, config={"displayModeBar": False})
        ui.glass_card_close()
