import sys
from PyQt6 import QtWidgets, uic
from ui import MainWindow

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec())
