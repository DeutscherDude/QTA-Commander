import os


def copy_file(file_path: str, dest_path: str) -> bool:
    try:
        print(file_path)
        print(dest_path)
        file = open(file_path, 'rb').read()
        open(dest_path, 'wb').write()
        return True
    except OSError as error:
        print(f"{error}")
        return False

def delete_file(file_path) -> bool:
    try:
        os.remove(file_path)
        return True
    except:
        # Nie udało się usunąć pliku, brak dostępu
        # Except w Evencie?
        return False
