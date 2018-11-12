from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

from DetailLogWindow import DetailLogWindow


class ViolationItem (QtWidgets.QListWidget):
    def __init__ (self, parent = None):
        super(ViolationItem, self).__init__(parent)
        loadUi("./UI/ViolationItem.ui", self)
        self.carimage.setScaledContents(True)
        self.details_button.clicked.connect(self.showDetails)
        self.data = {}

    def showDetails(self):
        window = DetailLogWindow(self.data, self)
        window.show()

    def setCarId(self, id):
        print(self.carid)
        self.carid.setText(str(id))

    def setRule(self, rule):
        self.rule.setText(rule)

    def setLocation(self, location):
        self.location.setText(location)

    def setTime(self, time):
        self.time.setText(time)

    def setCarImage(self, pixmap):
        self.carimage.setPixmap(pixmap)
        self.carimage.show()

