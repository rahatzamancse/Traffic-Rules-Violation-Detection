from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QListWidget
from PyQt5.uic import loadUi

from Database import Database
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
        self.refresh_button.clicked.connect(self.refresh)

        self.database = Database.getInstance()

        cams = self.database.getCamList()
        self.cam_selector.clear()
        self.cam_selector.addItems(name for name, location in cams)
        self.cam_selector.setCurrentIndex(0)
        self.cam_selector.currentIndexChanged.connect(self.camChanged)

        self.updateCamInfo()

        self.updateLog()

    def updateSearch(self):
        pass

    def updateCamInfo(self):
        count, location = self.database.getCamViolationsCount(self.cam_selector.currentText())
        self.cam_id.setText(self.cam_selector.currentText())
        self.address.setText(location)
        self.total_records.setText(str(count))

    def updateLog(self):
        self.log_tabwidget.clear()
        violation_list = QListWidget(self)
        self.log_tabwidget.addTab(violation_list, "Violations")
        rows = self.database.getUnclearedViolationsFromCam(str(self.cam_selector.currentText()))
        for row in rows:
            print(row)
            listWidget = ViolationItem()
            listWidget.setData(row)
            listWidgetItem = QtWidgets.QListWidgetItem(violation_list)
            listWidgetItem.setSizeHint(listWidget.sizeHint())
            violation_list.addItem(listWidgetItem)
            violation_list.setItemWidget(listWidgetItem, listWidget)

    @QtCore.pyqtSlot()
    def refresh(self):
        self.updateCamInfo()
        self.updateLog()


    @QtCore.pyqtSlot()
    def search(self):
        from SearchWindow import SearchWindow
        searchWindow = SearchWindow(self, self.updateSearch)
        searchWindow.show()

    @QtCore.pyqtSlot()
    def clear(self):
        qm = QtWidgets.QMessageBox
        prompt = qm.question(self, '', "Are you sure to reset all the values?", qm.Yes | qm.No)
        if prompt == qm.Yes:
            self.database.clearCamLog()
            self.updateLog()
        else:
            pass

    @QtCore.pyqtSlot()
    def camChanged(self):
        self.updateCamInfo()
        self.updateLog()
