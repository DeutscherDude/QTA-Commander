import os
from PySide6.QtWidgets import QApplication
import DataFetcher as DF
from dialog_box import CustomDialog


def copy_file() -> bool:
    """Copies currently selected item to the previously visited directory"""

    # TODO: Add the item live to the list & update it :)
    test = DF.fetch_dest_paths()
    file_path = test[0]
    print(test[0])
    dest_path = test[1]
    print(test[1])
    if os.path.isfile(dest_path) or os.path.isdir(dest_path):
        dlg = CustomDialog("Overwrite existing file?", "This file already exists, are you sure you want to overwrite it?")
        if dlg.exec():
            try:
                file = open(file_path, 'rb').read()
                open(dest_path, 'wb').write(file)
                return True
            except OSError as error:
                print(f"{error}")
                return False
        else:
            return False
    else:
        file = open(file_path, 'rb').read()
        open(dest_path, 'wb').write(file)
        return True

def delete_file() -> bool:
    """Permanently deletes a file/directory from a specified path"""
    path = DF.fetch_c_it_p()
    dlg = CustomDialog("Permanently delete a file?", "Are you sure you want to permanently delete this file/directory? This action cannot be undone.")
    if dlg.exec():
        try:
            print("Beep boop")
            os.remove(path)
            return True
        except os.error as error:
            print(f"An error occurred... {error}")
            return False

def move_file() -> bool:
    """Moves the selected file to the specified path"""
    if copy_file() == True:
        try:
            path = DF.fetch_c_it_p()
            print("Beep boop")
            os.remove(path)
            return True
        except os.error as error:
            print(f"An error occurred... {error}")
            return False
