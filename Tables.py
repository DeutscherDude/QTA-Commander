from __future__ import annotations
import os
import pathlib
from PySide6.QtWidgets import QAbstractItemView, QListWidget, QListWidgetItem
from PySide6.QtGui import QIcon
import IconHandler
from DataFetcher import get_dir_widgets, get_available_drives


class Tables(QListWidget):
    last_index = 0
    curr_index = 1

    def __init__(self, path: str, index: int):
        super().__init__()
        self.index = index
        self.paths = pathlib.Path(path)
        items = get_dir_widgets(self.paths)
        for item in items:
            self.addItem(item)
        self.itemDoubleClicked.connect(self.on_double_click)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

    def on_double_click(self, item: QListWidgetItem):
        self.assign_indexes()
        print(f"{Tables.curr_index} {Tables.last_index}")
        txt = item.text()
        items = []
        if txt == "...":
            self.clear()
            if self.paths == self.paths.parent:
                drives = get_available_drives()
                for drive in drives:
                    items.append(QListWidgetItem(QIcon(IconHandler.Icons.drive), f"{drive}:\\"))
                self.paths = pathlib.Path("")
            else:
                self.paths = self.paths.parent
                items = get_dir_widgets(self.paths)
            for item in items:
                self.addItem(item)
        elif os.path.isfile(os.path.join(self.paths.as_posix(), txt)):
            os.startfile(self.paths.joinpath(txt))
        else:
            self.clear()
            self.paths = self.paths.joinpath(txt)
            items = get_dir_widgets(self.paths, txt)s
            for item in items:
                self.addItem(item)

    def assing_tables(self, tables: list[Tables]):
        self.tables = tables

    def assign_indexes(self) -> None:
        if Tables.curr_index != self.index:
            Tables.last_index = Tables.currentIndex
            Tables.currentIndex = self.index
