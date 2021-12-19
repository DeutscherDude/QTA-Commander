from __future__ import annotations
import os
import pathlib
from PySide6.QtWidgets import QAbstractItemView, QListWidget, QListWidgetItem
from PySide6.QtGui import QIcon, QKeyEvent, Qt
from PySide6.QtCore import Signal, Slot
import IconHandler
from DataFetcher import get_directories


class Tables(QListWidget):
    last_index = 0
    current_index = 0

    pressed = Signal()

    # TODO: Referencing tables EXCLUDING the table you are currently working on
    def __init__(self, path: str, index: int):
        super().__init__()
        self.index = index
        self.paths = pathlib.Path(path)
        items = get_directories(self.paths)
        for item in items:
            self.addItem(item)
        self.itemDoubleClicked.connect(self.on_double_click)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

    def on_double_click(self, item: QListWidgetItem):
        txt = item.text()
        if txt == "...":
            # TODO: Using root whilst hitting the end of the drive?
            self.clear()
            if self.paths == self.paths.parent:
                items = [QListWidgetItem(QIcon(IconHandler.Icons.drive),"C:\\"),
                         QListWidgetItem(QIcon(IconHandler.Icons.drive), "D:\\",),
                         QListWidgetItem(QIcon(IconHandler.Icons.drive),"E:\\")]
                self.paths = pathlib.Path("")
            else:
                self.paths = self.paths.parent
                items = get_directories(self.paths)
            for item in items:
                self.addItem(item)
        elif os.path.isfile(os.path.join(self.paths.as_posix(), txt)):
            os.startfile(self.paths.joinpath(txt))
        else:
            self.clear()
            self.paths = self.paths.joinpath(txt)
            items = get_directories(self.paths, txt)
            for item in items:
                self.addItem(item)

    def assing_tables(self, tables: list[Tables]):
        self.tables = tables

    # def keyPressEvent(self, event:QKeyEvent) -> None:
    #     if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
    #         self.clear()
    #         items = self.get_current_dir()
    #         for item in items:
    #             self.addItem(item)

    # def enter_pressed(self):
    #     self.pressed.emit(self.currentItem())
    #
    # @Slot(QListWidgetItem)
    # def entering(self, item: QListWidgetItem):
    #     self.on_double_click(item)
