from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                            QListView, QHBoxLayout, QStyle,
                            QLabel, QFrame)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from tables import Tables
import os
import Shortcut_Handler
from titlebar import TitleBar


class MasterLayout(QVBoxLayout):
    def __init__(self, tables: list[Tables], *args):
        super().__init__()

        # Title bar setup
        title_bar = QFrame()
        title_bar.setMaximumSize(QSize(160000, 50))
        title_bar.setFrameShape(QFrame.NoFrame)
        title_bar.setFrameShadow(QFrame.Raised)


        title = QLabel("QTA Commander")
        title.setMaximumSize(QSize(16000,50))
        title.setFrameShape(QFrame.NoFrame)
        title.setFrameShadow(QFrame.Raised)
        title.setWindowIcon(QIcon("QTA_Icon.png"))

        # Frame for command buttons layout
        btns_frame = QFrame(title)
        btns_frame.setMaximumSize(QSize(100, 16000))
        btns_frame.setFrameShape(QFrame.StyledPanel)

        minim_btn = QPushButton("_", btns_frame)
        minim_btn.setMaximumSize(QSize(50, 50))
        minim_btn.setMinimumSize(QSize(20, 20))
        # minim_btn.setIcon(QIcon((QStyle.SP_TitleBarMinButton)))
        maxim_btn = QPushButton("[]", btns_frame)
        maxim_btn.setMaximumSize(QSize(50, 50))
        maxim_btn.setMinimumSize(QSize(20, 20))
        # maxim_btn.setIcon(QIcon((QStyle.SP_TitleBarMaxButton)))
        close_btn = QPushButton("X", btns_frame)
        close_btn.setMaximumSize(QSize(50, 50))
        close_btn.setMinimumSize(QSize(20, 20))

        # close_btn.setIcon(QIcon(QStyle.SP_TitleBarCloseButton))

        # TODO: Create a separate class where those buttons are created :^)
        self.copy_butt = QPushButton("F5 Copy")
        self.copy_butt.clicked.connect(Shortcut_Handler.copy_file)
        self.move_butt = QPushButton("F6 Move")
        self.move_butt.clicked.connect(Shortcut_Handler.move_file)
        self.fldr_butt = QPushButton("F7 NewFolder")
        self.fldr_butt.clicked.connect(Shortcut_Handler.create_dir)
        self.delete_butt = QPushButton("F8 Delete")
        self.delete_butt.clicked.connect(Shortcut_Handler.delete_file)

        tables[0].setResizeMode(QListView.ResizeMode(1))

        # Buttons layout setup
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.copy_butt)
        buttons_layout.addWidget(self.move_butt)
        buttons_layout.addWidget(self.fldr_butt)
        buttons_layout.addWidget(self.delete_butt)

        # Titlebar layout setup
        titlebar_layout = QHBoxLayout()
        titlebar_layout.addWidget(title, 0, Qt.AlignLeft)
        titlebar_layout.addWidget(minim_btn, 0, Qt.AlignRight)
        titlebar_layout.addWidget(maxim_btn, 0, Qt.AlignRight)
        titlebar_layout.addWidget(close_btn, 0, Qt.AlignRight)
        titlebar_layout.setSpacing(0)
        titlebar_layout.setContentsMargins(0, 0, 0, 0)

        listsLayout = QHBoxLayout()
        for i in range(len(tables)):
            tables[i].assing_tables(tables)
            listsLayout.addWidget(tables[i])

        if args is not None:
            for i in range(len(args)):
                test = args[i]
                listsLayout.addWidget(test)

        test1 = QHBoxLayout()
        test1.addWidget(TitleBar())

        self.addLayout(test1)
        self.addLayout(titlebar_layout)
        self.addLayout(listsLayout)
        self.addLayout(buttons_layout)

    def add_custom_layout(self, *args, **kwargs):
        layout = QVBoxLayout()
        layout.addWidget(args)
        self.addLayout(layout)


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
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.minim_btn)
        self.layout.addWidget(self.maxim_btn)
        self.layout.addWidget(self.close_btn)
        