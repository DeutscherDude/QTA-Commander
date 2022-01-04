import os
import pathlib
import logging
import shutil
from send2trash import send2trash
from PySide6.QtGui import QIcon, QScreen
from PySide6.QtWidgets import QListWidgetItem, QApplication
from PySide6.QtCore import Qt
import DataFetcher as DF
from Icons.IconHandler import Icons
from Widgets.Custom_Widgets.dialog_box import CustomDialog
from Widgets.Custom_Widgets.tables import Tables

level = logging.DEBUG
FMT = '[%(levelname)s] %(asctime)s - %(message)s'
logging.basicConfig(level=level, format=FMT)


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
    """Permanently deletes a file/directory from a specified path"""
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
