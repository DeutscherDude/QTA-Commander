import sys
import os
import platform
from Widgets.Custom_Widgets.bottomButtons import BottomButtons
from Widgets.Custom_Widgets.titlebar import TitleBar
from Widgets.Custom_Widgets.treeview import MyTreeWidget
import Widgets.MainWind as MainWind
from PySide6.QtWidgets import QApplication
from Icons import icons
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

    main_win = MainWind.MainWind()
    inner_widgets = MainWind.CentralWidget()

    title = TitleBar(main_win)

    buttons = BottomButtons(main_win)

    tree = MyTreeWidget()
    tree2 = MyTreeWidget()

    layout = MasterLayout(main_win)
    layout.add_frames_vertically(title)
    layout.add_frames_horizontally_multiple([tree2, tree])
    layout.add_frames_vertically(buttons)

    inner_widgets.setUi(layout)

    main_win.setCentralWidget(inner_widgets)
    App.setStyleSheet(open('style/style.qss').read())
    sys.exit(App.exec())

if __name__ == "__main__":
    main()
