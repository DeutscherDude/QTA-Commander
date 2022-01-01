from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QStyle, QWidget
from PySide6.QtGui import QIcon
from Icons.IconHandler import Icons

class TitleBar(QWidget):
    def __init__(self):
        super().__init__()
        self.title = QLabel("QTA Commander", parent=self)
        self.title.setWindowIcon(QIcon("QTA_Icon.png"))

        self.minim_btn = QPushButton("_", parent=self)
        self.minim_btn.setIcon(QIcon(self.style().standardIcon(QStyle.SP_TitleBarMinButton)))
        self.maxim_btn = QPushButton("[]", parent=self)
        self.maxim_btn.setIcon(QIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton)))
        self.close_btn = QPushButton("X", parent=self)
        self.close_btn.setIcon(QIcon(self.style().standardIcon(QStyle.SP_TitleBarCloseButton)))
        self.layout = QHBoxLayout()
