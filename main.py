import sys
import os
from PySide6.QtWidgets import *
import icons
from MainWind import Window
from Tables import Tables
from ItemsModel import ItemModel
from MasterLayout import MasterLayout

# sqlalchemy
# TODO: Add capabilities for changing color scheme using QSS


if __name__ == "__main__":
    home = os.environ['USERPROFILE']
    App = QApplication(sys.argv)
    tables = [Tables(home, i) for i in range(2)]
    App.setStyleSheet(open('style.qss').read())
    layout = MasterLayout(tables)
    test_model = ItemModel()
    inner_widgets = Window(layout=layout)
    sys.exit(App.exec())
