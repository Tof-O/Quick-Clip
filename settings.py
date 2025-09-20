WINDOW_WIDTH = 350
WINDOW_HEIGHT = 400
DEFAULT_THEME = "light"

THEME_COLORS = {
    "light": {
        "border": "#000000",
        "bg": "#fff",
        "label": "#222",
        "btn_bg": "#eee",
        "btn_fg": "#222",
        "btn_hover": "#ccc"
    },
    "dark": {
        "border": "#ffffff",
        "bg": "#232629",
        "label": "#f0f0f0",
        "btn_bg": "#444",
        "btn_fg": "#fff",
        "btn_hover": "#666"
    }
}

BUTTON_CONFIG = {
    "theme": {"text_light": "🌙", "text_dark": "☀️", "size": (32, 32)},
    "close": {"text": "✕", "size": (32, 32)},
    "back": {"text": "←", "size": (32, 32)},
    "paste": {"text": "📋 Paste", "size": (80, 32)},
    "edit": {"text": "✏️ Edit", "size": (60, 32)},
    "save": {"text": "💾 Save", "size": (70, 32)},
    "cancel": {"text": "Cancel", "size": (80, 32)},
    "tab_paste": {"text": "📋", "size": (32, 28)},
    "tab_bullet": {"text": "⋮"}
}

import os, json
CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".clipboard_popup_theme.json")

def load_theme():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
                return data.get("theme", DEFAULT_THEME)
        except Exception:
            return DEFAULT_THEME
    return DEFAULT_THEME

def save_theme(theme):
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump({"theme": theme}, f)
    except Exception:
        pass
