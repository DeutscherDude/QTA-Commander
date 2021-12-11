import ctypes
import os
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QKeyEvent
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QListWidgetItem, QListWidget, QWidget, QListView, \
    QAbstractItemView, QVBoxLayout

BUTTON_WIDTH = 100
BUTTON_HEIGHT = 60
HOME = os.environ['USERPROFILE']
PTH_L = Path(HOME)
PTH_R = Path('/Users')


# TODO: Selecting, copying, deleting, moving multiple files
# TODO: OS stat - Podaje statystyki plików i folderów; os.path.isdir


def get_initial_directory():
    global PTH_L
    pth = PTH_L
    all_files = []
    for record in pth.iterdir():
        if record.is_dir():
            i_rec = QIcon("folder.png")
            n_rec = QListWidgetItem(i_rec, record.stem)
            all_files.append(n_rec)
        elif record.is_file():
            i_rec = QIcon("file.png")
            n_rec = QListWidgetItem(i_rec, record.stem)
            all_files.append(n_rec)
    return all_files


class Listings(QVBoxLayout):
    def __init__(self):
        super().__init__()
        print(HOME)
        self.test = QListWidget()
        self.test.addItem(QListWidgetItem(QIcon("Arrow_48x48"), "..."))
        self.copy_butt = QPushButton("F5 Copy")
        self.move_butt = QPushButton("F6 Move")
        self.fldr_butt = QPushButton("F7 NewFolder")
        self.delete_butt = QPushButton("F8 Delete")

        items = get_initial_directory()
        self.test.setResizeMode(QListView.ResizeMode(1))
        self.test2 = QListWidget()

        for item in items:
            self.test.addItem(item)

        items = get_initial_directory()

        for item in items:
            self.test2.addItem(item)

        self.test.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.test2.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.test.itemDoubleClicked.connect(self.on_double_click)
        self.test2.itemDoubleClicked.connect(self.on_double_click)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.copy_butt)
        buttons_layout.addWidget(self.move_butt)
        buttons_layout.addWidget(self.fldr_butt)
        buttons_layout.addWidget(self.delete_butt)
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.test)
        topLayout.addWidget(self.test2)
        self.addLayout(topLayout)
        self.addLayout(buttons_layout)

    def on_double_click(self, item: QListWidgetItem):
        global PTH_L
        txt = item.text()
        # TODO: Figuring out the parent widget of the item?
        if txt == "...":
            # TODO: Using the Windows base icons I extracted :^) & maaaaybe introducing some of my own choosing
            # TODO: Using root whilst hitting the end of the drive?
            test = PTH_L.parent
            print(PTH_L)
            PTH_L = test
            self.test.clear()
            items = self.get_current_dir()
        else:
            self.test.clear()
            items = self.get_current_dir(txt)
        for item in items:
            self.test.addItem(item)

    def get_current_dir(self, file_name="") -> list:
        global PTH_L
        PTH_L = PTH_L.joinpath(file_name)
        try:
            all_files = []
            # TODO: Fix entering certain directories like: Desktop
            all_files.append(QListWidgetItem(QIcon("Arrow_48x48"), "..."))
            for record in PTH_L.iterdir():
                if record.is_dir():
                    i_rec = QIcon("folder.png")
                    n_rec = QListWidgetItem(i_rec, record.stem)
                    all_files.append(n_rec)
                elif record.is_file():
                    i_rec = QIcon("file.png")
                    n_rec = QListWidgetItem(i_rec, record.stem)
                    all_files.append(n_rec)
        except OSError as error:
            print(f"The following error occurred: {error}")
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
            bitch = self.lay.test.currentItem()
            self.lay.on_double_click(bitch)
        elif event.key() == Qt.Key.Key_Backspace:
            global PTH_L
            test = PTH_L.parent
            PTH_L = test
            self.lay.test.clear()
            items = self.lay.get_current_dir()
            for item in items:
                self.lay.test.addItem(item)

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
