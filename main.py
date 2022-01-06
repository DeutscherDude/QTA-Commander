import sys
import os
import platform
from PySide6.QtCore import Qt
import Widgets.MainWind as MainWind
from PySide6.QtWidgets import QApplication, QTableWidgetItem
from Icons import icons
from Widgets.Custom_Widgets.tables import Tables, TablesFrame
# from Widgets.Custom_Widgets.tables_test import Tables
from Layout.MasterLayout import MasterLayout

# sqlalchemy
# TODO: Add capabilities for changing color scheme using QSS 
# TODO: Creating my own ListView using AbstractView(Widget?)
# TODO: Create a menu bar with settings

# TODO: Multiple items deletions, copying, moving
# TODO: Add logs
# Adn. requires the usage of "selectedItems()" and passing those as list. Changes in the code inc.

def main():
    system = platform.system()
    home = ''

    if system == "Windows":
        home = os.environ['USERPROFILE']
    elif system == "Linux":
        home = os.environ["HOME"]

    App = QApplication(sys.argv)
    inner_widgets = MainWind.CentralWidget()

    tables = [Tables(home, i) for i in range(2)]
    t_frame = TablesFrame(tables, home)
    layout = MasterLayout(tables, inner_widgets)
    inner_widgets.setUi(layout)

    main_win = MainWind.MainWind()
    main_win.setCentralWidget(inner_widgets)
    test = QTableWidgetItem()
    print(test.whatsThis())
    App.setStyleSheet(open('style/style.qss').read())
    sys.exit(App.exec())

if __name__ == "__main__":
    main()
