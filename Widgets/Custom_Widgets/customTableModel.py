from typing import List
from PySide6.QtCore import QAbstractListModel
from PySide6.QtWidgets import QListWidgetItem, QTableWidget, QWidget
import DataFetcher as DF

class TableItemView(QAbstractListModel):
    def __init__(self, path: str) -> None:
        QAbstractListModel.__init__(self)
        
        self.path = path
        self.itemList = DF.get_directories_tuples(path)
        

    def rowCount(self, parent) -> int:
        return len(self.itemList)

    def columnCount(self, parent) -> int:
        return len(self.itemList[0])

    # def data(self, index: int) -> object:
    #     return super().data(index, role=role)
