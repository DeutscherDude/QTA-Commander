import pathlib
import os
from types import NoneType
from typing import List
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QIcon, QMouseEvent
from PySide6.QtCore import QDir, QDirIterator,QFileInfo, Qt, Signal
from PySide6.QtWidgets import QAbstractItemView, QFileIconProvider, QHeaderView,QTreeWidget, QTreeWidgetItem
from Icons.IconHandler import Icons
import Shortcut_Handler
from Widgets.Custom_Widgets.dialog_box import CustomDialog


class MyTreeWidget(QTreeWidget):
    Item_Double_Clicked = Signal(QTreeWidgetItem)

    Dragged_Items = []
    Free_Index = 0
    Cur_Index = 0
    Last_Index = 1
    Ex_Views = []

    def __init__(self, headers=["Name", "Size", "Suf.", "Date modified"], parent=None):
        super(MyTreeWidget, self).__init__(parent=parent)
        self.setColumnCount(4)
        self.cur_dir = ""
        self.widg_names = []
        
        self.itemDoubleClicked.connect(self.enter_directory)
        self.itemClicked.connect(self._assign_indexes)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setAcceptDrops(False)
        self.setDragDropOverwriteMode(True)

        header = QTreeWidgetItem(headers)

        header.setTextAlignment(0, Qt.AlignCenter); header.setTextAlignment(1, Qt.AlignCenter)
        header.setTextAlignment(2, Qt.AlignCenter); header.setTextAlignment(3, Qt.AlignCenter)

        self.setHeaderItem(header)
        self.header().setObjectName(u"header")
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
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
            self.widg_names.append(drives[i].path())
            icon = icon_prov.icon(drives[i])
            dir_item.setIcon(0, icon)
            tree_list.append(dir_item)

        self.clear()
        self.addTopLevelItems(tree_list)

    def enter_directory(self, item: QTreeWidgetItem):
        self.cur_dir = pathlib.Path(self.cur_dir)
        further = True

        if item.text(0) == "...":
            if self.cur_dir == self.cur_dir.parent:
                self._init_fillTree()
                further = False
            self.cur_dir = self.cur_dir.parent
        elif os.path.isfile(os.path.join(self.cur_dir.as_posix(), item.text(0))):
            os.startfile(self.cur_dir.joinpath(item.text(0)))
        else:
            self.cur_dir = self.cur_dir.joinpath(item.text(0))

        if further:
            self.setAcceptDrops(True)
            dir = self.cur_dir.as_posix()
            iterator = QDirIterator(dir, QDir.NoDotAndDotDot | QDir.AllEntries | QDirIterator.Subdirectories)
            new_tree = self.iterate(iterator)
            self.clear()
            self.addTopLevelItems(new_tree)
            self.sortByColumn(0, Qt.SortOrder.AscendingOrder)

    def iterate(self, iterator: QDirIterator) -> List[QTreeWidgetItem]:
        icon_prov = QFileIconProvider()
        return_item = QTreeWidgetItem(["...", "", "", ""])
        return_item.setIcon(0, QIcon(Icons.return_))
        new_tree = [return_item]

        self.widg_names = []

        while iterator.hasNext():
            iterator.next()
            item = iterator.fileInfo()
            icon = icon_prov.icon(item)

            self.widg_names.append(item.fileName())
            dir_item = QTreeWidgetItem([item.fileName(), f"{str(round((item.size() / 1048576), 2))} MB", 
                                        item.suffix(), item.lastModified().toString("dd.MM.yyyy hh:mm:ss")])
            
            dir_item.setIcon(0, icon)
            new_tree.append(dir_item)
        
        return new_tree
        
    def get_cur_path(self) -> pathlib.Path: 
        return self.cur_dir

    def _assign_indexes(self) -> None:
        if self.index != MyTreeWidget.Cur_Index:
            MyTreeWidget.Last_Index = MyTreeWidget.Cur_Index
            MyTreeWidget.Cur_Index = self.index

    def dragEnterEvent(self, event: QDragEnterEvent):
        event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        items = MyTreeWidget.Dragged_Items
        dir_ = MyTreeWidget.Ex_Views[MyTreeWidget.Last_Index].get_cur_path()
        icon_prov = QFileIconProvider()
        bois = []
        for item in items:
            pth = pathlib.Path(dir_)
            pth = pth.joinpath(item.text(0))
            cur_pth = pathlib.Path(self.cur_dir)
            cur_pth = cur_pth.joinpath(item.text(0))

            pth = pth.as_posix()
            icon = icon_prov.icon(QFileInfo(pth))
            copy = QTreeWidgetItem([item.text(0), item.text(1), item.text(2), item.text(3)])
            copy.setIcon(0, icon)
            bois.append(copy)
    
        Shortcut_Handler.copy_file_tree()
        
        self.setAcceptDrops(True)
        if len(items) > 1:
            self.addTopLevelItems(bois)
        elif bois[0].text(0) not in self.widg_names:
            self.addTopLevelItem(bois[0])
            self.widg_names.append(bois[0].text(0))
        event.accept()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton & len(self.selectedItems()) != 0:
            MyTreeWidget.Dragged_Items = self.selectedItems()
        return super().mousePressEvent(event)

    # def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
    #     if event.buttons() == Qt.LeftButton and type(self.itemAt(event.pos())) != NoneType:
    #         self.Item_Double_Clicked.emit(event)
    #         return super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        return super().mouseReleaseEvent(event)
