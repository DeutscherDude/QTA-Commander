from __future__ import annotations
from MasterLayout import MasterLayout
from Shortcut_Handler import copy_file, delete_file, move_file, create_dir, return_to_previous, enter_return
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent, QMouseEvent, QIcon, QScreen
from PySide6.QtWidgets import QMainWindow, QWidget, QApplication, QListWidgetItem

# TODO: Selecting, copying, deleting, moving multiple files
# TODO: PyDantic ogarnąć


class MainWind(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setGeometry(0, 0, 1240, 800)

        # Bool for handling the maximize status of the app 
        self.max_status = False

        scr_size = QScreen.availableGeometry(QApplication.primaryScreen())
        x_pos = (scr_size.width() - self.width())/2
        y_pos = (scr_size.height() - self.height())/2

        self.move(x_pos, y_pos)
        self.show()

class CentralWidget(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.m_pos = None
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

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            pos = event.pos()
            x_pos, y_pos = pos.x(), pos.y()
            cen_x, cen_y = self.width(), self.height()
            self.m_pos = event.pos()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.m_pos = event.pos()
        return super().mouseMoveEvent(event)

    def move(self, pos) -> None:
        if self.windowState() == Qt.WindowMaximized or self.windowState == Qt.WindowFullScreen:
            return
        super(QApplication.activeWindow, self).move(pos)