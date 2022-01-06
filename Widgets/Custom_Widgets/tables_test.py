from __future__ import annotations
import os
import pathlib

from PySide6.QtCore import Qt
import Icons.IconHandler as IconHandler
from PySide6.QtWidgets import QAbstractItemView, QFrame, QHBoxLayout, QListWidget, QListWidgetItem, QScrollBar, QWidget
from PySide6.QtGui import QIcon
from DataFetcher import get_dir_widgets, get_available_drives, get_directories_tuples

class Tables(QFrame):
    l_index = 1
    c_index = 0
    ex_tab = []

    def __init__(self, path: str, index: int):
        super().__init__()

        self.setObjectName(u'bitch')

        self.index = index
        self.paths = pathlib.Path(path)
        items = get_dir_widgets(self.paths)
        self.items_list = QListWidget(self)

        v_scroll_bar = QScrollBar(Qt.Vertical)
        h_scroll_bar = QScrollBar(Qt.Horizontal, self)
        self.items_list.setVerticalScrollBar(v_scroll_bar)

        for item in items:
            self.items_list.addItem(item)

        self.items_list.itemDoubleClicked.connect(self.on_double_click)
        self.items_list.itemClicked.connect(self._assign_indexes)
        self.items_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        Tables.ex_tab.append(self)

        self.time_view_list = QListWidget(self)
        self.time_view_list.setObjectName(u'times')
        self.time_view_list.setVerticalScrollBar(v_scroll_bar)
        
        self.items_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.time_view_list.setHorizontalScrollBar(h_scroll_bar)

        self.items_list.setHorizontalScrollBar(h_scroll_bar)

        items = get_directories_tuples(path)
        self.time_view_list.addItem('')
        for item in items:
            self.time_view_list.addItem(QListWidgetItem(QIcon("clock.png"),item[1]))

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.items_list)
        self.layout.addWidget(self.time_view_list)


    def on_double_click(self, item: QListWidgetItem):
        Tables._assign_indexes(self)
        txt = item.text()
        items = []
        if txt == "...":
            self.clear()
            if self.paths == self.paths.parent and self.paths != pathlib.Path("\\"):
                drives = get_available_drives()
                for drive in drives:
                    items.append(QListWidgetItem(QIcon(IconHandler.Icons.drive), f"{drive}:\\"))
                self.paths = pathlib.Path(self.paths.root)
            else:
                self.paths = self.paths.parent
                items = get_dir_widgets(self.paths)
            for item in items:
                self.addItem(item)
        elif os.path.isfile(os.path.join(self.paths.as_posix(), txt)):
            os.startfile(self.paths.joinpath(txt))
        else:
            self.clear()
            items = get_dir_widgets(self.paths, txt)
            self.paths = self.paths.joinpath(txt)
            for item in items:
                self.addItem(item)

    def assing_tables(self, tables: list[Tables]):
        self.tables = tables

    def return_path(self):
        return self.paths

    def _assign_indexes(self) -> None:
        if self.index != Tables.c_index:
            Tables.l_index = Tables.c_index
            Tables.c_index = self.index
