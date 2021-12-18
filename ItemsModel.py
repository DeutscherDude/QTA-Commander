import operator

from PySide6.QtCore import SIGNAL, QAbstractTableModel
from PySide6.QtGui import QStandardItemModel, QFont, QIcon, Qt
from PySide6.QtWidgets import QWidget, QTableView
from PySide6.QtWidgets import QListView, QVBoxLayout, QTableWidget, QTableWidgetItem
from IconHandler import Icons


class MyTableModel(QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        return len(self.mylist[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None

        return self.mylist[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]

        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.mylist = sorted(self.mylist, key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(SIGNAL("layoutChanged()"))


class Example(QWidget):
    def __init__(self, data_list, header):
        super().__init__()
        self.initUI(data_list, header)
        self.resize(600, 400)
        self.setWindowTitle("Click on column title to sort")

    def initUI(self, data_list, header):
        table_view = QTableView()
        table_model = MyTableModel(self, data_list, header)
        table_view.setModel(table_model)

        # set font
        font = QFont("Arial", 8)
        table_view.setFont(font)

        # set column width to fit contents (set font first!)
        table_view.setColumnWidth(0,260)

        # enable sorting
        table_view.setSortingEnabled(True)
        layout = QVBoxLayout(self)
        layout.addWidget(table_view)
        self.setLayout(layout)
