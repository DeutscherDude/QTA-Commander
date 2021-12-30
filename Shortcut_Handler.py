import os
import pathlib
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QListWidgetItem
from PySide6.QtCore import Qt
import DataFetcher as DF
from Icons.IconHandler import Icons
from dialog_box import CustomDialog
from tables import Tables


def copy_file() -> bool:
    """Copies currently selected item to the previously visited directory"""
    test = DF.fetch_dest_paths()
    file_path = test[0]
    dest_path = test[1]
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
    path = DF.fetch_c_it_p()
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
            path = DF.fetch_c_it_p()
            os.remove(path)
            __set_visibility(True)
            return True
        except os.error as error:
            print(f"An error occurred... {error}")
            return False


def __set_visibility(hidden: bool) -> None:
    itm = QApplication.focusWidget().currentItem()
    itm.setHidden(hidden)
