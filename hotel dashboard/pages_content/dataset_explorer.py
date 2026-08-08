"""
dataset_explorer.py
--------------------
Transparency page: shows exactly what the cleaning pipeline changed
(before/after), lets the manager filter and browse the cleaned data,
and offers a CSV download of the filtered view.
"""

import streamlit as st
import pandas as pd

from components import ui_elements as ui
from data.data_processor import get_cleaning_report
from config import DATA_PATH


def render(df):
    ui.page_header(
        "Dataset Explorer",
        "Full transparency on data cleaning, plus a live filterable view of the cleaned dataset.",
        badge="TRANSPARENT",
    )

    report = get_cleaning_report(DATA_PATH)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        ui.kpi_card("Raw Rows", f"{report['raw_rows']:,}", "Before cleaning", icon="inbox")
    with c2:
        ui.kpi_card("Duplicates Removed", f"{report['duplicates_removed']:,}", "Exact duplicate rows", icon="trash")
    with c3:
        ui.kpi_card("Clean Rows", f"{report['clean_rows']:,}", "Analysis-ready", icon="check-circle")
    with c4:
        pct = report["rows_removed"] / report["raw_rows"] * 100
        ui.kpi_card("Rows Removed", f"{pct:.1f}%", "Duplicates + anomalies", icon="trash")

    st.markdown("<div style='height:1.4rem'></div>", unsafe_allow_html=True)

    ui.glass_card_open()
    ui.section_title("Missing Values — Before vs. After Cleaning", icon="shield")
    missing_before = {k: v for k, v in report["missing_before"].items() if v > 0}
    missing_after = {k: v for k, v in report["missing_after"].items() if v > 0}
    comp = pd.DataFrame({
        "Column": list(missing_before.keys()),
        "Missing (Raw)": list(missing_before.values()),
        "Missing (Cleaned)": [missing_after.get(k, 0) for k in missing_before.keys()],
    })
    st.dataframe(comp, use_container_width=True, hide_index=True)
    st.markdown("""
    - `children` → filled with 0 (mode; assumes no children when unspecified)
    - `city` → filled with "Unknown" (preserves the booking record)
    - `agent` / `company` → filled with 0, since 0 is itself a meaningful category
      (booking made without an agent / not a corporate booking), not truly "missing"
    - `meal` "Undefined" values recoded to "No Meal" (same real-world meaning)
    - Negative and extreme `adr` outliers corrected; bookings with 0 total guests dropped
    """)
    ui.glass_card_close()

    st.markdown("<div style='height:1.4rem'></div>", unsafe_allow_html=True)

    ui.section_title("Filter & Browse Cleaned Data", icon="folder")
    ui.glass_card_open()

    f1, f2, f3, f4 = st.columns(4)
    with f1:
        hotel_filter = st.multiselect("Hotel Type", sorted(df["hotel"].unique()), default=list(df["hotel"].unique()))
    with f2:
        status_filter = st.multiselect("Booking Status", sorted(df["booking_status"].unique()),
                                        default=list(df["booking_status"].unique()))
    with f3:
        year_filter = st.multiselect("Arrival Year", sorted(df["arrival_date_year"].unique()),
                                      default=list(df["arrival_date_year"].unique()))
    with f4:
        segment_filter = st.multiselect("Market Segment", sorted(df["market_segment"].unique()),
                                         default=list(df["market_segment"].unique()))

    filtered = df[
        df["hotel"].isin(hotel_filter)
        & df["booking_status"].isin(status_filter)
        & df["arrival_date_year"].isin(year_filter)
        & df["market_segment"].isin(segment_filter)
    ]

    st.markdown(f"<p style='color:#b8a9d9;'>Showing <b style='color:#fff;'>{len(filtered):,}</b> of {len(df):,} cleaned records</p>",
                unsafe_allow_html=True)

    display_cols = [
        "hotel", "booking_status", "arrival_date_year", "arrival_date_month",
        "lead_time", "total_nights", "adults", "children", "meal", "market_segment",
        "deposit_type", "customer_type", "adr", "total_of_special_requests",
    ]
    st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True, height=420)

    csv = filtered[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button("Download Filtered Data (CSV)", data=csv, file_name="filtered_hotel_bookings.csv",
                        mime="text/csv", use_container_width=True)

    ui.glass_card_close()
