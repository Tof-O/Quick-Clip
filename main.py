import sys
from PySide6.QtWidgets import QApplication
from preview import PopupWindow
from text import HotkeyListener

if __name__ == "__main__":
    app = QApplication(sys.argv)
    listener = HotkeyListener()
    sys.exit(app.exec())