from __future__ import annotations
from MasterLayout import MasterLayout
from Shortcut_Handler import copy_file, delete_file, move_file, create_dir
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent, QIcon
from PySide6.QtWidgets import QWidget, QApplication, QListWidgetItem

# TODO: Selecting, copying, deleting, moving multiple files
# TODO: PyDantic ogarnąć


class Window(QWidget):
    def __init__(self, layout: MasterLayout, *args):
        super().__init__()
        # Main window setup
        self.setWindowTitle("QT Commander")
        self.setWindowIcon(QIcon("QTA_Icon.png"))
        self.setGeometry(0, 0, 1240, 800)
        self.setLayout(layout)
        self.layout = layout
        self.show()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_F5:
            copy_file()
        elif event.key() == Qt.Key.Key_F6:
            move_file()
        elif event.key() == Qt.Key.Key_F7:
            create_dir()
        elif event.key() == Qt.Key.Key_F8 or event.key() == Qt.Key.Key_Delete:
            delete_file()
        elif event.key() == Qt.Key.Key_Backspace:
            # TODO: Move the Enter & Return methods to Shortcut_Handler
            current_table = QApplication.focusWidget()
            current_table.on_double_click(QListWidgetItem("..."))
        elif event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            current_table = QApplication.focusWidget()
            current_table.on_double_click(current_table.currentItem())
