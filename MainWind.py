from __future__ import annotations
from MasterLayout import MasterLayout
from Shortcut_Handler import copy_file, delete_file, move_file, create_dir, return_to_previous, enter_return
from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QKeyEvent, QMouseEvent, QIcon, QScreen
from PySide6.QtWidgets import QMainWindow, QWidget, QApplication, QListWidgetItem

# TODO: Selecting, copying, deleting, moving multiple files
# TODO: PyDantic ogarnąć


class MainWind(QMainWindow):

    windowMoved = Signal(QPoint)

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.setGeometry(0, 0, 1240, 800)

        self.windowMoved.connect(self.movement)
        
        # Positions and bools for handling the movement of the app
        self.m_pos = None
        self._pressed = False
        self.show()

        self.max_status = False

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.m_pos = event.pos()
        return super().mousePressEvent(event)

    # TODO: Fix the movement flickering
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.windowMoved.emit(self.mapToGlobal(event.pos() - self.m_pos))
        return super().mouseMoveEvent(event)

    def movement(self, pos) -> None:
        if self.windowState() == Qt.WindowMaximized or self.windowState == Qt.WindowFullScreen:
            self.setWindowState(Qt.WindowNoState)
            self.resize(1240, 800)
            return
        super(MainWind, self).move(pos)


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
