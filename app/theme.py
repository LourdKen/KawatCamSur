
DARK = {
    "BG": "#0B1120",
    "SIDEBAR": "#111C2F",
    "CARD": "#182235",
    "BORDER": "#273449",
    "GREEN": "#84CC16",
    "ACTIVE_BG": "#26351F",
    "WHITE": "#F8FAFC",
    "MUTED": "#94A3B8",
}

LIGHT = {
    "BG": "#F1F5F9",
    "SIDEBAR": "#FFFFFF",
    "CARD": "#FFFFFF",
    "BORDER": "#E2E8F0",
    "GREEN": "#65A30D",
    "ACTIVE_BG": "#ECFCCB",
    "WHITE": "#0F172A",
    "MUTED": "#64748B",
}

current_theme = "dark"


def get_colors():
    return DARK if current_theme == "dark" else LIGHT


def set_theme(value):
    global current_theme
    current_theme = value
