from __future__ import annotations
import os
import pathlib
import IconHandler
from PySide6.QtWidgets import QAbstractItemView, QListWidget, QListWidgetItem
from PySide6.QtGui import QIcon
from DataFetcher import get_dir_widgets, get_available_drives


class Tables(QListWidget):
    l_index = 0
    c_index = 0
    ex_tab = []

    def __init__(self, path: str, index: int):
        super().__init__()
        self.index = index
        self.paths = pathlib.Path(path)
        items = get_dir_widgets(self.paths)
        for item in items:
            self.addItem(item)
        self.itemDoubleClicked.connect(self.on_double_click)
        self.itemClicked.connect(self._assign_indexes)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        Tables.ex_tab.append(self)

    def on_double_click(self, item: QListWidgetItem):
        Tables._assign_indexes(self)
        txt = item.text()
        print(f"C_ind: {Tables.c_index}, L_ind: {Tables.l_index}")
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
        print(f"L_ind: {Tables.l_index}, C_ind: {Tables.c_index}")
