from __future__ import annotations
from time import sleep
from Layout.MasterLayout import MasterLayout
from Shortcut_Handler import copy_file, delete_file, move_file, create_dir, return_to_previous, enter_return, maximizeWindow
from PySide6.QtCore import QPoint, QTimer, QTimerEvent, Qt, Signal
from PySide6.QtGui import QKeyEvent, QMouseEvent
from PySide6.QtWidgets import QMainWindow, QWidget

# TODO: Selecting, copying, deleting, moving multiple files
# TODO: PyDantic ogarnąć

class MainWind(QMainWindow):

    windowMoved = Signal(QPoint)
    TimerStarted = Signal(QTimer)

    def __init__(self):
        QMainWindow.__init__(self, None, objectName= "main_window")
        self.setMouseTracking(True)

        self.margins = 5
        self.setContentsMargins(self.margins, self.margins, self.margins, self.margins)
        self.setGeometry(0, 0, 1240, 800)

        self.show()

class CentralWidget(QWidget):
    def __init__(self, *args):
        super().__init__()
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
            return_to_previous()
        elif event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            enter_return()

    def setUi(self, layout: MasterLayout):
        self.setLayout(layout)
        self.layout = layout
