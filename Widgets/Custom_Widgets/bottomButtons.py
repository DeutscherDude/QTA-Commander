from PySide6.QtWidgets import (QWidget, QPushButton, 
                            QHBoxLayout, QFrame)
import Shortcut_Handler


class BottomButtons(QFrame):
    def __init__(self, master: QWidget) -> None:
        super().__init__()
        self.setParent(master)
        self.copy_butt = QPushButton("F5 Copy")
        self.copy_butt.clicked.connect(Shortcut_Handler.copy_file)
        self.move_butt = QPushButton("F6 Move")
        self.move_butt.clicked.connect(Shortcut_Handler.move_file)
        self.fldr_butt = QPushButton("F7 NewFolder")
        self.fldr_butt.clicked.connect(Shortcut_Handler.create_dir)
        self.delete_butt = QPushButton("F8 Delete")
        self.delete_butt.clicked.connect(Shortcut_Handler.delete_file)
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.copy_butt)
        self.layout.addWidget(self.move_butt)
        self.layout.addWidget(self.fldr_butt)
        self.layout.addWidget(self.delete_butt)
