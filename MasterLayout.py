from PySide6.QtWidgets import QVBoxLayout, QPushButton, QListView, QHBoxLayout
from tables import Tables
import Shortcut_Handler
from titlebar import TitleBar


class MasterLayout(QVBoxLayout):
    def __init__(self, tables: list[Tables], *args):
        super().__init__()
        # TODO: Create a separate class where those buttons are created :^)
        self.copy_butt = QPushButton("F5 Copy")
        self.copy_butt.clicked.connect(Shortcut_Handler.copy_file)
        self.move_butt = QPushButton("F6 Move")
        self.move_butt.clicked.connect(Shortcut_Handler.move_file)
        self.fldr_butt = QPushButton("F7 NewFolder")
        self.fldr_butt.clicked.connect(Shortcut_Handler.create_dir)
        self.delete_butt = QPushButton("F8 Delete")
        self.delete_butt.clicked.connect(Shortcut_Handler.delete_file)

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

        if args is not None:
            for i in range(len(args)):
                test = args[i]
                topLayout.addWidget(test)

        self.addLayout(topLayout)
        self.addLayout(buttons_layout)

    def add_custom_layout(self, *args, **kwargs):
        layout = QVBoxLayout()
        layout.addWidget(args)
        self.addLayout(layout)
