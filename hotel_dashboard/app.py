"""
app.py
------
Main entry point for the Hotel Analytics VIP dashboard.

Run with:
    streamlit run app.py

Responsibilities:
  - Configure the Streamlit page (title, icon, wide layout)
  - Inject the glassmorphism/neon theme CSS
  - Load and cache the cleaned dataset
  - Render the sidebar and route to the selected page module
"""

import streamlit as st

from config import APP_TITLE, APP_ICON, DATA_PATH
from data.data_processor import load_and_clean_data
from components.sidebar import render_sidebar

from pages_content import home, analytics, ai_insights, dataset_explorer, profile

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_css():
    with open("assets/styles.css", "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


@st.cache_data(show_spinner="Loading and cleaning hotel booking data...")
def get_data():
    return load_and_clean_data(DATA_PATH)


PAGES = {
    "home": home,
    "analytics": analytics,
    "ai_insights": ai_insights,
    "dataset_explorer": dataset_explorer,
    "profile": profile,
}


def main():
    inject_css()
    df = get_data()

    active_page = render_sidebar()

    page_module = PAGES.get(active_page, home)
    page_module.render(df)


if __name__ == "__main__":
    main()
