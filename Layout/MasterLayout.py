from PySide6.QtWidgets import (QWidget, QVBoxLayout,
                            QListView, QHBoxLayout)
from Widgets.Custom_Widgets.tables import Tables
from Widgets.Custom_Widgets.titlebar import TitleBar
from Widgets.Custom_Widgets.bottomButtons import BottomButtons


class MasterLayout(QVBoxLayout):
    def __init__(self, tables: list[Tables], master: QWidget, *args):
        super().__init__()

        tables[0].setResizeMode(QListView.ResizeMode(1))

        listsLayout = QHBoxLayout()
        for i in range(len(tables)):
            tables[i].assing_tables(tables)
            listsLayout.addWidget(tables[i])

        if args is not None:
            for i in range(len(args)):
                test = args[i]
                listsLayout.addWidget(test)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(BottomButtons(master))

        title_test = QHBoxLayout()
        title_test.addWidget(TitleBar(master))

        self.addLayout(title_test)
        self.addLayout(listsLayout)
        self.addLayout(buttons_layout)
        self.setContentsMargins(0, 0, 0, 0)

    def add_custom_layout(self, *args, **kwargs):
        layout = QVBoxLayout()
        layout.addWidget(args)
        self.addLayout(layout)
        