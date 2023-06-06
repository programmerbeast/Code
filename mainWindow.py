# Form implementation generated from reading ui file '.\untitled.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets
from reviews_to_analysis2v1 import driver_reviews
from uiDialog import NewAppDialog, ChangeAppDialog
from crawler import driverCrawler
import subprocess
import threading
import os
import sys
k=-1


command = ["python", "app2.py"]


class MainWindow(object):
    def __init__(self):
        # List of Dict(appName, appId)
        self.appList = []
        self.thread = None

    def setupUi(self, MainWindow):
        # Ui setup
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        MainWindow.setMaximumSize(QtCore.QSize(640, 480))

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_companyName = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_companyName.setGeometry(QtCore.QRect(160, 20, 451, 61))

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(35)

        self.label_companyName.setFont(font)
        self.label_companyName.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_companyName.setObjectName("label_companyName")

        self.graphicsView = QtWidgets.QGraphicsView(parent=self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(150, 20, 61, 61))

        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        self.graphicsView.setBackgroundBrush(brush)
        self.graphicsView.setObjectName("graphicsView")

        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(380, 110, 231, 271))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.pushButton_newApp = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton_newApp.setObjectName("pushButton_newApp")
        self.pushButton_newApp.clicked.connect(self.onClick_pushButton_newApp)
        self.verticalLayout.addWidget(self.pushButton_newApp)

        self.pushButton_runCrawler = QtWidgets.QPushButton(
            parent=self.verticalLayoutWidget
        )
        self.pushButton_runCrawler.setObjectName("pushButton_runCrawler")
        self.pushButton_runCrawler.clicked.connect(self.onClick_pushButton_runCrawler)
        self.verticalLayout.addWidget(self.pushButton_runCrawler)

        self.pushButton_displayGraph = QtWidgets.QPushButton(
            parent=self.verticalLayoutWidget
        )
        self.pushButton_displayGraph.setObjectName("pushButton_displayGraph")
        self.pushButton_displayGraph.clicked.connect(
            self.onClick_pushButton_displayGraph
        )
        self.verticalLayout.addWidget(self.pushButton_displayGraph)

        self.pushButton_quit = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton_quit.setObjectName("btn_Quit")
        self.pushButton_quit.clicked.connect(self.onClick_pushButton_quit)
        self.verticalLayout.addWidget(self.pushButton_quit)

        self.listWidget = QtWidgets.QListWidget(parent=self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(30, 140, 281, 211))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.itemActivated.connect(self.onActivation_listWidget)

        self.label_footer = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_footer.setGeometry(QtCore.QRect(0, 420, 631, 16))
        self.label_footer.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.label_footer.setObjectName("label_footer")
        MainWindow.setCentralWidget(self.centralwidget)

        # Test
        self.appList.append(
            {
                "appName": "Twitter",
                "appId": "com.twitter.android",
            }
        )
        self.appList.append(
            {
                "appName": "Instagram",
                "appId": "com.instagram.android",
            }
        )
        self.appList.append(
            {
                "appName": "Facebook",
                "appId": "com.facebook.katana",
            }
        )
        self.appList.append(
            {
                "appName": "LinkedIn",
                "appId": "com.linkedin.android",
            }
        )

        self.updateListWidget()

        self.retranslateUi(MainWindow)
        self.listWidget.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_companyName.setText(_translate("MainWindow", "Company Name"))
        self.pushButton_newApp.setText(_translate("MainWindow", "Add new app"))
        self.pushButton_runCrawler.setText(_translate("MainWindow", "Run Crawler"))
        self.pushButton_displayGraph.setText(_translate("MainWindow", "Display graph"))
        self.pushButton_quit.setText(_translate("MainWindow", "Quit"))
        self.label_footer.setText(
            _translate("MainWindow", "A property of Chaos, Badr and Mohommad.")
        )

    def updateListWidget(self):
        self.listWidget.clear()
        for element in self.appList:
            self.listWidget.addItem(element["appName"])

    def onClick_pushButton_newApp(self):
        dialog_newApp = QtWidgets.QDialog()
        obj_newApp = NewAppDialog(self.appList)
        obj_newApp.setupUi(dialog_newApp)
        dialog_newApp.exec()
        self.updateListWidget()

    def onClick_pushButton_runCrawler(self):
        for element in self.appList:
            appName = element["appName"]
            appId = element["appId"]
            driverCrawler(
                appName, appId, epochs=100
            )  # change the epochs to incerease number of reviews

    def onClick_pushButton_displayGraph(self):
        # Create a new thread and run the command in it
    
        



        selected_item = self.listWidget.currentItem()
        if selected_item is not None:
            global k
            k+=1
            app_name = selected_item.text()
            print(app_name)
            #df_reviews=driver_reviews(app_name)
            #output_file = os.path.join("saved_dataframes", "reviews.csv")
            #f_reviews.to_csv(output_file, index=False)
            print("aaa")
            print(self.thread)
           # if self.thread and self.thread.is_alive():
           #     self.thread.join()
            print("vdfg")

    
            self.thread = threading.Thread(target=run_command, args=(command, app_name,k))
            self.thread.start()
        # stdout=subprocess.PIPE, stderr=subprocess.PIPE
        # Wait for the process to finish and get the output

        # Decode the output and error messages
        # output = output.decode('utf-8')
        # error = error.decode('utf-8')

        # Print the output and error messages

    # print("Output:")
    # print(output)
    # print("Error:")
    # print(error)
    # display_graph("Linkedin")

    def onClick_pushButton_quit(self):
        sys.exit()

    def onActivation_listWidget(self, item):
        appName = item.text()
        for i in range(len(self.appList)):
            if self.appList[i]["appName"] == appName:
                break
        dialog_listEditDelete = QtWidgets.QDialog()
        obj_listEditDelete = ChangeAppDialog(self.appList, i)
        obj_listEditDelete.setupUi(dialog_listEditDelete)
        dialog_listEditDelete.exec()
        self.updateListWidget()


def run_command(command,arg1,arg2):
    command2=command + [arg1] + [str(arg2)]
    process = subprocess.Popen(command2)
    process.communicate()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec())
