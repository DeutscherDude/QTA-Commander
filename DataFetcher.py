import ctypes, itertools, os, pathlib
import platform, string, time
import Widgets.Custom_Widgets.tables as tables
from typing import List, Sequence
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QListWidgetItem
from Icons.IconHandler import Icons
from Widgets.Custom_Widgets.treeview import MyTreeWidget

### QListWidget/QListWidgetItem specific functions ###

def get_directories_paths(path: str, *args) -> List[pathlib.Path]:
    """Fetches a list paths of directories & files listed in the specified path."""
    s_path = pathlib.Path(path)
    try:
        directory = []
        for record in s_path.iterdir():
            directory.append(record)
    except OSError as error:
        print(f"The following error occurred {error}")
    return directory


def get_dir_widgets(path: pathlib.Path, file_name="", *args) -> List[QListWidgetItem]:
    """Fetches a list of QListWidgetItems based on specified path"""
    path = path.joinpath(file_name)
    try:
        directory = [QListWidgetItem(QIcon(Icons.return_), "...")]
        for record in path.iterdir():
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


def get_directories_tuples(path: str) -> List[tuple]:
    """Fetches a list of tuples containing name, time of last modification, size & suffix of the file/directory."""
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


def get_available_drives() -> List[str]:
    """Returns a string list of available drive names"""
    oper_sys = platform.system()
    if 'Windows' == oper_sys:
        drive_bitmask = ctypes.cdll.kernel32.GetLogicalDrives()
        return list(itertools.compress(string.ascii_uppercase,
                                   map(lambda x: ord(x) - ord('0'), bin(drive_bitmask)[:1:-1])))
    elif 'Linux' == oper_sys:
        return []
    

def fetch_dest_pths_w_items(items_inc = True) -> tuple:
    """Fetches a tuple with an item of QListWidgetItem type"""
    try:
        boy = tables.Tables.ex_tab[tables.Tables.c_index]
        if items_inc:
            file_path = boy.currentItem().text()
            dir_path = boy.return_path().joinpath(file_path)
            des_path = tables.Tables.ex_tab[tables.Tables.l_index].return_path().joinpath(file_path)
            return dir_path, des_path
        else:
            dir_path = boy.return_path()
            des_path = tables.Tables.ex_tab[tables.Tables.l_index].return_path()
            return dir_path, des_path
    except EnvironmentError as err:
        print(f"The following error occurred: {err}")


def cur_itm_pth() -> pathlib.Path:
    """Fetches a current item path - QListWidget specific"""
    boy = tables.Tables.ex_tab[tables.Tables.c_index]
    file_path = boy.currentItem().text()
    dir_path = boy.return_path().joinpath(file_path)
    return dir_path


### QTreeWidget/QTreeWidgetItem specific functions ###


def cur_itm_pth_tree() -> pathlib.Path:
    """Fetches a current item path - QTreeWidget specific"""
    boy = MyTreeWidget.Ex_Views[MyTreeWidget.Cur_Index]
    file_path = boy.currentItem().text(0)
    dir_path = boy.get_cur_path().joinpath(file_path)
    return dir_path

def fetch_dest_pths_w_items_tree() -> tuple[pathlib.Path, pathlib.Path]:
    """Fetches a tuple with an item of QTreeWidget type"""
    try:
        boy = MyTreeWidget.Ex_Views[MyTreeWidget.Cur_Index]
        file_path = boy.currentItem().text(0)
        dir_path = boy.get_cur_path().joinpath(file_path)
        des_path = MyTreeWidget.Ex_Views[MyTreeWidget.Last_Index].get_cur_path().joinpath(file_path)
        return dir_path, des_path
    except EnvironmentError as err:
        print(f"The following error occurred: {err}")
