from __future__ import annotations
import ctypes
import os
import pathlib
from dataclasses import dataclass
from enum import Enum, auto
from win32api import FindExecutable, GetLongPathName
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QKeyEvent
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QListWidgetItem, QListWidget, QWidget, QListView, \
    QAbstractItemView, QVBoxLayout


@dataclass(frozen=True)
class Icons:
    return_ = ":return"
    remo_st = ":rem_stor"
    drive = ":drive"
    trash = ":trash"
    file = ":file"
    directory = ":dir"


# TODO: Selecting, copying, deleting, moving multiple files
# TODO: OS stat - Podaje statystyki plików i folderów; os.path.isdir
# TODO: PyDantic ogarnąć

class Side(Enum):
    RIGHT = auto()
    LEFT = auto()


class Tables(QListWidget):
    last_index = 0
    # TODO: Referencing tables EXCLUDING the table you are currently working on
    def __init__(self, path: str, index: int):
        super().__init__()
        self.index = index
        self.paths = pathlib.Path(path)
        items = self.get_current_dir()
        for item in items:
            self.addItem(item)
        self.itemDoubleClicked.connect(self.on_double_click)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

    def get_current_dir(self, file_name="") -> list:
        Tables.last_index = self.index
        self.paths.joinpath(file_name)
        try:
            all_files = []
            # TODO: Fix entering certain directories like: Desktop
            all_files.append(QListWidgetItem(QIcon(Icons.return_), "..."))
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
        print(txt)
        if txt == "...":
            # TODO: Using root whilst hitting the end of the drive?
            self.clear()
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


class Listings(QVBoxLayout):
    def __init__(self, tables: list[Tables]):
        super().__init__()
        self.copy_butt = QPushButton("F5 Copy")
        self.move_butt = QPushButton("F6 Move")
        self.fldr_butt = QPushButton("F7 NewFolder")
        self.delete_butt = QPushButton("F8 Delete")


        tables[0].setResizeMode(QListView.ResizeMode(1))

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.copy_butt)
        buttons_layout.addWidget(self.move_butt)
        buttons_layout.addWidget(self.fldr_butt)
        buttons_layout.addWidget(self.delete_butt)
        topLayout = QHBoxLayout()
        for i in range(len(tables)):
            tables[i].assing_tables(tables)
            topLayout.addWidget(tables[i])
        self.addLayout(topLayout)
        self.addLayout(buttons_layout)

    def on_double_click_left(self, item: QListWidgetItem):
        # TODO: !!!If double clicked object is a file, proceed to open it ;)!!!
        txt = item.text()
        if txt == "...":
            # TODO: Using the Windows base icons I extracted :^) & maaaaybe introducing some of my own choosing
            # TODO: Using root whilst hitting the end of the drive?
            self.left_table.clear()
            items = self.get_current_dir_left()
        else:
            self.left_table.clear()
            items = self.get_current_dir_left(txt)
        for item in items:
            self.left_table.addItem(item)


class Window(QWidget):
    def __init__(self, tables: list[Tables]):
        super().__init__()
        # Main window setup
        self.setWindowTitle("QT Commander")
        self.setGeometry(0, 0, 1200, 800)
        self.lay = Listings(tables)

        self.setLayout(self.lay)
        self.show()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_F5:
            print("F5 button has been pressed... suck my toes")
        elif event.key() == Qt.Key.Key_F6:
            print("F6 button has been pressed... suck my ding dong")
        elif event.key() == Qt.Key.Key_F7:
            print("F7 button has been pressed... suck my anus")
        elif event.key() == Qt.Key.Key_F8:
            print("F8 button has been pressed... kiss homies goodnight")
        elif event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            bitch = self.lay.left_table.currentItem()
            self.lay.on_double_click(bitch)
        elif event.key() == Qt.Key.Key_Backspace:
            global PTH_L
            test = PTH_L.parent
            PTH_L = test
            self.lay.left_table.clear()
            items = self.lay.get_current_dir()
            for item in items:
                self.lay.left_table.addItem(item)

    def copy_file(file_path: str, dest_path) -> bool:
        try:
            file = open(file_path, 'rb').read()
            open(dest_path, 'wb').write()
            return True
        except:
            print("Argh, an error occurred")
            return False

    def delete_file(file_path) -> bool:
        try:
            os.remove(file_path)
            return True
        except:
            # Nie udało się usunąć pliku, brak dostępu
            # Except w Evencie?
            return False
