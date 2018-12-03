from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class AddMainWindow(QMainWindow):
    def __init__(self, parent=None, ui=None):
        super(AddMainWindow, self).__init__(parent)
        loadUi(ui, self)
        self.add.clicked.connect(self.addToDatabase)
        self.cancel.clicked.connect(self.close)

    def close(self):
        self.destroy(True)

    def addToDatabase(self):
        pass
