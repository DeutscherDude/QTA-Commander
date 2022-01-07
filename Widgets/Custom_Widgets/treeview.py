import pathlib
import logging
from typing import List
from PySide6.QtGui import QDrag, QDragEnterEvent, QDropEvent, QIcon, QMouseEvent, QPixmap
from PySide6.QtCore import QDir, QDirIterator, QFileInfo, QMimeData, Qt, Signal
from PySide6.QtWidgets import QAbstractItemView, QFileIconProvider, QTextBrowser, QTreeWidget, QTreeWidgetItem
from Icons.IconHandler import Icons


class MyTreeWidget(QTreeWidget):

    Item_Double_Clicked = Signal(QTreeWidgetItem)
    Dragged_Item = ''

    def __init__(self, parent=None):
        super(MyTreeWidget, self).__init__(parent=parent)
        self.setColumnCount(4)
        self.cur_dir = ""
        
        self.Item_Double_Clicked.connect(self.enter_directory)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setAcceptDrops(False)
        self.setDragDropOverwriteMode(True)

        header = QTreeWidgetItem(["Name", "Size", "Type", "Date modified"])
        header.setTextAlignment(0, Qt.AlignCenter); header.setTextAlignment(1, Qt.AlignCenter)
        header.setTextAlignment(2, Qt.AlignCenter); header.setTextAlignment(3, Qt.AlignCenter)

        self.setHeaderItem(header)
        self.setSortingEnabled(True)
        
        self._init_fillTree()


    def _init_fillTree(self):
        drives = QDir.drives()

        icon_prov = QFileIconProvider()
        tree_list = []
        for i in range(0, len(drives)):
            if drives[i].isDir:
                type = "Folder"
            elif drives[i].isFile:
                type = "File"
            else:
                type = "Drive" 

            dir_item = QTreeWidgetItem([drives[i].path(), drives[i].size(), 
                                        type, drives[i].lastModified().toString("dd.MM.yyyy hh:mm:ss")])
            icon = icon_prov.icon(drives[i])
            dir_item.setIcon(0, icon)

            tree_list.append(dir_item)
        self.clear()
        self.addTopLevelItems(tree_list)

    def enter_directory(self):
        self.cur_dir = pathlib.Path(self.cur_dir)
        further = True

        item = self.itemFromIndex(self.currentIndex())

        if item.text(0) == "...":
            if self.cur_dir == self.cur_dir.parent:
                self._init_fillTree()
                further = False
            self.cur_dir = self.cur_dir.parent
        else:
            self.cur_dir = self.cur_dir.joinpath(item.text(0))

        if further:
            self.setAcceptDrops(True)
            self.cur_dir = self.cur_dir.as_posix()
            iterator = QDirIterator(self.cur_dir, QDir.NoDotAndDotDot | QDir.AllEntries | QDirIterator.Subdirectories)
            new_tree = self.iterate(iterator)
            self.clear()
            self.addTopLevelItems(new_tree)
            self.sortByColumn(0, Qt.SortOrder.AscendingOrder)

    def iterate(self, iterator: QDirIterator) -> List[QTreeWidgetItem]:
        icon_prov = QFileIconProvider()
        return_item = QTreeWidgetItem(["...", "", "", ""])
        return_item.setIcon(0, QIcon(Icons.return_))
        new_tree = [return_item]

        while iterator.hasNext():
            iterator.next()
            item = iterator.fileInfo()
            if item.isFile():
                type = "File"
            elif item.isDir():
                type = "Folder"
            else:
                type = "Drive" 
            icon = icon_prov.icon(item)

            dir_item = QTreeWidgetItem([item.completeBaseName(), item.size(), type, item.lastModified().toString("dd.MM.yyyy hh:mm:ss")])
            dir_item.setIcon(0, icon)
            new_tree.append(dir_item)
        
        return new_tree
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        icon_prov = QFileIconProvider()
        item = MyTreeWidget.Dragged_Item[0]
        dir_ = MyTreeWidget.Dragged_Item[1]
        pth = pathlib.Path(dir_)
        pth = pth.joinpath(item.text(0))
        pth = pth.as_posix()

        icon = icon_prov.icon(QFileInfo(pth))
        item.setIcon(0, icon)
        self.addTopLevelItem(QTreeWidgetItem([item.text(0), item.text(1), item.text(2), item.text(3)]))
        event.accept()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            MyTreeWidget.Dragged_Item = self.extract_data(self.itemAt(event.pos()))
        return super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.Item_Double_Clicked.emit(event)
            return super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        return super().mouseReleaseEvent(event)

    def extract_data(self, item: QTreeWidgetItem):
        name = item.text(0)
        size = item.text(1)
        type = item.text(2)
        edit_t = item.text(3)
        new_itm = QTreeWidgetItem([name, size, type, edit_t])
        return new_itm, self.cur_dir
