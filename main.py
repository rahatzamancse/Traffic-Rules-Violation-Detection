import sys
# import qdarkstyle
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
