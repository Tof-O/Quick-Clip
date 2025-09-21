# preview.py
# Quick-Clip Clipboard Popup App
#
# This file manages the main popup window UI, including previewing clipboard items,
# scrolling through history, launching the edit page, and handling theme toggling and border rendering.
#
# Author: Tof-O
# License: MIT

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGridLayout, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from edit import EditPage
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, load_theme, save_theme, THEME_COLORS, BUTTON_CONFIG
from text import create_tab_row

class PopupWindow(QMainWindow):
    def toggle_theme(self):
        """Toggle the theme between light and dark modes."""
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self.save_theme()
        self.apply_theme()
        if hasattr(self, 'border_widget'):
            self.border_widget.theme = self.theme
            self.border_widget.update()
    class BorderWidget(QWidget):
        def __init__(self, parent, theme):
            super().__init__(parent)
            self.theme = theme
            self.setAttribute(Qt.WA_TransparentForMouseEvents)
            self.setStyleSheet("background: transparent;")
        def paintEvent(self, event):
            """Custom paint event to draw the window border."""
            from PySide6.QtGui import QPainter, QPen, QColor
            painter = QPainter(self)
            pen = QPen()
            pen.setWidth(5)
            pen.setColor(QColor(0,0,0) if self.theme == "light" else QColor(255,255,255))
            painter.setPen(pen)
            rect = self.rect()
            rect.adjust(2, 2, -2, -2)
            painter.drawRoundedRect(rect, 12, 12)
    def show_edit_page(self):
        """Switch to edit mode and display the edit page."""
        self.edit_mode = True
        self._init_ui()
        self.apply_theme()
    def show_preview_from_edit(self):
        """Switch from edit mode to preview mode."""
        self.edit_mode = False
        self._init_ui()
        self.apply_theme()
    def save_edit(self):
        """Save the edited text and switch back to preview mode."""
        new_text = self.text_edit.toPlainText()
        for idx, item in enumerate(self.items):
            if item["text"] == self.preview_text:
                self.items[idx]["text"] = new_text
                self.preview_text = new_text
                break
        self.edit_mode = False
        self.show_preview(new_text)
    def _init_ui(self):
        """Initialize the user interface components."""
        central = QWidget()
        self.main_layout = QVBoxLayout(central)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        top_bar = QHBoxLayout()
        top_bar.setAlignment(Qt.AlignRight)
        theme_btn = QPushButton(BUTTON_CONFIG['theme']['text_light'] if self.theme == 'light' else BUTTON_CONFIG['theme']['text_dark'])
        theme_btn.setFixedSize(*BUTTON_CONFIG['theme']['size'])
        theme_btn.setStyleSheet("border:none;font-size:18px;")
        theme_btn.clicked.connect(self.toggle_theme)
        self.theme_btn = theme_btn
        close_btn = QPushButton(BUTTON_CONFIG['close']['text'])
        close_btn.setFixedSize(*BUTTON_CONFIG['close']['size'])
        close_btn.setStyleSheet("border:none;font-size:18px;")
        close_btn.clicked.connect(self.hide)
        top_bar.addWidget(theme_btn)
        top_bar.addWidget(close_btn)
        self.main_layout.addLayout(top_bar)
        self.tab_layout = QVBoxLayout()
        self.tab_layout.setAlignment(Qt.AlignTop)
        if getattr(self, 'edit_mode', False):
            def show_preview_callback(new_text):
                self.edit_mode = False
                self.show_preview(new_text)
            self.edit_page = EditPage(self.preview_text, self.items, self.preview_text, show_preview_callback, theme=self.theme)
            self.main_layout.addWidget(self.edit_page)
        elif self.preview_mode:
            preview_layout = QVBoxLayout()
            preview_layout.setContentsMargins(10, 10, 10, 10)
            top_bar = QGridLayout()
            back_btn = QPushButton(BUTTON_CONFIG['back']['text'])
            back_btn.setFixedSize(*BUTTON_CONFIG['back']['size'])
            back_btn.setStyleSheet("border:none;font-size:18px;")
            back_btn.clicked.connect(self.show_main_page)
            top_bar.addWidget(back_btn, 0, 0, alignment=Qt.AlignLeft)
            preview_label = QLabel("<b>Preview</b>")
            preview_label.setStyleSheet("font-size:18px;")
            top_bar.addWidget(preview_label, 0, 1, alignment=Qt.AlignHCenter)
            paste_btn = QPushButton(BUTTON_CONFIG['paste']['text'])
            paste_btn.setFixedSize(*BUTTON_CONFIG['paste']['size'])
            paste_btn.setStyleSheet("margin-left:12px;")
            paste_btn.clicked.connect(lambda checked, i=self.preview_text: self.paste_content(i))
            top_bar.addWidget(paste_btn, 0, 2, alignment=Qt.AlignRight)
            edit_btn = QPushButton(BUTTON_CONFIG['edit']['text'])
            edit_btn.setFixedSize(*BUTTON_CONFIG['edit']['size'])
            edit_btn.setStyleSheet("margin-right:8px;")
            edit_btn.clicked.connect(self.show_edit_page)
            top_bar.addWidget(edit_btn, 0, 3, alignment=Qt.AlignRight)
            top_bar.setColumnStretch(0, 1)
            top_bar.setColumnStretch(1, 2)
            top_bar.setColumnStretch(2, 1)
            preview_layout.addLayout(top_bar)
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            preview_content = QWidget()
            preview_content_layout = QVBoxLayout(preview_content)
            preview_content_layout.setContentsMargins(10, 10, 10, 10)
            preview_content_layout.setAlignment(Qt.AlignTop)
            # Show the actual text and timestamp
            preview_item = next((item for item in self.items if item["text"] == self.preview_text), None)
            if preview_item:
                preview_text_label = QLabel(preview_item["text"])
                preview_text_label.setWordWrap(True)
                preview_text_label.setAlignment(Qt.AlignTop)
                preview_text_label.setStyleSheet("padding: 10px;")
                preview_content_layout.addWidget(preview_text_label)
                ts_label = QLabel(f"<i>{preview_item['ts']}</i>")
                ts_label.setStyleSheet("padding-left:10px; color: #888;")
                preview_content_layout.addWidget(ts_label)
            else:
                preview_text_label = QLabel(self.preview_text)
                preview_text_label.setWordWrap(True)
                preview_text_label.setAlignment(Qt.AlignTop)
                preview_text_label.setStyleSheet("padding: 10px;")
                preview_content_layout.addWidget(preview_text_label)
            scroll.setWidget(preview_content)
            preview_layout.addWidget(scroll)
            self.main_layout.addLayout(preview_layout)
        else:
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            tab_content = QWidget()
            tab_content_layout = QVBoxLayout(tab_content)
            tab_content_layout.setAlignment(Qt.AlignTop)
            for idx, item in enumerate(self.items):
                tab_widget = create_tab_row(
                    item["text"], item["ts"],
                    on_preview=self.show_preview,
                    on_paste=self.paste_content
                )
                tab_content_layout.addWidget(tab_widget)
            scroll.setWidget(tab_content)
            self.main_layout.addWidget(scroll)
        self.setCentralWidget(central)
        self.border_widget = self.BorderWidget(self, self.theme)
        self.border_widget.setGeometry(0, 0, self.width(), self.height())
        self.border_widget.raise_()
        self.border_widget.show()
    def resizeEvent(self, event):
        """Handle the window resize event."""
        super().resizeEvent(event)
        if hasattr(self, 'border_widget'):
            self.border_widget.setGeometry(0, 0, self.width(), self.height())
    def showEvent(self, event):
        """Handle the window show event."""
        super().showEvent(event)
        if hasattr(self, 'border_widget'):
            self.border_widget.setGeometry(0, 0, self.width(), self.height())
            self.border_widget.raise_()
    def apply_theme(self):
        """Apply the current theme to the UI components."""
        colors = THEME_COLORS[self.theme]
        self.setStyleSheet(f"""
            QMainWindow {{ background: {colors['bg']}; border-radius: 12px; border: 5px solid {colors['border']} !important; }}
            QWidget {{ background: {colors['bg']}; border-radius: 12px; border: none !important; }}
            QLabel {{ color: {colors['label']}; }}
            QPushButton {{ background: {colors['btn_bg']}; color: {colors['btn_fg']}; border-radius: 8px; }}
            QPushButton:hover {{ background: {colors['btn_hover']}; }}
        """)
        if hasattr(self, 'theme_btn') and self.theme_btn is not None:
            try:
                self.theme_btn.setText("☀️" if self.theme == "dark" else "🌙")
            except RuntimeError:
                pass
        if getattr(self, 'edit_mode', False) and hasattr(self, 'edit_page'):
            self.edit_page.set_theme(self.theme)
    def __init__(self, items, theme=None):
        """Initialize the PopupWindow with clipboard items and an optional theme."""
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.theme = load_theme() if theme is None else theme
        self.items = items
        self.preview_mode = False
        self.preview_text = ""
        self._init_ui()
        self.apply_theme()
    def load_theme(self):
        """Load the theme from settings."""
        return load_theme()
    def save_theme(self):
        """Save the current theme to settings."""
        save_theme(self.theme)
    def show_main_page(self):
        """Show the main page with clipboard history."""
        self.preview_mode = False
        self._init_ui()
        self.apply_theme()
    def paste_content(self, text):
        """Paste the given text to the clipboard and simulate a paste action."""
        from PySide6.QtGui import QGuiApplication
        clipboard = QGuiApplication.instance().clipboard()
        clipboard.setText(text)
        self.hide()
        from PySide6.QtCore import QTimer
        def do_paste():
            try:
                import win32gui, win32con, win32api, time
                hwnd = win32gui.GetForegroundWindow()
                win32gui.SetForegroundWindow(hwnd)
                for vk in [win32con.VK_MENU, win32con.VK_SHIFT]:
                    win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
                win32api.keybd_event(0x56, 0, 0, 0)
                win32api.keybd_event(0x56, 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
            except Exception as e:
                print(f"Paste failed: {e}")
        QTimer.singleShot(200, do_paste)
    def show_preview(self, text):
        """Show the preview of the given text."""
        self.preview_mode = True
        self.preview_text = text
        self._init_ui()
        self.apply_theme()
        if hasattr(self, 'border_widget'):
            self.border_widget.theme = self.theme
            self.border_widget.update()
    def show_at_cursor(self):
        """Show the popup window at the current cursor position."""
        pos = QCursor.pos()
        self.move(pos.x(), pos.y())
        self.show()
        self.preview_mode = False
        self._init_ui()
        self.apply_theme()
