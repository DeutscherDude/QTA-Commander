from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QStyle, QWidget
from PySide6.QtGui import QFont, QIcon, QMouseEvent, Qt
from PySide6.QtCore import QPoint, QSize, Signal
from Shortcut_Handler import maximizeWindow, closeApp, minimizeWindow

class TitleBar(QWidget):
    def __init__(self, master: QWidget):
        super().__init__()
        self._m_pos = None
        self.icon_size = 20

        self.setParent(master)

        self.title_bar = QFrame(self)
        self.title_bar.setMaximumSize(QSize(16000, 50))
        self.title_bar.setFrameShape(QFrame.NoFrame)
        self.title_bar.setFrameShadow(QFrame.Raised)

        self.title = QLabel("Twuj stary wchodzi Ci do wanny", self.title_bar, MaximumSize= QSize(16000, 50),
                            ObjectName= "app_title", FrameShape= QFrame.NoFrame, FrameShadow= QFrame.Raised)

        self.btns_frame = QFrame(self.title_bar, MaximumSize= QSize(100, 16000), FrameShape= QFrame.StyledPanel)

        self.minim_btn = QPushButton("", self.btns_frame,objectName= "minim_button", clicked= minimizeWindow,
                                    MaximumSize= QSize(40, 40), MinimumSize= QSize(20, 20),
                                    Icon = self.style().standardIcon(QStyle.SP_TitleBarMinButton))

        self.maxim_btn = QPushButton("", self.btns_frame, clicked= maximizeWindow, objectName= "maxim_button", 
                                    MaximumSize= QSize(40, 40), MinimumSize= QSize(20, 20), 
                                    Icon= self.style().standardIcon(QStyle.SP_TitleBarMaxButton))

        self.close_btn = QPushButton("", self.btns_frame, clicked= closeApp, objectName= "close_button", 
                                    MaximumSize= QSize(40, 40), MinimumSize= QSize(20, 20), 
                                    Icon= self.style().standardIcon(QStyle.SP_TitleBarCloseButton))

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.minim_btn)
        self.layout.addWidget(self.maxim_btn)
        self.layout.addWidget(self.close_btn)
