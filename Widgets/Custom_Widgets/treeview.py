import pathlib
import logging
from typing import List
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtCore import QDir, QDirIterator, Qt, Signal
from PySide6.QtWidgets import QAbstractItemView, QFileIconProvider, QTreeWidget, QTreeWidgetItem
from Icons.IconHandler import Icons


class MyTreeWidget(QTreeWidget):

    Item_Double_Clicked = Signal(QTreeWidgetItem)

    def __init__(self, parent=None):
        super(MyTreeWidget, self).__init__(parent=parent)
        self.setColumnCount(4)
        self.cur_dir = ""
        
        self.Item_Double_Clicked.connect(self.enter_directory)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setAcceptDrops(True)
        self.setDragDropOverwriteMode(True)

        header = QTreeWidgetItem(["Name", "Size", "Type", "Date modified"])
        header.setTextAlignment(0, Qt.AlignCenter)
        header.setTextAlignment(1, Qt.AlignCenter)
        header.setTextAlignment(2, Qt.AlignCenter)
        header.setTextAlignment(3, Qt.AlignCenter)

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
            self.cur_dir = self.cur_dir.as_posix()

            iterator = QDirIterator(self.cur_dir, QDir.NoDotAndDotDot | QDir.AllEntries | QDirIterator.Subdirectories)
            new_tree = self.iterate(iterator)
            self.clear()
            self.addTopLevelItems(new_tree)
            self.sortByColumn(0, Qt.SortOrder.AscendingOrder)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.Item_Double_Clicked.emit(event)
        return super().mouseDoubleClickEvent(event)

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
        

    

