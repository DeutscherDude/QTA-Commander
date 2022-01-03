from __future__ import annotations
from Layout.MasterLayout import MasterLayout
from Shortcut_Handler import copy_file, delete_file, move_file, create_dir, return_to_previous, enter_return, maximizeWindow
from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QCursor, QKeyEvent, QMouseEvent, QIcon, QScreen
from PySide6.QtWidgets import QMainWindow, QWidget, QApplication, QListWidgetItem

# TODO: Selecting, copying, deleting, moving multiple files
# TODO: PyDantic ogarnąć


class MainWind(QMainWindow):

    windowMoved = Signal(QPoint)

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.margins = 5
        self.setContentsMargins(self.margins, self.margins, self.margins, self.margins)
        self.setGeometry(0, 0, 1600, 800)

        self.windowMoved.connect(self.movement)
        
        # Positions and bools for handling the movement of the app
        self.click_pos = None
        self.show()

        self.max_status = False

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.click_pos = event.pos()
        return super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        maximizeWindow()
        return super().mouseDoubleClickEvent(event)

    # TODO: Fix the movement flickering
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            click_dif = QPoint((event.pos().x() - self.click_pos.x()), (event.pos().y() - self.click_pos.y()))
            self.windowMoved.emit(self.mapToGlobal((self.pos() + click_dif)))
            self.click_pos = event.globalPos()
            event.accept()
        else:
            self.showNormal()

    def movement(self, pos) -> None:
        # print(pos)
        if self.windowState() == Qt.WindowMaximized or self.windowState == Qt.WindowFullScreen:
            self.setWindowState(Qt.WindowNoState)
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
