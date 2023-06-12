from mainWindow import MainWindow
import sys
from PySide6 import QtWidgets
import reviewsToAnalysis
import displayGraph
import makeGraph

app = QtWidgets.QApplication(sys.argv)
mainWindow = QtWidgets.QMainWindow()
ui = MainWindow()
ui.setupUi(mainWindow)
mainWindow.show()
sys.exit(app.exec())
