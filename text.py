# text.py
# Quick-Clip Clipboard Popup App
#
# This file contains clipboard monitoring logic, hotkey listeners, and tab row creation for displaying clipboard items.
# Manages clipboard history and theme persistence.
#
# Author: Tof-O
# License: MIT

from PySide6.QtCore import QTimer, Signal, QObject
import keyboard
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget
from settings import BUTTON_CONFIG

def create_tab_row(text, ts, on_preview, on_paste):
    tab_row = QHBoxLayout()
    bullet = QLabel(BUTTON_CONFIG['tab_bullet']['text'])
    bullet.setStyleSheet("font-size:18px; margin-right:8px;")
    tab_row.addWidget(bullet)
    tab_btn = QPushButton(f"{text[:32]}\n{ts}")
    tab_btn.setStyleSheet("text-align:left;")
    tab_btn.clicked.connect(lambda checked, i=text: on_preview(i))
    tab_row.addWidget(tab_btn, stretch=1)
    paste_btn = QPushButton(BUTTON_CONFIG['tab_paste']['text'])
    paste_btn.setFixedSize(*BUTTON_CONFIG['tab_paste']['size'])
    paste_btn.setStyleSheet("margin-left:8px;")
    paste_btn.clicked.connect(lambda checked, i=text: on_paste(i))
    tab_row.addWidget(paste_btn)
    tab_widget = QWidget()
    tab_widget.setLayout(tab_row)
    return tab_widget

class HotkeyListener(QObject):
    show_popup_signal = Signal(str)
    def __init__(self):
        super().__init__()
        self.items = []  # Each copy is a new tab, format: (text, timestamp)
        self.theme = self.load_theme()
        self.popup = None
        self.last_clipboard = ""
        self.show_popup_signal.connect(self.show_popup)
        keyboard.add_hotkey('ctrl+v', self.on_ctrl_v, suppress=True)
        keyboard.add_hotkey('ctrl+c', self.on_ctrl_c)
        self.clipboard_timer = QTimer()
        self.clipboard_timer.timeout.connect(self.check_clipboard)
        self.clipboard_timer.start(100)
    def load_theme(self):
        import os, json
        config_path = os.path.join(os.path.expanduser("~"), ".clipboard_popup_theme.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    data = json.load(f)
                    return data.get("theme", "light")
            except Exception:
                return "light"
        return "light"
    def check_clipboard(self):
        from PySide6.QtGui import QGuiApplication
        clipboard = QGuiApplication.instance().clipboard()
        if clipboard.mimeData().hasText():
            text = clipboard.text().strip()
            if text and text != self.last_clipboard and (not self.items or self.items[0][0] != text):
                from datetime import datetime
                ts = datetime.now().strftime(' %d-%m-%Y, %H:%M')
                self.items.insert(0, (text, ts))
                self.last_clipboard = text
                if self.popup and self.popup.isVisible():
                    self.popup.items = self.items
                    self.popup._init_ui()
                    self.popup.apply_theme()
    def on_ctrl_c(self):
        pass
    def on_ctrl_v(self):
        self.show_popup_signal.emit("")
    def show_popup(self, _):
        if not self.items:
            self.items.append(("(No copied items yet)", ""))
        self.theme = self.load_theme()
        if self.popup is None:
            from preview import PopupWindow
            self.popup = PopupWindow(self.items, theme=self.theme)
            def update_theme():
                self.theme = self.popup.theme
                self.save_theme(self.theme)
            self.popup.theme_btn.clicked.connect(update_theme)
        else:
            self.popup.items = self.items
            self.popup.theme = self.theme
            self.popup._init_ui()
            self.popup.apply_theme()
        self.popup.show_at_cursor()
    def save_theme(self, theme):
        import os, json
        config_path = os.path.join(os.path.expanduser("~"), ".clipboard_popup_theme.json")
        try:
            with open(config_path, "w") as f:
                json.dump({"theme": theme}, f)
        except Exception:
            pass
def update_clipboard_item(items, old_text, new_text):
    for idx, (txt, ts) in enumerate(items):
        if txt == old_text:
            items[idx] = (new_text, ts)
            return idx
    return -1
