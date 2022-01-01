import sys
import os
from PySide6.QtWidgets import QApplication
from Icons import icons
from MainWind import Window
from tables import Tables
from MasterLayout import MasterLayout

# sqlalchemy
# TODO: Add capabilities for changing color scheme using QSS
# TODO: Creating my own ListView using AbstractView(Widget?)
# TODO: Create a menu bar with settings

def main():
    home = os.environ['USERPROFILE']
    App = QApplication(sys.argv)
    inner_widgets = Window()
    tables = [Tables(home, i) for i in range(2)]
    App.setStyleSheet(open('style/style.qss').read())
    layout = MasterLayout(tables)
    inner_widgets.setUi(layout)
    sys.exit(App.exec())


if __name__ == "__main__":
    main()
