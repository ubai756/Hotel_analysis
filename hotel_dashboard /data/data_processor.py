"""
data_processor.py
------------------
Cleans and prepares the raw hotel bookings dataset for analysis and
visualization. Handles missing values, duplicate rows, inconsistent
categorical values, and numeric anomalies, then engineers a handful
of derived features used throughout the dashboard.

Usage:
    from data.data_processor import load_and_clean_data
    df = load_and_clean_data("data/hotel_bookings_data.csv")
"""

from __future__ import annotations

import os
import numpy as np
import pandas as pd

RAW_COLUMNS_EXPECTED = 29

# Month name -> number, used for building a real datetime column
MONTH_MAP = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12,
}


def _fix_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Missing value strategy (documented per-column):

    - children: 4 missing -> fill with 0 (mode; assume no children when unspecified)
    - city: missing -> fill with 'Unknown' (preserves the row, flags unknown origin)
    - agent: missing -> fill with 0 (0 = booking not made through an agent, a real category)
    - company: missing -> fill with 0 (0 = not a corporate/company booking, a real category)
    """
    df = df.copy()

    if "children" in df.columns:
        df["children"] = df["children"].fillna(0).astype(int)

    if "city" in df.columns:
        df["city"] = df["city"].fillna("Unknown")

    if "agent" in df.columns:
        df["agent"] = df["agent"].fillna(0).astype(int)

    if "company" in df.columns:
        df["company"] = df["company"].fillna(0).astype(int)

    return df


def _remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Drop fully duplicated rows (same values across every column)."""
    return df.drop_duplicates(keep="first").reset_index(drop=True)


def _standardize_categories(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recode ambiguous / inconsistent categorical values.

    - meal: 'Undefined' effectively means the same thing as 'No Meal'
      (SC / self-catering, no board plan selected) -> recode to 'No Meal'
    - hotel, deposit_type, customer_type, market_segment, distribution_channel:
      strip whitespace / normalize casing for consistency
    """
    df = df.copy()

    if "meal" in df.columns:
        df["meal"] = df["meal"].replace({"Undefined": "No Meal"})

    for col in ["hotel", "deposit_type", "customer_type", "market_segment",
                "distribution_channel", "reservation_status", "city"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df


def _clean_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle numeric anomalies:

    - adr (average daily rate): drop negative values (data entry errors),
      cap extreme outliers (> 99.9th percentile) to reduce chart distortion
    - zero-guest bookings: rows with 0 adults + 0 children + 0 babies are
      invalid (no one is actually staying) -> dropped
    """
    df = df.copy()

    if "adr" in df.columns:
        df = df[df["adr"] >= 0]
        cap = df["adr"].quantile(0.999)
        df["adr"] = df["adr"].clip(upper=cap)

    guest_cols = [c for c in ["adults", "children", "babies"] if c in df.columns]
    if guest_cols:
        total_guests = df[guest_cols].sum(axis=1)
        df = df[total_guests > 0]

    # Invalid calendar dates (e.g. Sept 31, Feb 29-31 in non-leap years) show
    # up in the raw data due to upstream entry errors. Clamp the day-of-month
    # to the last valid day of that month/year instead of dropping the row.
    if {"arrival_date_year", "arrival_date_month", "arrival_date_day_of_month"}.issubset(df.columns):
        month_num = df["arrival_date_month"].map(MONTH_MAP)
        days_in_month = pd.to_datetime(
            dict(year=df["arrival_date_year"], month=month_num, day=1)
        ) + pd.offsets.MonthEnd(0)
        max_day = days_in_month.dt.day
        df["arrival_date_day_of_month"] = np.minimum(df["arrival_date_day_of_month"], max_day)

    return df.reset_index(drop=True)


def _engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived columns used across the dashboard's charts and model."""
    df = df.copy()

    if {"stays_in_weekend_nights", "stays_in_weekdays_nights"}.issubset(df.columns):
        df["total_nights"] = df["stays_in_weekend_nights"] + df["stays_in_weekdays_nights"]

    if {"adults", "children", "babies"}.issubset(df.columns):
        df["total_guests"] = df["adults"] + df["children"] + df["babies"]

    if {"arrival_date_year", "arrival_date_month", "arrival_date_day_of_month"}.issubset(df.columns):
        month_num = df["arrival_date_month"].map(MONTH_MAP)
        df["arrival_date"] = pd.to_datetime(
            dict(year=df["arrival_date_year"], month=month_num, day=df["arrival_date_day_of_month"]),
            errors="coerce",
        )
        df["arrival_month_num"] = month_num

    if "lead_time" in df.columns:
        bins = [-1, 7, 30, 90, 180, 365, 10000]
        labels = ["0-7d", "8-30d", "31-90d", "91-180d", "181-365d", "365d+"]
        df["lead_time_bucket"] = pd.cut(df["lead_time"], bins=bins, labels=labels)

    if "total_nights" in df.columns:
        bins = [-1, 1, 3, 7, 14, 1000]
        labels = ["1 night", "2-3 nights", "4-7 nights", "8-14 nights", "15+ nights"]
        df["stay_length_bucket"] = pd.cut(df["total_nights"], bins=bins, labels=labels)

    if "is_canceled" in df.columns:
        df["booking_status"] = df["is_canceled"].map({0: "Completed", 1: "Canceled"})

    if {"agent", "company"}.issubset(df.columns):
        df["is_direct_booking"] = ((df["agent"] == 0) & (df["company"] == 0)).astype(int)

    return df


def load_and_clean_data(csv_path: str) -> pd.DataFrame:
    """
    Full cleaning pipeline: load raw CSV -> fix missing values ->
    remove duplicates -> standardize categories -> clean anomalies ->
    engineer features. Returns an analysis-ready DataFrame.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at: {csv_path}")

    df = pd.read_csv(csv_path)

    df = _fix_missing_values(df)
    df = _remove_duplicates(df)
    df = _standardize_categories(df)
    df = _clean_anomalies(df)
    df = _engineer_features(df)

    return df


def get_cleaning_report(raw_path: str) -> dict:
    """
    Produces a before/after summary of the cleaning pipeline, used by the
    Dataset Explorer page to show exactly what was fixed and why.
    """
    raw = pd.read_csv(raw_path)
    clean = load_and_clean_data(raw_path)

    report = {
        "raw_rows": len(raw),
        "raw_cols": raw.shape[1],
        "clean_rows": len(clean),
        "rows_removed": len(raw) - len(clean),
        "duplicates_removed": int(raw.duplicated().sum()),
        "missing_before": raw.isnull().sum().to_dict(),
        "missing_after": clean.isnull().sum().to_dict(),
    }
    return report
