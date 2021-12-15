import sys
import os
from PySide6.QtWidgets import *
import icons
from MainWind import Window
from pathlib import Path
from MainWind import Tables

# sqlalchemy
# TODO: Add capabilities for changing color scheme using QSS


if __name__ == "__main__":
    home = os.environ['USERPROFILE']
    App = QApplication(sys.argv)
    tables = [Tables(home, i) for i in range(2)]
    App.setStyleSheet(open('style.qss').read())
    inner_widgets = Window(tables)
    sys.exit(App.exec())
