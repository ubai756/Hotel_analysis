"""
ui_elements.py
--------------
Small reusable HTML/CSS-driven UI building blocks: KPI cards, page
headers, section titles, animated progress bars, and status pills.
Keeping these in one place means every page renders visually identical
"glass" components instead of re-implementing markup each time.
"""

from typing import Optional

import streamlit as st
from components.icons import icon_svg


def page_header(title: str, subtitle: str = "", badge: Optional[str] = None, title_icon: Optional[str] = None):
    badge_html = f'<span class="vip-badge" style="margin-left:0.8rem;">{badge}</span>' if badge else ""
    icon_html = f' {icon_svg(title_icon, size=26, color="#ff6ec7", stroke_width=2)}' if title_icon else ""
    st.markdown(
        f"""
        <div class="page-header" style="margin-bottom:1.4rem;">
            <h1>{title}{icon_html} {badge_html}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(text: str, icon: Optional[str] = None, icon_color: str = "#ff6ec7"):
    icon_html = f'<span style="display:inline-flex; margin-right:0.5rem;">{icon_svg(icon, size=17, color=icon_color)}</span>' if icon else ""
    st.markdown(
        f"""
        <div class="section-title">
            <span class="accent-bar"></span>{icon_html}<span>{text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, caption: str = "", icon: Optional[str] = None,
             delta: Optional[str] = None, delta_positive: bool = True,
             glow_color: str = "#ff2ea6"):
    delta_html = ""
    if delta:
        cls = "kpi-delta-up" if delta_positive else "kpi-delta-down"
        arrow = "▲" if delta_positive else "▼"
        delta_html = f'<div class="{cls}">{arrow} {delta}</div>'

    icon_html = f'<span style="display:inline-flex;">{icon_svg(icon, size=15, color=glow_color)}</span>' if icon else ""

    st.markdown(
        f"""
        <div class="kpi-card" style="--glow-color:{glow_color};">
            <div class="kpi-label">{icon_html}<span>{label}</span></div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-caption">{caption}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def glass_card_open(extra_style: str = ""):
    st.markdown(f'<div class="glass-card" style="{extra_style}">', unsafe_allow_html=True)


def glass_card_close():
    st.markdown("</div>", unsafe_allow_html=True)


def animated_progress(label: str, percent: float, caption: str = ""):
    percent = max(0, min(100, percent))
    st.markdown(
        f"""
        <div style="margin-bottom:1rem;">
            <div style="display:flex; justify-content:space-between; font-size:0.82rem;
                        color:#f5f3ff; font-weight:600;">
                <span>{label}</span><span>{percent:.0f}%</span>
            </div>
            <div class="progress-bar-track">
                <div class="progress-bar-fill" style="width:{percent:.0f}%;"></div>
            </div>
            <div style="font-size:0.72rem; color:#b8a9d9; margin-top:0.2rem;">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_pill(text: str, tone: str = "success"):
    colors = {
        "success": ("#3ddc97", "rgba(61,220,151,0.15)"),
        "warning": ("#ffd166", "rgba(255,209,102,0.15)"),
        "danger": ("#ff3b5c", "rgba(255,59,92,0.15)"),
        "info": ("#a259ff", "rgba(162,89,255,0.15)"),
    }
    fg, bg = colors.get(tone, colors["info"])
    st.markdown(
        f"""
        <span style="background:{bg}; color:{fg}; padding:0.3rem 0.8rem; border-radius:999px;
                      font-size:0.78rem; font-weight:700; border:1px solid {fg}55;">
            {text}
        </span>
        """,
        unsafe_allow_html=True,
    )
