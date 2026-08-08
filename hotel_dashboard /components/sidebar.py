"""
sidebar.py
----------
Renders the VIP sidebar navigation: brand header, icon-labeled nav
buttons for each page, and a footer status chip. Uses st.session_state
to track and highlight the active page.

Native Streamlit buttons can only render plain text (no HTML/SVG), so
each icon is injected as a CSS background-image directly on the
button itself, scoped via the `.st-key-<key>` class Streamlit attaches
to a widget's wrapper when a `key` is given. This keeps the icon truly
inside the gradient button box instead of floating beside it.
"""

import streamlit as st
from config import NAV_PAGES
from components.icons import icon_svg, icon_data_uri

BRAND_ICON_COLOR = "#ff6ec7"
NAV_ICON_COLOR = "#ffffff"


def _nav_icon_css() -> str:
    """Builds one <style> block with a background-image rule per nav button,
    scoped to that button's unique Streamlit key, so the icon renders
    truly inside the gradient button instead of beside it."""
    rules = []
    for page in NAV_PAGES:
        data_uri = icon_data_uri(page["icon"], color=NAV_ICON_COLOR, stroke_width=2.2)
        key = f"nav_{page['key']}"
        rules.append(f"""
        div.st-key-{key} button {{
            position: relative;
            padding-left: 2.4rem !important;
            text-align: left !important;
        }}
        div.st-key-{key} button::before {{
            content: "";
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            width: 18px;
            height: 18px;
            background-image: {data_uri};
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
        }}
        """)
    return "<style>" + "\n".join(rules) + "</style>"


def render_sidebar() -> str:
    """Renders the sidebar and returns the currently selected page key."""

    if "active_page" not in st.session_state:
        st.session_state.active_page = "home"

    with st.sidebar:
        st.markdown(_nav_icon_css(), unsafe_allow_html=True)

        st.markdown(
            f"""
            <div style="text-align:center; padding: 0.4rem 0 1.2rem 0;">
                <div style="margin-bottom:0.4rem;">
                    {icon_svg("building", size=34, color=BRAND_ICON_COLOR, stroke_width=1.5)}
                </div>
                <div style="font-family:'Space Grotesk',sans-serif; font-weight:800;
                            font-size:1.15rem; color:#fff; letter-spacing:0.04em;">
                    HOTEL ANALYTICS
                </div>
                <div style="font-size:0.68rem; letter-spacing:0.18em; color:#d9a9ff;
                            text-transform:uppercase; margin-top:0.1rem;">
                    Business Intelligence
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="vip-badge" style="display:flex; justify-content:center; align-items:center;
                        gap:0.4rem; margin: 0 auto 1.4rem auto; width:fit-content;">
                ✦ VIP DASHBOARD
            </div>
            """,
            unsafe_allow_html=True,
        )

        for page in NAV_PAGES:
            is_active = st.session_state.active_page == page["key"]
            wrapper_class = "nav-active" if is_active else "nav-inactive"
            st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
            if st.button(page["label"], key=f"nav_{page['key']}", use_container_width=True):
                st.session_state.active_page = page["key"]
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="glass-card" style="padding:0.9rem 1rem; text-align:center;">
                <div style="font-size:0.72rem; color:#b8a9d9; letter-spacing:0.05em;">
                    LIVE DATA STATUS
                </div>
                <div style="color:#3ddc97; font-weight:700; font-size:0.85rem; margin-top:0.25rem;
                            display:flex; align-items:center; justify-content:center; gap:0.35rem;">
                    {icon_svg("check-circle", size=15, color="#3ddc97")} Connected &amp; Cleaned
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return st.session_state.active_page
