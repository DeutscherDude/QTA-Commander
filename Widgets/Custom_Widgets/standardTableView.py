from pathlib import Path
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
import DataFetcher as DF
from PySide6.QtCore import Qt

class TableLayout(QTableWidget):
    def __init__(self, path: str) -> None:
        super().__init__()
        self.setColumnCount(4)

        self.pth = str(path)
        self.my_items = DF.get_directories_tuples(self.pth)
        self.setRowCount(len(self.my_items))
        # self.itemDoubleClicked(self.on_double_click)

        test = 0

        for i in self.my_items:
            item = QTableWidgetItem(i[0])
            print(i[0])
            self.setItem(test, 0, item)
            item = QTableWidgetItem(i[1])
            self.setItem(test, 1, item)
            item = QTableWidgetItem(i[2])
            self.setItem(test, 2, item)
            item = QTableWidgetItem(i[3])
            self.setItem(test, 3, item)
            test = test + 1

        test = 0

    def itemDoubleClicked(self, item: QTableWidgetItem):
        print("boop")

    def on_double_click(self, item: QTableWidgetItem):
        print("BOOP")
    