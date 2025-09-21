# settings.py
# Quick-Clip Clipboard Popup App
#
# Centralized configuration for window dimensions, theme colors, and button settings.
# Provides functions to load and save theme preferences.
#
# Author: Tof-O
# License: MIT

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
try:
    import winshell
except ImportError:
    winshell = None

COPY_FILE = os.path.join(os.path.dirname(__file__), 'copy.json')

def add_to_startup():
    """Add this app to Windows startup using a shortcut."""
    if winshell is None:
        return False
    exe_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'main.py'))
    startup = winshell.startup()
    shortcut = os.path.join(startup, 'Quick-Clip.lnk')
    if not os.path.exists(shortcut):
        from win32com.client import Dispatch
        shell = Dispatch('WScript.Shell')
        shortcut_obj = shell.CreateShortCut(shortcut)
        shortcut_obj.Targetpath = exe_path
        shortcut_obj.WorkingDirectory = os.path.dirname(exe_path)
        shortcut_obj.save()
    return True

def load_copies():
    """Load clipboard history from copy.json."""
    if os.path.exists(COPY_FILE):
        try:
            with open(COPY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_copies(items):
    """Save clipboard history to copy.json."""
    try:
        with open(COPY_FILE, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".clipboard_popup_theme.json")

def load_theme():
    """Load the theme from the configuration file."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
                return data.get("theme", DEFAULT_THEME)
        except Exception:
            return DEFAULT_THEME
    return DEFAULT_THEME

def save_theme(theme):
    """Save the selected theme to the configuration file."""
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump({"theme": theme}, f)
    except Exception:
        pass
