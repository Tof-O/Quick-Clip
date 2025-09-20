# main.py
# Quick-Clip Clipboard Popup App
#
# Entry point for the application. Initializes the Qt application and starts the hotkey listener.
#
# Author: Tof-O
# License: MIT

import sys
from PySide6.QtWidgets import QApplication
from preview import PopupWindow
from text import HotkeyListener

if __name__ == "__main__":
    app = QApplication(sys.argv)
    listener = HotkeyListener()
    sys.exit(app.exec())