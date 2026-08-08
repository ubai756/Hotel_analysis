"""
config.py
---------
Central place for theme colors, page metadata, and shared constants.
Import from here instead of hardcoding colors/strings across pages.
"""

APP_TITLE = "Hotel Analytics — VIP Business Intelligence"
APP_ICON = None
DATA_PATH = "data/hotel_bookings_data.csv"
MODEL_PATH = "data/cancellation_model.pkl"

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
