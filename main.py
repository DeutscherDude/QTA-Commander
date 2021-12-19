import sys
import os
from PySide6.QtWidgets import *
import icons
from MainWind import Window
from Tables import Tables
from MasterLayout import MasterLayout

# sqlalchemy
# TODO: Add capabilities for changing color scheme using QSS
# TODO: Creating my own ListView using AbstractView(Widget?)

header = ['File Name', 'Date modified', 'Type', 'Size']

if __name__ == "__main__":
    home = os.environ['USERPROFILE']
    App = QApplication(sys.argv)
    tables = [Tables(home, i) for i in range(2)]
    App.setStyleSheet(open('style.qss').read())
    layout = MasterLayout(tables)
    inner_widgets = Window(layout)
    sys.exit(App.exec())
