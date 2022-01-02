import os
import pathlib
from PySide6.QtGui import QIcon, QScreen
from PySide6.QtWidgets import QListWidgetItem, QApplication
from PySide6.QtCore import Qt
import DataFetcher as DF
from Icons.IconHandler import Icons
from dialog_box import CustomDialog
from tables import Tables


def copy_file() -> bool:
    """Copies currently selected item to the previously visited directory"""
    test = DF.fetch_dest_pths_w_items()
    file_path, dest_path = test[0], test[1]
    if os.path.isfile(dest_path) or os.path.isdir(dest_path):
        dlg = CustomDialog("Overwrite existing file?", "This file already exists, are you sure you want to overwrite "
                                                       "it?")
        if dlg.exec():
            try:
                if file_path.is_file():
                    dest_tab = Tables.ex_tab[Tables.l_index]
                    item = QListWidgetItem(QIcon(Icons.file), dest_path.name)
                    dest_tab.addItem(item)
                    boy = dest_tab.findItems(dest_path.name, Qt.MatchExactly)
                    boy[0].setHidden(False)
                file = open(file_path, 'rb').read()
                open(dest_path, 'wb').write(file)
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
        elif file_path.is_dir():
            dest_tab = Tables.ex_tab[Tables.l_index]
            item = QListWidgetItem(QIcon(Icons.directory), dest_path.name)
            dest_tab.addItem(item)
            boy = dest_tab.findItems(dest_path.name, Qt.MatchExactly)
            boy[0].setHidden(False)
        file = open(file_path, 'rb').read()
        open(dest_path, 'wb').write(file)
        return True


def delete_file() -> bool:
    """Permanently deletes a file/directory from a specified path"""
    path = DF.cur_itm_pth()
    dlg = CustomDialog("Permanently delete a file?", "Are you sure you want to permanently delete this "
                                                     "file/directory? This action cannot be undone.")
    if dlg.exec():
        try:
            os.remove(path)
            __set_visibility(True)
            return True
        except os.error as error:
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
    if app.max_status == False:
        x_size = screen_s.width()
        y_size = screen_s.height()
        app.setGeometry(0, 0, x_size, y_size)
        app.max_status = True
    else:
        app.setGeometry(0, 0, 1240, 800)
        x_pos = (screen_s.width() - app.width())/2
        y_pos = (screen_s.height() - app.height())/2
        app.move(x_pos, y_pos)
        app.max_status = False


def closeApp() -> None:
    app = QApplication.activeWindow()
    app.close()
