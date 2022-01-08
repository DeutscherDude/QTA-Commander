import pathlib
import os
from typing import List
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QIcon, QMouseEvent, QPixmap
from PySide6.QtCore import QDir, QDirIterator,QFileInfo, Qt, Signal
from PySide6.QtWidgets import QAbstractItemView, QFileIconProvider,QTreeWidget, QTreeWidgetItem
from Icons.IconHandler import Icons


class MyTreeWidget(QTreeWidget):

    Item_Double_Clicked = Signal(QTreeWidgetItem)
    Dragged_Items = []


    Free_Index = 0
    Cur_Index = 0
    Last_Index = 1
    Ex_Views = []

    def __init__(self, headers=["Name", "Size", "Type", "Date modified"], parent=None):
        super(MyTreeWidget, self).__init__(parent=parent)
        self.setColumnCount(4)
        self.cur_dir = ""
        
        self.Item_Double_Clicked.connect(self.enter_directory)
        self.setDragEnabled(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setAcceptDrops(False)
        self.setDragDropOverwriteMode(True)

        header = QTreeWidgetItem(headers)
        header.setTextAlignment(0, Qt.AlignCenter); header.setTextAlignment(1, Qt.AlignCenter)
        header.setTextAlignment(2, Qt.AlignCenter); header.setTextAlignment(3, Qt.AlignCenter)

        self.setHeaderItem(header)
        self.setSortingEnabled(True)
       
        self._init_fillTree()

        MyTreeWidget.Ex_Views.append(self)
        self.index = MyTreeWidget.Free_Index
        MyTreeWidget.Free_Index = MyTreeWidget.Free_Index + 1


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
        
    def get_cur_path(self) -> str:
        return self.cur_dir

    def dragEnterEvent(self, event: QDragEnterEvent):
        event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        items = MyTreeWidget.Dragged_Items

        # self.findItems()

        dir_ = MyTreeWidget.Ex_Views[MyTreeWidget.Last_Index].get_cur_path()
        icon_prov = QFileIconProvider()
        bois = []
        for item in items:
            pth = pathlib.Path(dir_)
            pth = pth.joinpath(item.text(0))
            pth = pth.as_posix()
            icon = icon_prov.icon(QFileInfo(pth))
            copy = QTreeWidgetItem([item.text(0), item.text(1), item.text(2), item.text(3)])
            copy.setIcon(0, icon)
            bois.append(copy)
    
        self.setAcceptDrops(True)

        if len(items) > 1:
            self.addTopLevelItems(bois)
        else:
            self.addTopLevelItem(bois[0])
        
        event.accept()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton & len(self.selectedItems()) != 0:
            MyTreeWidget.Dragged_Items = self.selectedItems()
        return super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.Item_Double_Clicked.emit(event)
            return super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        return super().mouseReleaseEvent(event)