from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QListWidget
from PyQt5.uic import loadUi

from Database import Database
from ViolationItem import ViolationItem


class ArchiveWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ArchiveWindow, self).__init__(parent)
        loadUi('UI/Archive.ui', self)

        self.cancel.clicked.connect(self.close)

        self.log_tabwidget.clear()
        self.violation_list = QListWidget(self)
        self.log_tabwidget.addTab(self.violation_list, "Violations")
        self.violation_list.clear()
        rows = Database.getInstance().getViolationsFromCam(None, cleared=True)
        for row in rows:
            listWidget = ViolationItem()
            listWidget.setData(row)
            listWidgetItem = QtWidgets.QListWidgetItem(self.violation_list)
            listWidgetItem.setSizeHint(listWidget.sizeHint())
            self.violation_list.addItem(listWidgetItem)
            self.violation_list.setItemWidget(listWidgetItem, listWidget)


    def close(self):
        self.destroy(True)
