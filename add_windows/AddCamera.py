from PyQt5.QtWidgets import QFileDialog

from Database import Database
from add_windows.AddMainWindow import AddMainWindow


class AddCamera(AddMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent, "UI/AddCamera.ui")
        self.file_browse.clicked.connect(lambda: self.getFile(self.file))

    def addToDatabase(self):
        id = str(self.id.text())
        group = str(self.group.text())
        location = str(self.location.text())
        x = str(self.x_coord.text())
        y = str(self.y_coord.text())
        file = str(self.file.text())
        Database.getInstance().insertIntoCamera(id, location, x, y, group, file)
        self.destroy()

    def getFile(self, lineEdit):
        lineEdit.setText(QFileDialog.getOpenFileName()[0])
