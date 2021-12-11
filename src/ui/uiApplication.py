import sys

from PyQt5.QtWidgets import QApplication
from src.ui.uiMainWindow import UiMainWindow


class UiApplication:
    def __init__(self):
        # ui settings
        app = QApplication(sys.argv)
        win = UiMainWindow()

        # display
        win.show()
        sys.exit(app.exec_())
