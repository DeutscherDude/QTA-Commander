import sys
import os

from PySide6.QtCore import Qt
import Widgets.MainWind as MainWind
from PySide6.QtWidgets import QApplication
from Icons import icons
from Widgets.Custom_Widgets.tables import Tables
from Layout.MasterLayout import MasterLayout

# sqlalchemy
# TODO: Add capabilities for changing color scheme using QSS 
# TODO: Creating my own ListView using AbstractView(Widget?)
# TODO: Create a menu bar with settings


# TODO: Multiple items deletions, copying, moving
# Adn. requires the usage of "selectedItems()" and passing those as list. Changes in the code inc.

# TODO: MAJOR BUG - Copying folders is not possible. Needs urgent fixing

def main():
    home = os.environ['USERPROFILE']
    App = QApplication(sys.argv)
    inner_widgets = MainWind.CentralWidget()
    
    tables = [Tables(home, i) for i in range(2)]
    layout = MasterLayout(tables, inner_widgets)
    inner_widgets.setUi(layout)

    main_win = MainWind.MainWind()
    main_win.setCentralWidget(inner_widgets)

    App.setStyleSheet(open('style/style.qss').read())
    sys.exit(App.exec())

if __name__ == "__main__":
    main()
