# Hotel Analytics — VIP Business Intelligence Dashboard

A production-ready, multi-page Streamlit dashboard for hotel booking and
cancellation analysis, built on a real 2017–2019 hotel bookings dataset
(119,390 raw rows, 29 columns). Styled with a glassmorphism + neon
pink/purple theme, animated UI elements, interactive Plotly charts, and
a live machine learning cancellation-risk predictor.

---

## Features

- **5-page app** with a custom animated sidebar nav (Home, Analytics,
  AI Insights, Dataset Explorer, Profile)
- **Glassmorphism / neon pink-purple theme** with glowing cards, animated
  gradients, hover transitions, and a shimmering VIP badge
- **Real data cleaning pipeline** (`data/data_processor.py`) — handles
  missing values, duplicate rows, inconsistent categories, and numeric
  anomalies, fully documented and justified
- **Interactive Plotly charts** — donut, funnel, violin, treemap, ROC
  curve, confusion matrix, and more, all themed consistently
- **Real trained ML model** (`data/model.py`) — a scikit-learn
  `GradientBoostingClassifier` predicting cancellation risk, with a
  live "what-if" predictor for hypothetical bookings
- Answers the **3 core business questions**: hotel type popularity &
  seasonality, stay-duration vs. cancellation, lead-time vs. cancellation

---

## Project Structure

```
hotel-dashboard/
├── app.py                       # Main entry point (run this)
├── config.py                    # Theme colors, page metadata, constants
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml              # Streamlit theme + server config
├── assets/
│   └── styles.css               # Glassmorphism/neon theme + animations
├── components/
│   ├── sidebar.py                # Sidebar navigation
│   ├── ui_elements.py            # KPI cards, headers, progress bars
│   └── charts.py                 # Reusable themed Plotly chart builders
├── data/
│   ├── hotel_bookings_data.csv   # Raw dataset
│   ├── data_processor.py         # Cleaning pipeline
│   └── model.py                  # ML model training/prediction
└── pages_content/
    ├── home.py
    ├── analytics.py
    ├── ai_insights.py
    ├── dataset_explorer.py
    └── profile.py
```

> **Note:** Page modules live in `pages_content/` rather than Streamlit's
> reserved `pages/` folder. This is intentional — it keeps our fully
> custom sidebar navigation in control instead of Streamlit's automatic
> native multi-page router taking over.

---

## Getting Started (VS Code / local)

1. **Clone or unzip** this project and open the folder in VS Code.

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**:
   ```bash
   streamlit run app.py
   ```

5. Your browser will open automatically at `http://localhost:8501`.

---

## ️ Deploying (e.g. Streamlit Community Cloud)

1. Push this project to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io), connect your
   GitHub account, and select the repo.
3. Set the **main file path** to `app.py`.
4. Deploy — `requirements.txt` and `.streamlit/config.toml` are already
   configured for a clean deploy.

---

## Data Cleaning Summary

| Issue | Rows Affected | Action Taken |
|---|---|---|
| Duplicate rows | 33,261 | Dropped |
| Missing `children` | 4 | Filled with 0 |
| Missing `city` | 488 | Filled with "Unknown" |
| Missing `agent` / `company` | 16,340 / 112,593 | Filled with 0 (a real category — "no agent/company") |
| `meal` = "Undefined" | 1,169 | Recoded to "No Meal" |
| Negative `adr` | 1 | Dropped |
| Extreme `adr` outlier | 1 | Capped at 99.9th percentile |
| Zero-guest bookings | 180 | Dropped |
| Invalid calendar dates (e.g. Sept 31, Feb 30) | 9 rows/date combos | Clamped to last valid day of month |

Full before/after detail is also viewable live on the **Dataset Explorer**
page inside the app.

---

## AI Insights

The AI Insights page trains a `GradientBoostingClassifier` on the cleaned
dataset (sampled to 40,000 rows for speed) using 21 booking features. It
reports accuracy, precision, recall, ROC-AUC, a confusion matrix, an ROC
curve, and feature importances — then lets you enter a hypothetical
booking to get a live predicted cancellation probability with an
actionable recommendation.

---

## ️ Tech Stack

Python · Streamlit · Pandas · NumPy · Plotly · Scikit-learn
