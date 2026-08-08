"""
analytics.py
------------
Answers the 3 business questions from the project brief:
  1. Which hotel type do customers book most often, and what's the
     seasonal pattern?
  2. Does length of stay affect cancellation rate?
  3. Does lead time affect cancellation rate?

Each is presented as its own tab with chart + auto-generated narrative
insight, followed by ADR / market-segment / deposit-type deep dives.
"""

import streamlit as st

from components import ui_elements as ui
from components import charts


def render(df):
    ui.page_header(
        "Business Analytics",
        "Answers to the three core business questions, backed by the cleaned dataset.",
        badge="ANALYTICS",
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "Hotel Type & Seasonality",
        "Stay Duration Impact",
        "Lead Time Impact",
        "Revenue & Segments",
    ])

    # ---------------- Q1: Hotel type popularity + seasonality ----------------
    with tab1:
        col1, col2 = st.columns([1, 1.6])
        with col1:
            ui.glass_card_open()
            ui.section_title("Booking Share", icon="pie")
            st.plotly_chart(charts.hotel_share_donut(df), use_container_width=True,
                             config={"displayModeBar": False})
            ui.glass_card_close()
        with col2:
            ui.glass_card_open()
            ui.section_title("Monthly Trend by Hotel Type", icon="trend-up")
            st.plotly_chart(charts.monthly_booking_trend(df), use_container_width=True,
                             config={"displayModeBar": False})
            ui.glass_card_close()

        city_share = (df["hotel"] == "City Hotel").mean() * 100
        peak_month = df.groupby("arrival_date_month").size().idxmax()
        low_month = df.groupby("arrival_date_month").size().idxmin()

        ui.glass_card_open("margin-top:1rem;")
        st.markdown(f"""
        **Key Insight:** City Hotel accounts for **{city_share:.0f}%** of all bookings, making it
        the more frequently booked property type. Demand peaks in **{peak_month}** and dips lowest in
        **{low_month}**, a pattern consistent with holiday travel and seasonal leisure demand.

        **Recommendation:** Launch targeted seasonal promotions for the Resort Hotel during off-peak
        months to balance occupancy, and pre-emptively scale staffing/inventory ahead of the
        {peak_month} peak.
        """)
        ui.glass_card_close()

    # ---------------- Q2: Stay duration vs cancellation ----------------
    with tab2:
        ui.glass_card_open()
        ui.section_title("Cancellation Rate vs. Length of Stay", icon="bar-chart")
        st.plotly_chart(charts.cancellation_by_stay_length(df), use_container_width=True,
                         config={"displayModeBar": False})
        ui.glass_card_close()

        short_stay_rate = df[df["total_nights"] <= 1]["is_canceled"].mean() * 100
        long_stay_rate = df[df["total_nights"] >= 8]["is_canceled"].mean() * 100
        direction = "increases" if long_stay_rate > short_stay_rate else "decreases"

        ui.glass_card_open("margin-top:1rem;")
        st.markdown(f"""
        **Key Insight:** Cancellation rate {direction} with stay length — single-night stays cancel
        at **{short_stay_rate:.1f}%**, versus **{long_stay_rate:.1f}%** for stays of 8+ nights. Longer,
        more expensive bookings appear to carry more uncertainty, likely from advance planning risk.

        **Recommendation:** Apply stricter cancellation terms or a non-refundable deposit tier for
        long-stay bookings, while keeping short-stay policies flexible to protect conversion.
        """)
        ui.glass_card_close()

    # ---------------- Q3: Lead time vs cancellation ----------------
    with tab3:
        ui.glass_card_open()
        ui.section_title("Cancellation Rate vs. Lead Time", icon="alert")
        st.plotly_chart(charts.cancellation_by_lead_time(df), use_container_width=True,
                         config={"displayModeBar": False})
        ui.glass_card_close()

        near_rate = df[df["lead_time"] <= 7]["is_canceled"].mean() * 100
        far_rate = df[df["lead_time"] > 180]["is_canceled"].mean() * 100

        ui.glass_card_open("margin-top:1rem;")
        st.markdown(f"""
        **Key Insight:** Bookings made within a week of arrival cancel at **{near_rate:.1f}%**,
        while bookings made more than 6 months in advance cancel at **{far_rate:.1f}%** — cancellation
        risk rises sharply the further out a guest books.

        **Recommendation:** For bookings with 180+ day lead times, trigger automated reminder emails,
        require a partial deposit at booking, and offer a one-time free reschedule instead of outright
        cancellation to preserve revenue.
        """)
        ui.glass_card_close()

    # ---------------- Extra: revenue / segment deep dive ----------------
    with tab4:
        col1, col2 = st.columns(2)
        with col1:
            ui.glass_card_open()
            ui.section_title("ADR Distribution", icon="dollar")
            st.plotly_chart(charts.adr_distribution(df), use_container_width=True,
                             config={"displayModeBar": False})
            ui.glass_card_close()
        with col2:
            ui.glass_card_open()
            ui.section_title("Deposit Type vs. Outcome", icon="credit-card")
            st.plotly_chart(charts.deposit_type_treemap(df), use_container_width=True,
                             config={"displayModeBar": False})
            ui.glass_card_close()

        ui.glass_card_open("margin-top:1rem;")
        ui.section_title("Bookings by Market Segment", icon="layers")
        st.plotly_chart(charts.market_segment_bar(df), use_container_width=True,
                         config={"displayModeBar": False})
        ui.glass_card_close()
