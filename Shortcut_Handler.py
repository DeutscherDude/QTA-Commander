import os
import pathlib
from dialog_box import CustomDialog


def copy_file(file_path: pathlib.Path, dest_path: pathlib.Path) -> bool:
    """Copies currently selected item to the specified path"""

    if os.path.isfile(dest_path):
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

def delete_file(file_path) -> bool:
    try:
        os.remove(file_path)
        return True
    except:
        # Nie udało się usunąć pliku, brak dostępu
        # Except w Evencie?
        return False
