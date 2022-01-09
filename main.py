import sys
import os
import platform
from Widgets.Custom_Widgets.bottomButtons import BottomButtons
from Widgets.Custom_Widgets.titlebar import TitleBar
from Widgets.Custom_Widgets.treeview import MyTreeWidget
import Widgets.MainWind as MainWind
from PySide6.QtWidgets import QApplication, QToolBar
from Icons import icons
from Layout.MasterLayout import MasterLayout

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
    buttons = BottomButtons(main_win)

    tree = MyTreeWidget()
    tree2 = MyTreeWidget()

    layout = MasterLayout(main_win)
    layout.add_frames_horizontally(QToolBar(main_win))
    layout.add_frames_horizontally_multiple([tree2, tree])
    layout.add_frames_vertically(buttons)

    inner_widgets.setUi(layout)
    main_win.setCentralWidget(inner_widgets)
    App.setStyleSheet(open('style/style.qss').read())
    sys.exit(App.exec())

if __name__ == "__main__":
    main()
