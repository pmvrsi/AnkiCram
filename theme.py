import re
from aqt.qt import QColor

VERSION = "v1.0.2"

THEME = {
    "bg": "#030712",
    "glass": "rgba(255, 255, 255, 0.03)",
    "glass_hover": "rgba(255, 255, 255, 0.06)",
    "glass_border": "rgba(255, 255, 255, 0.1)",
    "primary": "#a78bfa",
    "primary_grad": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #a78bfa, stop:1 #6366f1)",
    "secondary": "#22d3ee",
    "text": "#f8fafc",
    "text_muted": "#94a3b8",
    "success": "#4ade80",
    "danger": "#ef4444",
    "danger_bg": "rgba(239, 68, 68, 0.1)"
}

STYLESHEET = f"""
    QLabel {{
        color: {THEME['text']};
        font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', sans-serif;
    }}
    QScrollBar:vertical {{
        border: none;
        background: transparent;
        width: 4px;
        margin: 0px; 
    }}
    QScrollBar::handle:vertical {{
        background: {THEME['glass_border']};
        min-height: 20px;
        border-radius: 2px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        border: none;
        background: none;
        height: 0px;
    }}
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
        border: none;
        background: none;
        height: 0px;
    }}
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
        background: none;
    }}
    QLineEdit {{
        padding: 12px;
        border: 1px solid {THEME['glass_border']};
        border-radius: 8px;
        background: rgba(0, 0, 0, 0.3);
        color: {THEME['text']};
        font-size: 14px;
    }}
    QLineEdit:focus {{ border: 1px solid {THEME['primary']}; }}
    QCheckBox {{
        color: {THEME['text_muted']};
        spacing: 10px;
        font-size: 13px;
        background: transparent;
        border: none;
        padding: 5px;
    }}
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border-radius: 4px;
        border: 1px solid {THEME['glass_border']};
        background: rgba(255, 255, 255, 0.05);
    }}
    QCheckBox::indicator:hover {{
        border: 1px solid {THEME['primary']};
        background: rgba(167, 139, 250, 0.1);
    }}
    QCheckBox::indicator:checked {{
        background-color: {THEME['primary']};
        border: 1px solid {THEME['primary']};
    }}
"""


def css_to_qcolor(css_str: str) -> QColor:
    if not css_str or css_str == "transparent":
        return QColor(0, 0, 0, 0)
    
    rgba_match = re.match(r"rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)", css_str)
    if rgba_match:
        r, g, b, a = rgba_match.groups()
        return QColor(int(r), int(g), int(b), int(float(a) * 255))
    
    return QColor(css_str)

