import os
import pathlib
import DataFetcher as DF
from dialog_box import CustomDialog


def copy_file() -> bool:
    """Copies currently selected item to the previously visited directory"""
    test = DF.fetch_dest_paths()
    file_path = test[0]
    print(test[0])
    dest_path = test[1]
    print(test[1])
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
    else:
        file = open(file_path, 'rb').read()
        open(dest_path, 'wb').write(file)
        return True

def delete_file(file_path) -> bool:
    try:
        os.remove(file_path)
        return True
    except:
        # Nie udało się usunąć pliku, brak dostępu
        # Except w Evencie?
        return False
