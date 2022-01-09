from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel
from PySide6.QtGui import QIcon, QPixmap
import Icons.IconHandler as IconHandler


class CustomDialog(QDialog):
    All_Accepted = Signal()

    def __init__(self, title: str, txt: str) -> bool:
        """Multi use-case dialog box with Yes/Cancel option"""
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(IconHandler.Icons.directory))

        QBtn = QDialogButtonBox.Yes | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(txt, ObjectName= "dialog_box")
        message.setWordWrap(True)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


    def __init__(self, title: str, txt: str, path =  "") -> bool:
        """Specifically for handling QTreeWidget"""
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(IconHandler.Icons.directory))

        QBtn = QDialogButtonBox.Yes |QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.file_icon = QPixmap()

        self.icon_lab = QLabel()

        self.layout = QVBoxLayout()
        message = QLabel(txt, ObjectName= "dialog_box")
        message.setWordWrap(True)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
