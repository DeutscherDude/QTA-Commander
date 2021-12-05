from PyQt6.QtWidgets import *
import os

BUTTON_WIDTH = 100
BUTTON_HEIGHT = 60


class Butts(QWidget):
    def __init__(self, app: QMainWindow):
        super().__init__()
        # Copy Button setup
        self.copy_butt = QPushButton("F5 Copy")
        self.button_setup(self.copy_butt, app)

        # Move button setup
        self.move_butt = QPushButton("F6 Move")
        self.button_setup(self.move_butt, app)

        # Create folder button setup
        self.fldr_butt = QPushButton("F7 NewFolder")
        self.button_setup(self.fldr_butt, app)

        # Delete button setup
        self.delete_butt = QPushButton("F8 Delete")
        self.button_setup(self.delete_butt, app)
        layout = QHBoxLayout()
        layout.addWidget(self.copy_butt)
        layout.addWidget(self.move_butt, 1)
        layout.addWidget(self.fldr_butt, 2)
        layout.addWidget(self.delete_butt, 3)
        self.setLayout(layout)
        # self.distribute_buttons(BUTTS_List, app)
        self.show()

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
            # Nie udało się skopiować pliku, pop-up
            return False

    def delete_file(self, file_path) -> bool:
        try:
            os.remove(file_path)
            return True
        except:
            # Nie udało się usunąć pliku, brak dostępu
            # Except w Evencie?
            return False
