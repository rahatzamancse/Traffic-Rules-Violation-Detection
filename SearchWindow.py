from PyQt5 import QtWidgets
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QMainWindow, QCompleter
from PyQt5.uic import loadUi

from Database import Database
from ViolationItem import ViolationItem


class SearchWindow(QMainWindow):
    def __init__(self, search_result, parent=None):
        super(SearchWindow, self).__init__(parent)
        loadUi("UI/Search.ui", self)

        self.search_result = search_result

        self.color.addItems(["None"])
        self.color.addItems(Database.get_instance().get_car_color_list())

        completer = QCompleter()
        self.substring.setCompleter(completer)
        model = QStringListModel()
        completer.setModel(model)
        licenseList = Database.get_instance().get_licenses()
        model.setStringList(licenseList)

        self.search_button.clicked.connect(self.search)

        cams = Database.get_instance().get_cam_list(None)
        self.camera.clear()
        self.camera.addItems(["None"])
        self.camera.addItems(id for id, cam, feed in cams)
        self.camera.setCurrentIndex(0)

    def search(self):
        cam = None if self.camera.currentText() == "None" else self.camera.currentText()
        color = None if self.color.currentText() == "None" else self.color.currentText()
        license = None if self.substring.text() == "" else self.substring.text()
        time = None if self.use_time.isChecked() is False else (self.from_time.dateTime().toMSecsSinceEpoch(), self.to_time.dateTime().toMSecsSinceEpoch())
        rows = Database.get_instance().search(cam=cam, color=color, license=license, time=time)
        for row in rows:
            print(row)
            listWidget = ViolationItem()
            listWidget.setData(row)
            listWidgetItem = QtWidgets.QListWidgetItem(self.search_result)
            listWidgetItem.setSizeHint(listWidget.sizeHint())
            self.search_result.addItem(listWidgetItem)
            self.search_result.setItemWidget(listWidgetItem, listWidget)
        self.destroy()
