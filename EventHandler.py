import os


def copy_file(file_path: str, dest_path) -> bool:
    try:
        file = open(file_path, 'rb').read()
        open(dest_path, 'wb').write()
        return True
    except:
        print("Argh, an error occurred")
        return False


def delete_file(file_path) -> bool:
    try:
        os.remove(file_path)
        return True
    except:
        # Nie udało się usunąć pliku, brak dostępu
        # Except w Evencie?
        return False
