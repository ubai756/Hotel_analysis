"""
profile.py
----------
Display-only about/profile page. Summarizes the project, tech stack,
and data source — no authentication, just a polished info page.
"""

import streamlit as st

from components import ui_elements as ui
from components.icons import icon_svg


def render(df):
    ui.page_header("Profile", "About this dashboard and the project behind it.", badge="ABOUT")

    col1, col2 = st.columns([1, 2])

    with col1:
        ui.glass_card_open("text-align:center;")
        st.markdown(
            f"""
            <div style="margin-bottom:0.6rem;">{icon_svg("building", size=44, color="#ff6ec7", stroke_width=1.4)}</div>
            <div style="font-family:'Space Grotesk',sans-serif; font-weight:800; font-size:1.3rem; color:#fff;">
                Hotel Analytics
            </div>
            <div style="color:#b8a9d9; font-size:0.85rem; margin-top:0.2rem;">
                VIP Business Intelligence Suite
            </div>
            <div style="margin-top:1rem;">
            """,
            unsafe_allow_html=True,
        )
        ui.status_pill("● VIP TIER", tone="info")
        st.markdown("</div>", unsafe_allow_html=True)
        ui.glass_card_close()

    with col2:
        ui.glass_card_open()
        ui.section_title("Project Overview", icon="info")
        st.markdown(f"""
        This dashboard investigates hotel booking and cancellation behavior across
        **{df['arrival_date_year'].min()}–{df['arrival_date_year'].max()}**, using a real-world
        dataset of **{len(df):,} cleaned bookings**. It answers three core business questions —
        hotel type popularity, the effect of stay duration on cancellations, and the effect of
        lead time on cancellations — and layers on a live machine learning model for predictive
        cancellation risk.
        """)
        ui.glass_card_close()

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    ui.glass_card_open()
    ui.section_title("Tech Stack", icon="layers")
    tech_cols = st.columns(5)
    stack = [
        ("cpu", "Python"), ("bolt", "Streamlit"), ("bar-chart", "Pandas / NumPy"),
        ("trend-up", "Plotly"), ("target", "Scikit-learn"),
    ]
    for col, (icon_name, name) in zip(tech_cols, stack):
        with col:
            st.markdown(
                f"""
                <div class="glass-card" style="text-align:center; padding:1rem 0.5rem;">
                    <div>{icon_svg(icon_name, size=26, color="#a259ff", stroke_width=1.6)}</div>
                    <div style="font-size:0.82rem; color:#f5f3ff; margin-top:0.4rem; font-weight:600;">{name}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    ui.glass_card_close()

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        ui.glass_card_open()
        ui.section_title("Data Source", icon="folder")
        st.markdown("""
        Hotel bookings dataset (2017–2019), 119,390 raw records across 29 columns,
        covering City Hotel and Resort Hotel properties. Cleaned in `data_processor.py`
        to remove duplicates, fix missing values, standardize categories, and correct
        numeric anomalies before analysis.
        """)
        ui.glass_card_close()
    with col_b:
        ui.glass_card_open()
        ui.section_title("Dashboard Pages", icon="layers")
        st.markdown("""
        - **Home** — executive KPI overview
        - **Analytics** — the 3 core business questions
        - **AI Insights** — live ML cancellation risk model
        - **Dataset Explorer** — cleaning report & filterable data
        - **Profile** — this page
        """)
        ui.glass_card_close()
