"""
config.py
---------
Central place for theme colors, page metadata, and shared constants.
Import from here instead of hardcoding colors/strings across pages.
"""

import os

APP_TITLE = "Hotel Analytics — VIP Business Intelligence"
APP_ICON = None

# Anchor every file path to this config.py's own location, not the process's
# working directory. Streamlit Cloud does not guarantee the working
# directory matches the app's folder (especially when app.py lives in a
# subfolder of the repo), so relative paths like "data/..." can silently
# resolve to the wrong place. Absolute, __file__-based paths always work
# regardless of where the app is launched from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "hotel_bookings_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "data", "cancellation_model.pkl")
CSS_PATH = os.path.join(BASE_DIR, "assets", "styles.css")

# ---------------------------------------------------------------
# Neon glassmorphism color palette (matches the reference mockup)
# ---------------------------------------------------------------
COLORS = {
    "bg_dark": "#0d0221",
    "bg_darker": "#08011a",
    "panel_glass": "rgba(255, 255, 255, 0.05)",
    "panel_border": "rgba(255, 255, 255, 0.12)",
    "pink": "#ff2ea6",
    "pink_soft": "#ff6ec7",
    "purple": "#8b2fe0",
    "purple_deep": "#4a0e8f",
    "violet": "#a259ff",
    "orange": "#ff8a3d",
    "red": "#ff3b5c",
    "text_primary": "#f5f3ff",
    "text_muted": "#b8a9d9",
    "success": "#3ddc97",
    "warning": "#ffd166",
}

# Gradient sequences reused by every Plotly chart to keep a consistent look
GRADIENT_SEQUENTIAL = ["#4a0e8f", "#8b2fe0", "#c93bd6", "#ff2ea6", "#ff8a3d"]
GRADIENT_DIVERGING = ["#3ddc97", "#a259ff", "#ff2ea6", "#ff3b5c"]
HOTEL_COLOR_MAP = {"City Hotel": "#ff2ea6", "Resort Hotel": "#8b2fe0"}
STATUS_COLOR_MAP = {"Completed": "#3ddc97", "Canceled": "#ff3b5c"}

PLOTLY_TEMPLATE = "plotly_dark"

NAV_PAGES = [
    {"key": "home", "label": "Home", "icon": "home"},
    {"key": "analytics", "label": "Analytics", "icon": "bar-chart"},
    {"key": "ai_insights", "label": "AI Insights", "icon": "cpu"},
    {"key": "dataset_explorer", "label": "Dataset Explorer", "icon": "folder"},
    {"key": "profile", "label": "Profile", "icon": "user"},
]
