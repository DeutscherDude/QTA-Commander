from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from pathlib import Path

BUTTON_WIDTH = 100
BUTTON_HEIGHT = 60

# TODO: OS stat - Podaje statystyki plików i folderów; os.path.isdir
# TODO: Add: exists from os.path; is_dir, is_file       For operations on files & directories we use path
# TODO: Change the code to PYSIDE6
# TODO: Create a listener for keyboard presses on UP, DOWN arrows & Function Keys - subclass of QWidget

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

        test = QListWidget()
        items = self.get_initial_directory()
        test.setResizeMode(QListView.ResizeMode(1))
        print(test.ResizeMode)
        test2 = QListWidget()
        print(test2.resizeMode())

        for item in items:
            test.addItem(item)

        items = self.get_initial_directory()

        for item in items:
            test2.addItem(item)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.copy_butt)
        buttons_layout.addWidget(self.move_butt)
        buttons_layout.addWidget(self.fldr_butt)
        buttons_layout.addWidget(self.delete_butt)
        outerLayout = QVBoxLayout()
        topLayout = QHBoxLayout()
        topLayout.addWidget(test)
        topLayout.addWidget(test2)
        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(buttons_layout)
        self.setLayout(outerLayout)
        self.show()

    def get_initial_directory(self):
        pth = Path('/Users/kolok')
        all_files = []
        for record in pth.iterdir():
            if record.is_dir():
                i_rec = QIcon("folder.png")
                n_rec = QListWidgetItem(i_rec, record.name)
                all_files.append(n_rec)
            elif record.is_file():
                i_rec = QIcon("file.png")
                n_rec = QListWidgetItem(i_rec, record.name)
                all_files.append(n_rec)
        return all_files

    def get_current_dir(self):
        pass


    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_F5:
            print("F5 button has been pressed... suck my toes")
        elif event.key() == Qt.Key.Key_F6:
            print("F6 button has been pressed... suck my ding dong")
        elif event.key() == Qt.Key.Key_F7:
            print("F7 button has been pressed... suck my anus")
        elif event.key() == Qt.Key.Key_F8:
            print("F8 button has been pressed... kiss homies goodnight")
