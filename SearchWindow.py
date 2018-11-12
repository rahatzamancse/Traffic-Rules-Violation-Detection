from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class SearchWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SearchWindow, self).__init__(parent)
        loadUi("UI/Search.ui", self)

