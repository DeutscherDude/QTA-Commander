from PySide6.QtCore import QSize
from PySide6.QtWidgets import (QWidget, QPushButton, 
                            QHBoxLayout, QFrame)
import Shortcut_Handler


class BottomButtons(QFrame):
    def __init__(self, master: QWidget) -> None:
        super().__init__()
        self.setParent(master)
        self.copy_butt = QPushButton("F5 Copy", clicked= Shortcut_Handler.copy_file_tree, MinimumSize= QSize(120, 40))
        self.move_butt = QPushButton("F6 Move", clicked= Shortcut_Handler.move_file_tree, MinimumSize= QSize(120, 40))
        self.fldr_butt = QPushButton("F7 NewFolder", clicked= Shortcut_Handler.create_dir_tree, MinimumSize= QSize(120, 40))
        self.delete_butt = QPushButton("F8 Delete", clicked= Shortcut_Handler.delete_file_tree, MinimumSize= QSize(120, 40))

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.copy_butt)
        self.layout.addWidget(self.move_butt)
        self.layout.addWidget(self.fldr_butt)
        self.layout.addWidget(self.delete_butt)
        self.layout.setContentsMargins(0, 0, 0, 0)
