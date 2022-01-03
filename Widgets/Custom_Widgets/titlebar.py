from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QStyle, QWidget
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize, Qt
from Shortcut_Handler import maximizeWindow, closeApp, minimizeWindow

class TitleBar(QWidget):
    def __init__(self, master: QWidget):
        super().__init__()
        self._m_pos = None
        self.icon_size = 20

        self.setParent(master)

        self.title_bar = QFrame(self, WindowIcon= QIcon("QTA_Icon.png"), MaximumSize= QSize(16000, 50), 
                                FrameShape = QFrame.NoFrame, FrameShadow= QFrame.Raised)

        icon_pix = QPixmap("QTA_Icon.png")
        icon_pix = icon_pix.scaledToHeight(30, Qt.SmoothTransformation)
        self.icon_lab = QLabel(self.title_bar, Pixmap = icon_pix, MaximumSize = QSize(30, 30))

        self.title = QLabel("QTA Commander", self.title_bar, MaximumSize= QSize(16000, 50),
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
        self.layout.addWidget(self.icon_lab)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.minim_btn)
        self.layout.addWidget(self.maxim_btn)
        self.layout.addWidget(self.close_btn)
