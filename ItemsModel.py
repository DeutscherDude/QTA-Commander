from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QWidget, QTableView
from PySide6.QtWidgets import QListView


class ItemModel(QStandardItemModel):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setRowCount(2)


class TableView(QTableView):
    def __init__(self):
        super(self).__init__()
