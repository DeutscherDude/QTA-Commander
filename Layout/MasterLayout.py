from PySide6.QtWidgets import (QWidget, QVBoxLayout,
                            QListView, QHBoxLayout)
from typing import List
from Widgets.Custom_Widgets.tables import Tables
from Widgets.Custom_Widgets.titlebar import TitleBar
from Widgets.Custom_Widgets.bottomButtons import BottomButtons
from enum import Enum, auto


class MasterLayout(QVBoxLayout):
    def __init__(self, master: QWidget, *args):
        super().__init__()

        if args is not None:
            for i in range(len(args)):
                test = args[i]
                self.addWidget(test)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(BottomButtons(master))

        self.setContentsMargins(0, 0, 0, 0)
   
    def add_frames_vertically(self, widget: QWidget):
        layout = QVBoxLayout()
        layout.addWidget(widget)
        self.addLayout(layout)

    def add_frames_vertically_multiple(self, widgets: List[QWidget]):
        layout = QVBoxLayout()
        for widget in widgets:
            layout.addWidget(widget)
        self.addLayout(layout)

    def add_frames_horizontally(self, widget: QWidget):
        layout = QHBoxLayout()
        layout.addWidget(widget)
        self.addLayout(layout)

    def add_frames_horizontally_multiple(self, widgets: List[QWidget]):
        layout = QHBoxLayout()
        for widget in widgets:
            layout.addWidget(widget)
        self.addLayout(layout)