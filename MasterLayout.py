from PySide6.QtWidgets import QVBoxLayout, QPushButton, QListView, QHBoxLayout
from Tables import Tables


class MasterLayout(QVBoxLayout):
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

    def add_custom_layout(self, *args, **kwargs):
        layout = QVBoxLayout()
        layout.addWidget(args)
        self.addLayout(layout)
