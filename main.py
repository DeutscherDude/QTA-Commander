import sys
from PySide6.QtWidgets import *
from MainWind import Window

# sqlalchemy
# TODO: Add capabilities for changing color scheme using QSS

App = QApplication(sys.argv)
App.setStyleSheet(open('style.qss').read())
inner_widgets = Window()
sys.exit(App.exec())
