from Database import Database
from add_windows.AddMainWindow import AddMainWindow


class AddViolation(AddMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent, "UI/AddViolation.ui")

    def addToDatabase(self):
        camera = str(self.camera.text())
        car = str(self.car.text())
        rule = str(self.rule.text())
        time = self.time.dateTime()
        Database.get_instance().insert_into_violations(camera, car, rule, time)
        self.destroy()
