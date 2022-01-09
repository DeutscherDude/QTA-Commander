import os
import pathlib
import logging
import shutil
import time
from send2trash import send2trash
from PySide6.QtGui import QIcon, QScreen
from PySide6.QtWidgets import QFileIconProvider, QListWidgetItem, QApplication, QTreeWidgetItem
from PySide6.QtCore import QFileInfo, Qt
import DataFetcher as DF
from Icons.IconHandler import Icons
from Widgets.Custom_Widgets.dialog_box import CustomDialog
from Widgets.Custom_Widgets.tables import Tables
from Widgets.Custom_Widgets.treeview import MyTreeWidget

level = logging.DEBUG
FMT = '[%(levelname)s] %(asctime)s - %(message)s'
logging.basicConfig(level=level, format=FMT)


def copy_file_tree(add_item = False) -> bool:
    """Copies currently selected item(TreeWidget) to the previously visited directory"""
    item = DF.fetch_dest_pths_w_items_tree()
    file_path, dest_path = item[0], item[1]
    file_inf = QFileInfo(file_path)
    if os.path.exists(dest_path):
        dlg = CustomDialog("Overwrite existing file?", f"{file_inf.fileName()} already exists, are you sure you want to overwrite "
                                                       "it?")
        if dlg.exec():
            try:
                file = open(file_path, 'rb').read()
                open(dest_path, 'wb').write(file)
                os.chmod(dest_path, 777)
                return True
            except OSError as error:
                print(f"{error}")
                return False
        else:
            return False
    else:
        if file_path.is_file():
            if add_item:
                icon_prov = QFileIconProvider()
                icon = icon_prov.icon(file_inf)

                dest_tab = MyTreeWidget.Ex_Views[Tables.l_index]
                item = QTreeWidgetItem([item.fileName(), f"{str(round((item.size() / 1048576), 2))} MB", 
                                        type, item.lastModified().toString("dd.MM.yyyy hh:mm:ss")])
                item.setIcon(0, icon)
                dest_tab.addTopLevelItem(item)
            file = open(file_path, 'rb').read()
            open(dest_path, 'wb').write(file)
            return True
        elif file_path.is_dir():
            if add_item:
                dest_tab = MyTreeWidget.Ex_Views[MyTreeWidget.Last_Index]
                item = QTreeWidgetItem([file_path.name, '', '<DIR>', str(time.ctime())])
                dest_tab.addTopLevelItem(item)
            shutil.copytree(file_path, dest_path)
            return True

def move_file_tree() -> bool:
    """Moves the selected file to the specified path"""
    if copy_file_tree():
        try:
            path = DF.cur_itm_pth_tree()
            os.remove(path)
            return True
        except os.error as error:
            print(f"An error occurred... {error}")
            return False

def create_dir_tree(pressed = True, dir_name="New Folder") -> bool:
    """Creates a new directory called New Folder"""
    # TODO: Add functionality to input your own name for the folder. Default: "New Folder"
    path = MyTreeWidget.Ex_Views[MyTreeWidget.Cur_Index].get_cur_path()
    path = path.joinpath(dir_name)
    try:
        os.mkdir(path)
        itm_info = QFileInfo(path.as_posix())
        icon_prov = QFileIconProvider()
        item = QTreeWidgetItem([dir_name, "", "<DIR>", str(time.ctime())])
        icon = icon_prov.icon(itm_info)
        item.setIcon(0, icon)

        boy = MyTreeWidget.Ex_Views[Tables.c_index]
        boy.addTopLevelItem(item)
    except OSError as err:
        print(f"Sadly, the following error occurred: {err}")

def enter_return_tree() -> bool:
    current_table = QApplication.focusWidget()
    current_table.enter_directory(current_table.currentItem())
    return True

def return_to_previous_tree() -> bool:
    current_table = QApplication.focusWidget()
    if current_table.cur_dir != pathlib.Path("\\"):
        current_table.enter_directory(QTreeWidgetItem(["...", '','','']))
    return True

def delete_file_tree() -> bool:
    """Permanently deletes a file/directory from a specified path"""
    path = DF.cur_itm_pth_tree()
    dlg = CustomDialog("Move file to trash bin?", "Are you sure you want to move this "
                                                     "file/directory to trash?")
    if dlg.exec():
        try:
            os.chmod(path, 777)
            send2trash(path)
            return True
        except os.error as error:
            logging.error(f"The operation failed. {error}")
            print(f"An error occurred... {error}")
            return False


def copy_file() -> bool:
    """Copies currently selected item to the previously visited directory"""
    test = DF.fetch_dest_pths_w_items()
    file_path, dest_path = test[0], test[1]
    if os.path.isfile(dest_path) or os.path.isdir(dest_path):
        dlg = CustomDialog("Overwrite existing file?", "This file already exists, are you sure you want to overwrite "
                                                       "it?")
        if dlg.exec():
            try:
                file = open(file_path, 'rb').read()
                open(dest_path, 'wb').write(file)
                os.chmod(dest_path, 777)
                return True
            except OSError as error:
                print(f"{error}")
                return False
        else:
            return False
    else:
        if file_path.is_file():
            dest_tab = Tables.ex_tab[Tables.l_index]
            item = QListWidgetItem(QIcon(Icons.file), dest_path.name)
            dest_tab.addItem(item)
            boy = dest_tab.findItems(dest_path.name, Qt.MatchExactly)
            boy[0].setHidden(False)
            file = open(file_path, 'rb').read()
            open(dest_path, 'wb').write(file)
            return True
        elif file_path.is_dir():
            dest_tab = Tables.ex_tab[Tables.l_index]
            item = QListWidgetItem(QIcon(Icons.directory), dest_path.name)
            dest_tab.addItem(item)
            boy = dest_tab.findItems(dest_path.name, Qt.MatchExactly)
            boy[0].setHidden(False)
            shutil.copytree(file_path, dest_path)
            return True

def delete_file() -> bool:
    """Sends a specified item to trash bin"""
    path = DF.cur_itm_pth()
    dlg = CustomDialog("Move file to trash bin?", "Are you sure you want to move this "
                                                     "file/directory to trash?")
    if dlg.exec():
        try:
            os.chmod(path, 777)
            send2trash(path)
            __set_visibility(True)
            return True
        except os.error as error:
            logging.error(f"The operation failed. {error}")
            print(f"An error occurred... {error}")
            return False

def move_file() -> bool:
    """Moves the selected file to the specified path"""
    if copy_file():
        try:
            path = DF.cur_itm_pth()
            os.remove(path)
            __set_visibility(True)
            return True
        except os.error as error:
            print(f"An error occurred... {error}")
            return False


def create_dir(pressed = True, dir_name="New Folder") -> bool:
    """Creates a new directory called New Folder"""
    # TODO: Add functionality to input your own name for the folder. Default: "New Folder"
    paths = DF.fetch_dest_pths_w_items(False)
    path = paths[0]
    path = path.joinpath(dir_name)
    try:
        os.mkdir(path)
        item = QListWidgetItem(QIcon(Icons.directory), path.name)
        boy = Tables.ex_tab[Tables.c_index]
        boy.addItem(item)
        itm = boy.findItems(path.name, Qt.MatchExactly)
        itm[0].setHidden(False)
    except OSError as err:
        print(f"Sadly, the following error occurred: {err}")

def return_to_previous() -> bool:
    current_table = QApplication.focusWidget()
    if current_table.paths != pathlib.Path("\\"):
        current_table.on_double_click(QListWidgetItem("..."))
    return True

def enter_return() -> bool:
    current_table = QApplication.focusWidget()
    current_table.on_double_click(current_table.currentItem())
    return True

def __set_visibility(hidden: bool) -> None:
    """Sets visibility of an item. Internal method"""
    itm = Tables.ex_tab[Tables.c_index].currentItem()
    itm.setHidden(hidden)


def maximizeWindow() -> None:
    app = QApplication.activeWindow()
    screen_s = QScreen.availableGeometry(QApplication.primaryScreen())
    if app.windowState() != Qt.WindowMaximized:
        app.setWindowState(Qt.WindowMaximized)
    else:
        app.showNormal()

def minimizeWindow() -> None:
    app = QApplication.activeWindow()
    app.setWindowState(Qt.WindowMinimized)

def closeApp() -> None:
    app = QApplication.activeWindow()
    app.close()
