from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QListWidgetItem, QListWidget, QWidget, QListView, \
    QAbstractItemView, QVBoxLayout, QMainWindow
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QIcon, QKeyEvent
from pathlib import Path
import os

BUTTON_WIDTH = 100
BUTTON_HEIGHT = 60
PTH_L = Path('/Users/kolok')
PTH_R = Path('/Users/kolok')


# TODO: Selecting, copying, deleting, moving multiple files
# TODO: OS stat - Podaje statystyki plików i folderów; os.path.isdir
# TODO: Add: exists from os.path; is_dir, is_file       For operations on files & directories we use path
# TODO: Change the code to PYSIDE6
# TODO: Create a listener for keyboard presses on UP, DOWN arrows & Function Keys - subclass of QWidget

def get_initial_directory():
    pth = Path('/Users/kolok')
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


class Window(QWidget):
    def __init__(self):
        super().__init__()
        # Main window setup
        self.setWindowTitle("QT Commander")
        self.setGeometry(0, 0, 1200, 800)
        self.copy_butt = QPushButton("F5 Copy")
        self.move_butt = QPushButton("F6 Move")
        self.fldr_butt = QPushButton("F7 NewFolder")
        self.delete_butt = QPushButton("F8 Delete")

        self.test = QListWidget()

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
        outerLayout = QVBoxLayout()
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.test)
        topLayout.addWidget(self.test2)
        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(buttons_layout)
        self.setLayout(outerLayout)
        self.show()

    def get_current_dir(self, file_name: str) -> list:
        global PTH_L
        PTH_L = Path("{}/{}".format(PTH_L, file_name))
        all_files = []
        for record in PTH_L.iterdir():
            if record.is_dir():
                i_rec = QIcon("folder.png")
                n_rec = QListWidgetItem(i_rec, record.name)
                all_files.append(n_rec)
            elif record.is_file():
                i_rec = QIcon("file.png")
                n_rec = QListWidgetItem(i_rec, record.name)
                all_files.append(n_rec)
        return all_files

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_F5:
            print("F5 button has been pressed... suck my toes")
        elif event.key() == Qt.Key.Key_F6:
            print("F6 button has been pressed... suck my ding dong")
        elif event.key() == Qt.Key.Key_F7:
            print("F7 button has been pressed... suck my anus")
        elif event.key() == Qt.Key.Key_F8:
            print("F8 button has been pressed... kiss homies goodnight")

    def button_setup(self, button: QPushButton, app: QMainWindow) -> None:
        button.resize(BUTTON_WIDTH, BUTTON_HEIGHT)
        button.setParent(app)
        button.show()

    def copy_file(self, file_path: str, dest_path) -> bool:
        try:
            file = open(file_path, 'rb').read()
            open(dest_path, 'wb').write()
            return True
        except:
            print("Argh, an error occurred")
            return False

    def delete_file(self, file_path) -> bool:
        try:
            os.remove(file_path)
            return True
        except:
            # Nie udało się usunąć pliku, brak dostępu
            # Except w Evencie?
            return False

    def on_double_click(self, item: QListWidgetItem):
        print(f"beep boop, {item.text()}")
        txt = item.text()
        self.test.clear()
        items = self.get_current_dir(txt)
        for item in items:
            self.test.addItem(item)
