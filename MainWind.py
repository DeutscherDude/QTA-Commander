import ctypes
import os
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QKeyEvent
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QListWidgetItem, QListWidget, QWidget, QListView, \
    QAbstractItemView, QVBoxLayout

HOME = os.environ['USERPROFILE']
PTH_L = Path(HOME)
PTH_R = Path(HOME)


# TODO: Selecting, copying, deleting, moving multiple files
# TODO: OS stat - Podaje statystyki plików i folderów; os.path.isdir
# TODO: ?My own instances of QListWidget & QListWidgetItem to include names of variables????????


class Listings(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.left_table = QListWidget()
        self.copy_butt = QPushButton("F5 Copy")
        self.move_butt = QPushButton("F6 Move")
        self.fldr_butt = QPushButton("F7 NewFolder")
        self.delete_butt = QPushButton("F8 Delete")
        items = self.get_current_dir_left()
        self.left_table.setResizeMode(QListView.ResizeMode(1))
        self.right_table = QListWidget()

        for item in items:
            self.left_table.addItem(item)

        items = self.get_current_dir_right()

        for item in items:
            self.right_table.addItem(item)

        self.left_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.right_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.left_table.itemDoubleClicked.connect(self.on_double_click_left)
        self.right_table.itemDoubleClicked.connect(self.on_double_click_right)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.copy_butt)
        buttons_layout.addWidget(self.move_butt)
        buttons_layout.addWidget(self.fldr_butt)
        buttons_layout.addWidget(self.delete_butt)
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.left_table)
        topLayout.addWidget(self.right_table)
        self.addLayout(topLayout)
        self.addLayout(buttons_layout)

    def on_double_click_left(self, item: QListWidgetItem):
        # TODO: If double clicked object is a file, proceed to open it ;)
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

    def on_double_click_right(self, item: QListWidgetItem):
        txt = item.text()
        if txt == "...":
            # TODO: Using the Windows base icons I extracted :^) & maaaaybe introducing some of my own choosing
            # TODO: Using root whilst hitting the end of the drive?
            self.right_table.clear()
            items = self.get_current_dir_right()
        else:
            self.right_table.clear()
            items = self.get_current_dir_right(txt)
        for item in items:
            self.right_table.addItem(item)

    def get_current_dir_left(self, file_name="") -> list:
        global PTH_L
        PTH_L = PTH_L.joinpath(file_name)
        if file_name == "":
            PTH_L = PTH_L.parent
        try:
            all_files = []
            # TODO: Fix entering certain directories like: Desktop
            all_files.append(QListWidgetItem(QIcon("Arrow_48x48"), "..."))
            for record in PTH_L.iterdir():
                if record.is_dir():
                    i_rec = QIcon("folder.png")
                    n_rec = QListWidgetItem(i_rec, record.name)
                    all_files.append(n_rec)
                elif record.is_file():
                    i_rec = QIcon("file.png")
                    n_rec = QListWidgetItem(i_rec, record.name)
                    all_files.append(n_rec)
        except OSError as error:
            print(f"The following error occurred: {error}")
            # TODO: Display a pop up (chmurkę) with information regarding to what went wrong to the user
        return all_files

    def get_current_dir_right(self, file_name="") -> list:
        global PTH_R
        PTH_R = PTH_R.joinpath(file_name)
        if file_name == "":
            PTH_R = PTH_R.parent
        try:
            all_files = []
            # TODO: Fix entering certain directories like: Desktop
            all_files.append(QListWidgetItem(QIcon("Arrow_48x48"), "..."))
            for record in PTH_R.iterdir():
                if record.is_dir():
                    i_rec = QIcon("folder.png")
                    n_rec = QListWidgetItem(i_rec, record.name)
                    all_files.append(n_rec)
                elif record.is_file():
                    i_rec = QIcon("file.png")
                    n_rec = QListWidgetItem(i_rec, record.name)
                    all_files.append(n_rec)
        except OSError as error:
            print(f"The following error occurred: {error}")
            # TODO: Display a pop up (chmurkę) with information regarding to what went wrong to the user
        return all_files


class Window(QWidget):
    def __init__(self):
        super().__init__()
        # Main window setup
        self.setWindowTitle("QT Commander")
        self.setGeometry(0, 0, 1200, 800)
        self.lay = Listings()

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
