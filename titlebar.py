from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QStyle, QWidget
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtCore import Qt, QSize
from Icons.IconHandler import Icons

class TitleBar(QWidget):
    def __init__(self, master: QWidget):
        super().__init__()
        self.setParent(master)
        self.setMouseTracking(True)
        self.mouseMoveEvent = self.moveWindow

        self.title_bar = QFrame(self)
        self.title_bar.setMaximumSize(QSize(16000, 50))
        self.title_bar.setFrameShape(QFrame.NoFrame)
        self.title_bar.setFrameShadow(QFrame.Raised)

        self.title = QLabel("QTA Commander", self.title_bar)
        self.title.setObjectName("app_title")
        self.title.setMaximumSize(QSize(16000,50))
        self.title.setFrameShape(QFrame.NoFrame)
        self.title.setFrameShadow(QFrame.Raised)

        self.btns_frame = QFrame(self.title_bar)
        self.btns_frame.setMaximumSize(QSize(100, 16000))
        self.btns_frame.setFrameShape(QFrame.StyledPanel)

        self.minim_btn = QPushButton("", self.btns_frame)
        self.minim_btn.setObjectName("blueButton")
        self.minim_btn.setMaximumSize(QSize(40, 40))
        self.minim_btn.setMinimumSize(QSize(20, 20))
        self.minim_btn.setIcon(QIcon(self.style().standardIcon(QStyle.SP_TitleBarMinButton)))

        self.maxim_btn = QPushButton("", self.btns_frame)
        self.maxim_btn.setObjectName("yellowButton")
        self.maxim_btn.setMaximumSize(QSize(40, 40))
        self.maxim_btn.setMinimumSize(QSize(20, 20))
        self.maxim_btn.setIcon(QIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton)))

        self.close_btn = QPushButton("", self.btns_frame)
        self.close_btn.setObjectName("evilButton")
        self.close_btn.setMaximumSize(QSize(40, 40))
        self.close_btn.setMinimumSize(QSize(20, 20))
        self.close_btn.setIcon(QIcon(self.style().standardIcon(QStyle.SP_TitleBarCloseButton)))

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.minim_btn)
        self.layout.addWidget(self.maxim_btn)
        self.layout.addWidget(self.close_btn)
        
    def moveWindow(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            print(f"Epstein did not kill himself\n {self.pos}")
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()
