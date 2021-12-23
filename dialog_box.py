from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QStyle
from PySide6.QtGui import QIcon
import IconHandler


class CustomDialog(QDialog):
    def __init__(self, title: str, txt: str) -> bool:
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(IconHandler.Icons.directory))

        # Creating buttons
        QBtn = QDialogButtonBox.Yes | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(txt)
        message.setWordWrap(True)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
