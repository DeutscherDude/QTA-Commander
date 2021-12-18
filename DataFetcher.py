import os
import pathlib
import time
from typing import List
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QListWidgetItem

from IconHandler import Icons


class DataFetcher:
    def __init__(self, *args):
        self.size = 0
        self.drives = ()

    def get_directories(self, path: str, *args) -> List[pathlib.Path]:
        """Fetches a list of directories & files listed in the specified path."""
        s_path = pathlib.Path(path)
        try:
            directory = []
            for record in s_path.iterdir():
                directory.append(record)
        except OSError as error:
            print(f"The following error occurred {error}")
        return directory

    def get_directories(self, path: str, file_name="", *args) -> List[QListWidgetItem]:
        """Fetches a list of QListWidgetItems based on specified path"""
        s_path = pathlib.Path(path)
        s_path.joinpath(file_name)
        try:
            directory = [QListWidgetItem(QIcon(Icons.return_), "...")]
            for record in s_path.iterdir():
                if record.is_dir():
                    i_rec = QIcon(Icons.directory)
                    n_rec = QListWidgetItem(i_rec, record.name)
                    directory.append(n_rec)
                elif record.is_file():
                    i_rec = QIcon(Icons.file)
                    n_rec = QListWidgetItem(i_rec, record.name)
                    directory.append(n_rec)
        except OSError as error:
            print(f"The following error occurred: {error}")
        return directory

    def get_directories(self, path: str) -> List[tuple]:
        s_path = pathlib.Path(path)
        try:
            directory = []
            for record in s_path.iterdir():
                rec_time = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(os.stat(record).st_mtime))
                rec_size = os.stat(record).st_size
                rec_type = record.suffix
                if rec_type == '':
                    rec_type = 'Folder'
                directory.append((record.name, rec_time, rec_type, rec_size))
        except OSError as error:
            print(f"The following error occurred: {error}")
        return directory


