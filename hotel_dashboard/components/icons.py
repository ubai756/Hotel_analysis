"""
icons.py
--------
A small library of clean, monochrome line-style SVG icons, sized and
colored to match the dashboard's neon glassmorphism theme. Used
everywhere emoji used to be (sidebar nav, KPI cards, section titles,
tabs, buttons) so the whole UI reads as one deliberate, VIP-grade
design system instead of relying on platform emoji glyphs.

Usage:
    from components.icons import icon
    st.markdown(icon("building", size=20, color="#ff6ec7"), unsafe_allow_html=True)
"""

# Each entry is the <path>/<g> inner content of a 24x24 viewBox line icon.
# Stroke-based, no fill, so a single `color` argument recolors the whole glyph.
_ICONS = {
    "building": '<path d="M4 21V5a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v16"/><path d="M15 9h4a1 1 0 0 1 1 1v11"/><path d="M9 8h.01M12 8h.01M9 11h.01M12 11h.01M9 14h.01M12 14h.01M9 17h.01M12 17h.01M18 13h.01M18 16h.01M2 21h20"/>',
    "calendar": '<rect x="3" y="4.5" width="18" height="16" rx="2"/><path d="M16 2.5v4M8 2.5v4M3 9.5h18"/>',
    "alert": '<path d="M10.3 3.9 1.9 18a2 2 0 0 0 1.7 3h16.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/><path d="M12 9v4M12 17h.01"/>',
    "diamond": '<path d="M6 3h12l4 6-10 12L2 9Z"/><path d="M2 9h20M11 3 8 9l4 12 4-12-3-6"/>',
    "dollar": '<path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    "route": '<circle cx="6" cy="19" r="2"/><circle cx="18" cy="5" r="2"/><path d="M8 19h7a4 4 0 0 0 4-4V8a4 4 0 0 0-4-4h-1"/>',
    "trend-up": '<path d="M3 17 9 11l4 4 8-8"/><path d="M17 7h4v4"/>',
    "pie": '<path d="M21.2 15.3A10 10 0 1 1 8.7 2.8"/><path d="M22 12A10 10 0 0 0 12 2v10Z"/>',
    "layers": '<path d="m12 2 9 5-9 5-9-5 9-5Z"/><path d="m3 12 9 5 9-5M3 17l9 5 9-5"/>',
    "credit-card": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/>',
    "cpu": '<rect x="6" y="6" width="12" height="12" rx="1"/><rect x="10" y="10" width="4" height="4"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    "search": '<circle cx="10.5" cy="10.5" r="7"/><path d="m20.5 20.5-4.8-4.8"/>',
    "radio": '<circle cx="12" cy="12" r="2.2"/><path d="M8.5 8.5a5 5 0 0 0 0 7M15.5 15.5a5 5 0 0 0 0-7M5.5 5.5a9.5 9.5 0 0 0 0 13M18.5 18.5a9.5 9.5 0 0 0 0-13"/>',
    "bolt": '<path d="M13 2 3 14h7l-1 8 11-13h-7l1-7Z"/>',
    "dice": '<rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8" cy="8" r="1.2"/><circle cx="16" cy="8" r="1.2"/><circle cx="8" cy="16" r="1.2"/><circle cx="16" cy="16" r="1.2"/><circle cx="12" cy="12" r="1.2"/>',
    "folder": '<path d="M3 6a1 1 0 0 1 1-1h5l2 2.5h9a1 1 0 0 1 1 1V18a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V6Z"/>',
    "download": '<path d="M12 3v13"/><path d="m7 11 5 5 5-5"/><path d="M4 21h16"/>',
    "trash": '<path d="M4 7h16"/><path d="M9 7V4h6v3"/><path d="M6 7l1 13a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1l1-13"/><path d="M10 11v6M14 11v6"/>',
    "check-circle": '<circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.5 2.5L16 9.5"/>',
    "inbox": '<path d="M4 12h4l2 3h4l2-3h4"/><path d="M5.3 5a1 1 0 0 1 .9-.6h11.6a1 1 0 0 1 .9.6L21 12v6a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-6l2.3-7Z"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.6-4 5-6 8-6s6.4 2 8 6"/>',
    "home": '<path d="m3 11 9-8 9 8"/><path d="M5 10v10a1 1 0 0 0 1 1h4v-6h4v6h4a1 1 0 0 0 1-1V10"/>',
    "bar-chart": '<path d="M4 21V10M12 21V4M20 21v-7"/><path d="M2 21h20"/>',
    "sparkle": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
    "shield": '<path d="M12 3 4.5 6v6c0 5 3.4 8.4 7.5 9 4.1-.6 7.5-4 7.5-9V6L12 3Z"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5h.01"/>',
    "star": '<path d="m12 3 2.6 5.9 6.4.6-4.8 4.3 1.4 6.2L12 16.9 6.4 20l1.4-6.2-4.8-4.3 6.4-.6L12 3Z"/>',
}


def icon_svg(name: str, size: int = 18, color: str = "currentColor", stroke_width: float = 1.8) -> str:
    """Returns a standalone <svg> string for the named icon."""
    inner = _ICONS.get(name, _ICONS["sparkle"])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round" '
        f'style="display:inline-block; vertical-align:middle; flex-shrink:0;">{inner}</svg>'
    )


def icon_html(name: str, size: int = 18, color: str = "currentColor", stroke_width: float = 1.8) -> str:
    """Same as icon_svg, alias kept for readability at call sites."""
    return icon_svg(name, size=size, color=color, stroke_width=stroke_width)


def icon_data_uri(name: str, color: str = "#ffffff", stroke_width: float = 2.0) -> str:
    """
    Returns a CSS-ready `url("data:image/svg+xml,...")` string for the
    named icon. Used to inject an icon as a CSS background-image on
    elements (like native Streamlit buttons) that can't render raw
    HTML/SVG directly, so the icon can sit truly *inside* the element
    instead of alongside it.

    `color` is a normal hex color (e.g. "#ffffff") — encoding for the
    data URI is handled internally.
    """
    inner = _ICONS.get(name, _ICONS["sparkle"])
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
        f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" '
        f'stroke-linejoin="round">{inner}</svg>'
    )
    # URL-encode the characters that break a data URI when left raw
    svg = svg.replace("#", "%23").replace('"', "'").replace("<", "%3C").replace(">", "%3E")
    return f'url("data:image/svg+xml,{svg}")'
