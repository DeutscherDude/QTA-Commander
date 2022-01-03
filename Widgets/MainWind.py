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
        QMainWindow.__init__(self, None, WindowFlag= Qt.FramelessWindowHint)
        self.setMouseTracking(True)

        self.margins = 5
        self.setContentsMargins(self.margins, self.margins, self.margins, self.margins)
        self.setGeometry(0, 0, 1240, 800)

        print(self.windowFlags())
        self.windowMoved.connect(self.movement)
        self.TimerStarted.connect(self.timerEvent)
        self.timer = QTimer()

        self.jp2 = None
        self.show()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.jp2 = event.globalPos() - self.pos()
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        return super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        maximizeWindow()
        return super().mouseDoubleClickEvent(event)

    # TODO: Fix the movement discrapencies
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        # self.TimerStarted.emit(self.timer)
        if event.buttons() == Qt.LeftButton:
            #Reducing fps?
            print(f"vektor: {self.jp2}, self.pos: {self.pos()}, event.pos: {event.pos()}")
            self.windowMoved.emit(self.mapToGlobal(event.pos() - self.jp2))
            sleep(0.01)
            event.accept()

    def movement(self, pos) -> None:
        if self.windowState() == Qt.WindowMaximized:
            self.setWindowState(Qt.WindowNoState)
            return None
        super(MainWind, self).move(pos)

    def timerEvent(self, event: QTimer) -> None:
        event.startTimer(50)
        print("Bitch")
        return super().timerEvent(event)


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
