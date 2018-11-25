from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QMainWindow, QCompleter
from PyQt5.uic import loadUi

from Database import Database


class SearchWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SearchWindow, self).__init__(parent)
        loadUi("UI/Search.ui", self)
        self.color.addItems(Database.getInstance().getCarColorsList())
        completer = QCompleter()
        self.substring.setCompleter(completer)
        model = QStringListModel()
        completer.setModel(model)

        licenseList = Database.getInstance().getLicenseList()

        model.setStringList(licenseList)

