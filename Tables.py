from __future__ import annotations
import os
import pathlib
from PySide6.QtWidgets import QAbstractItemView, QListWidget, QListWidgetItem
from PySide6.QtGui import QIcon, QKeyEvent, Qt
from PySide6.QtCore import Signal, Slot
import IconHandler
from DataFetcher import DataFetcher
from IconHandler import Icons


class Tables(QListWidget):
    last_index = 0
    current_index = 0

    pressed = Signal()

    # TODO: Referencing tables EXCLUDING the table you are currently working on
    def __init__(self, path: str, index: int):
        super().__init__()
        self.index = index
        self.paths = pathlib.Path(path)
        paths = self.paths
        items = self.get_current_dir()
        for item in items:
            self.addItem(item)
        self.itemDoubleClicked.connect(self.on_double_click)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        # self.DataF = DataFetcher()

    def get_current_dir(self, file_name="") -> list:
        Tables.last_index = self.index
        self.paths.joinpath(file_name)
        try:
            all_files = [QListWidgetItem(QIcon(Icons.return_), "...")]
            for record in self.paths.iterdir():
                if record.is_dir():
                    i_rec = QIcon(Icons.directory)
                    n_rec = QListWidgetItem(i_rec, record.name)
                    all_files.append(n_rec)
                elif record.is_file():
                    i_rec = QIcon(Icons.file)
                    n_rec = QListWidgetItem(i_rec, record.name)
                    all_files.append(n_rec)
        except OSError as error:
            print(f"The following error occurred: {error}")
            # TODO: Display a pop up with information regarding to what went wrong to the user
        return all_files

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
                items = self.get_current_dir()
            for item in items:
                self.addItem(item)
        elif os.path.isfile(os.path.join(self.paths.as_posix(), txt)):
            os.startfile(self.paths.joinpath(txt))
        else:
            self.clear()
            self.paths = self.paths.joinpath(txt)
            items = self.get_current_dir(txt)
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
