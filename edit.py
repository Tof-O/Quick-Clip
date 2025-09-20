from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit
from PySide6.QtCore import Qt
from text import update_clipboard_item

class EditPage(QWidget):
    def __init__(self, original_text, items, preview_text, on_show_preview, theme='light'):
        super().__init__()
        self.original_text = original_text
        self.items = items
        self.preview_text = preview_text
        self.on_show_preview = on_show_preview
        self.theme = theme
        self._init_ui()
        self.apply_theme()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        # Top bar: back arrow left, label center, save right
        top_bar = QHBoxLayout()
        back_btn = QPushButton("←")
        back_btn.setFixedSize(32, 32)
        back_btn.setStyleSheet("border:none;font-size:18px;")
        back_btn.clicked.connect(self._on_back)
        top_bar.addWidget(back_btn, alignment=Qt.AlignLeft)
        self.label = QLabel("<b>Edit Copy</b>")
        self.label.setStyleSheet("font-size:18px;")
        top_bar.addWidget(self.label, alignment=Qt.AlignHCenter)
        save_btn = QPushButton("💾 Save")
        save_btn.setFixedSize(70, 32)
        save_btn.clicked.connect(self._save_edit)
        top_bar.addWidget(save_btn, alignment=Qt.AlignRight)
        layout.addLayout(top_bar)
        self.text_edit = QTextEdit()
        self.text_edit.setText(self.original_text)
        self.text_edit.setStyleSheet("padding: 10px;")
        layout.addWidget(self.text_edit)
        # Cancel button at the bottom, slightly above border
        cancel_row = QHBoxLayout()
        cancel_row.addStretch(1)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedSize(80, 32)
        cancel_btn.clicked.connect(self._on_cancel)
        cancel_btn.setStyleSheet("margin-bottom:16px;")
        cancel_row.addWidget(cancel_btn, alignment=Qt.AlignRight)
        layout.addLayout(cancel_row)

    def _save_edit(self):
        new_text = self.text_edit.toPlainText()
        update_clipboard_item(self.items, self.preview_text, new_text)
        self.preview_text = new_text
        self.on_show_preview(new_text)

    def _on_cancel(self):
        self.on_show_preview(self.preview_text)

    def _on_back(self):
        self.on_show_preview(self.preview_text)

    def apply_theme(self):
        # Dynamic colors for dark/light theme
        bg_color = "#232629" if self.theme == "dark" else "#fff"
        text_color = "#f0f0f0" if self.theme == "dark" else "#222"
        self.text_edit.setStyleSheet(f"background: {bg_color}; color: {text_color}; padding: 10px;")
        self.label.setStyleSheet(f"font-size:18px; color: {text_color};")

    def set_theme(self, theme):
        self.theme = theme
        self.apply_theme()
