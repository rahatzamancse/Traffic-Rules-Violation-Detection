from Database import Database
from add_windows.AddMainWindow import AddMainWindow


class AddRule(AddMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent, "UI/AddRule.ui")

    def addToDatabase(self):
        rule = str(self.rule.text())
        fine = str(self.fine.text())
        Database.get_instance().insert_into_rules(rule, fine)
        self.destroy()
