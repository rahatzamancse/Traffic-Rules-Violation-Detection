from PyQt5.QtWidgets import QFileDialog

from Database import Database
from add_windows.AddMainWindow import AddMainWindow


class AddCar(AddMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent, "UI/AddCar.ui")
        self.license_browse.clicked.connect(lambda: self.getFile(self.license_img))
        self.car_browse.clicked.connect(lambda: self.getFile(self.car_img))

    def addToDatabase(self):
        color = str(self.color.text())
        lic_num = str(self.license_num.text())
        lic_img = str(self.license_img.text())
        car_img = str(self.car_img.text())
        owner = str(self.owner.text())
        Database.getInstance().insertIntoCars(color, lic_num, lic_img, car_img, owner)
        self.destroy()

    def getFile(self, lineEdit):
        lineEdit.setText(QFileDialog.getOpenFileName()[0])
