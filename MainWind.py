from __future__ import annotations
import os
import pathlib
from MasterLayout import MasterLayout
from Shortcut_Handler import copy_file
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QWidget, QApplication, QListWidgetItem

from Tables import Tables

# TODO: Selecting, copying, deleting, moving multiple files
# TODO: PyDantic ogarnąć


class Window(QWidget):
    def __init__(self, layout: MasterLayout, *args):
        super().__init__()
        # Main window setup
        self.setWindowTitle("QT Commander")
        self.setGeometry(0, 0, 1240, 800)
        self.setLayout(layout)
        self.layout = layout
        self.show()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_F5:
            boy = QApplication.focusWidget()
            file_path = boy.currentItem().text()
            dir_path = boy.return_path().joinpath(file_path)
            des_path = Tables.ex_tab[Tables.l_index].return_path()
            copy_file(dir_path, des_path)
        elif event.key() == Qt.Key.Key_F6:
            print("F6 button has been pressed... suck my ding dong")
        elif event.key() == Qt.Key.Key_F7:
            print("F7 button has been pressed... suck my anus")
        elif event.key() == Qt.Key.Key_F8:
            print("F8 button has been pressed... kiss homies goodnight")
        elif event.key() == Qt.Key.Key_Backspace:
            current_table = QApplication.focusWidget()
            current_table.on_double_click(QListWidgetItem("..."))
        elif event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            current_table = QApplication.focusWidget()
            current_table.on_double_click(current_table.currentItem())
