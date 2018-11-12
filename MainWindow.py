from time import localtime, asctime

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QComboBox, QListWidget, QFormLayout, QVBoxLayout
from PyQt5.uic import loadUi
import sqlite3 as lite

from Database import Database, KEYS
from ViolationItem import ViolationItem


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("./UI/MainWindow.ui", self)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Welcome")

        self.search_button.clicked.connect(self.search)
        self.clear_button.clicked.connect(self.clear)

        self.cam_selector.clear()
        self.cam_selector.addItems([
            "1",
            "2",
            "3"
        ])
        self.cam_selector.setCurrentIndex(0)
        self.cam_selector.currentIndexChanged.connect(self.camChanged)

        violation_list = QListWidget(self)
        self.log_tabwidget.addTab(violation_list, "Violations")

        # Database
        self.database = Database.getInstance()
        rows = self.database.getViolationsFromCam(str(self.cam_selector.currentText()))

        for row in rows:
            print(row)
            listWidget = ViolationItem()
            listWidget.data = row
            listWidget.setCarId(row[KEYS.CARID])
            listWidget.setTime(asctime(localtime(row[KEYS.TIME])))
            listWidget.setRule(row[KEYS.RULENAME])
            listWidget.setCarImage(row[KEYS.CARIMAGE])
            listWidgetItem = QtWidgets.QListWidgetItem(violation_list)
            listWidgetItem.setSizeHint(listWidget.sizeHint())
            violation_list.addItem(listWidgetItem)
            violation_list.setItemWidget(listWidgetItem, listWidget)

    @QtCore.pyqtSlot()
    def search(self):
        from SearchWindow import SearchWindow
        searchWindow = SearchWindow(self)
        searchWindow.show()

    @QtCore.pyqtSlot()
    def clear(self):
        pass

    @QtCore.pyqtSlot()
    def camChanged(self):
        pass
