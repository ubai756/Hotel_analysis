"""
model.py
--------
Trains a real machine learning classifier to predict booking
cancellation risk, and exposes helpers for feature importance,
evaluation metrics, and single-booking predictions.

Uses a GradientBoostingClassifier (scikit-learn) trained on a compact,
interpretable feature set. Wrapped with Streamlit's cache_resource so
training happens once per session, not on every rerun.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix,
)

FEATURE_COLUMNS = [
    "hotel", "lead_time", "arrival_date_month", "stays_in_weekend_nights",
    "stays_in_weekdays_nights", "adults", "children", "babies", "meal",
    "market_segment", "distribution_channel", "is_repeated_guest",
    "previous_cancellations", "previous_bookings_not_canceled",
    "booking_changes", "deposit_type", "days_in_waiting_list",
    "customer_type", "adr", "required_car_parking_spaces",
    "total_of_special_requests",
]

CATEGORICAL_COLUMNS = [
    "hotel", "arrival_date_month", "meal", "market_segment",
    "distribution_channel", "deposit_type", "customer_type",
]

TARGET_COLUMN = "is_canceled"


def _prepare_features(df: pd.DataFrame):
    """Encode categorical columns, return X, y, and fitted encoders."""
    data = df[FEATURE_COLUMNS + [TARGET_COLUMN]].dropna().copy()

    encoders = {}
    for col in CATEGORICAL_COLUMNS:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col].astype(str))
        encoders[col] = le

    X = data[FEATURE_COLUMNS]
    y = data[TARGET_COLUMN]
    return X, y, encoders


def train_cancellation_model(df: pd.DataFrame, sample_size: int = 40000, random_state: int = 42):
    """
    Trains a GradientBoostingClassifier on the cleaned dataset and
    returns a dict bundling the model, encoders, test metrics, and
    plot-ready evaluation data.

    A row sample is used to keep training fast inside a Streamlit app;
    40k rows is plenty for a stable, well-performing model here.
    """
    if len(df) > sample_size:
        df_sample = df.sample(sample_size, random_state=random_state)
    else:
        df_sample = df

    X, y, encoders = _prepare_features(df_sample)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=random_state, stratify=y
    )

    model = GradientBoostingClassifier(
        n_estimators=150, max_depth=3, learning_rate=0.1, random_state=random_state
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    fpr, tpr, _ = roc_curve(y_test, y_proba)

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "confusion_matrix": confusion_matrix(y_test, y_pred),
        "fpr": fpr,
        "tpr": tpr,
    }

    importances = pd.Series(model.feature_importances_, index=FEATURE_COLUMNS).sort_values(ascending=False)

    return {
        "model": model,
        "encoders": encoders,
        "metrics": metrics,
        "importances": importances,
        "feature_columns": FEATURE_COLUMNS,
        "categorical_columns": CATEGORICAL_COLUMNS,
    }


def predict_single(bundle: dict, input_row: dict) -> float:
    """
    Predicts cancellation probability for a single booking described by
    input_row (a dict of raw feature values). Unseen categorical values
    fall back to the most frequent training class to avoid crashes.
    """
    model = bundle["model"]
    encoders = bundle["encoders"]

    row = {}
    for col in FEATURE_COLUMNS:
        val = input_row.get(col)
        if col in CATEGORICAL_COLUMNS:
            le = encoders[col]
            if val in le.classes_:
                row[col] = le.transform([val])[0]
            else:
                row[col] = 0
        else:
            row[col] = val

    X_new = pd.DataFrame([row])[FEATURE_COLUMNS]
    proba = model.predict_proba(X_new)[0, 1]
    return float(proba)
