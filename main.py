import sys
import os
from PySide6.QtWidgets import *
from DataFetcher import DataFetcher
import icons
from MainWind import Window
from Tables import Tables
from MasterLayout import MasterLayout

# sqlalchemy
# TODO: Add capabilities for changing color scheme using QSS
# TODO: Key press event handler? How to integrate with existing key-presses?
# TODO: Creating my own ListView using AbstractView(Widget?)

header = ['File Name', 'Date modified', 'Type', 'Size']

if __name__ == "__main__":
    home = os.environ['USERPROFILE']
    App = QApplication(sys.argv)
    # test = DataFetcher()
    # data = test.get_directories(home)
    tables = [Tables(home, i) for i in range(2)]
    App.setStyleSheet(open('style.qss').read())
    # test_model = Example(data, header)
    layout = MasterLayout(tables)
    inner_widgets = Window(layout)
    sys.exit(App.exec())
