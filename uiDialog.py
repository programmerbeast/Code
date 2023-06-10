# Form implementation generated from reading ui file '.\NewAppDialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets
from abstractUiClasses import confirmDialog
import sys
from PySide6.QtCore import (
    QCoreApplication,
    QMetaObject,
    QRect,
    Qt,
    QDateTime,
    QDate,
    QTime,
)
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QWidget,
    QDateEdit,
    QSpinBox,
)
import sys
from datetime import datetime
from crawler import driverCrawler


class NewAppDialog(object):
    def __init__(self, appList):
        self.appList = appList

    def setupUi(self, Dialog):
        self.parent = Dialog

        Dialog.setObjectName("Dialog")
        Dialog.resize(420, 134)

        self.formLayoutWidget = QtWidgets.QWidget(parent=Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 30, 381, 61))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        self.label_appName = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.label_appName.setObjectName("label_appName")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_appName
        )

        self.lineEdit_appName = QtWidgets.QLineEdit(parent=self.formLayoutWidget)
        self.lineEdit_appName.setObjectName("lineEdit_appName")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEdit_appName
        )

        self.label_appId = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.label_appId.setObjectName("label_appId")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_appId
        )

        self.lineEdit_appId = QtWidgets.QLineEdit(parent=self.formLayoutWidget)
        self.lineEdit_appId.setObjectName("lineEdit_appId")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEdit_appId
        )

        self.pushButton_ok = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_ok.setGeometry(QtCore.QRect(240, 100, 75, 24))
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.pushButton_ok.clicked.connect(self.onClick_pushButton_ok)

        self.pushButton_cancel = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_cancel.setGeometry(QtCore.QRect(320, 100, 75, 24))
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.pushButton_cancel.clicked.connect(self.onClick_pushButton_cancel)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

        self.label_appName.setText(_translate("Dialog", "App Name :"))
        self.label_appId.setText(_translate("Dialog", "App Id :"))

        self.pushButton_ok.setText(_translate("Dialog", "Ok"))
        self.pushButton_cancel.setText(_translate("Dialog", "Cancel"))

    def onClick_pushButton_ok(self):
        if self.lineEdit_appName.text() == "" or self.lineEdit_appId.text() == "":
            popup = QtWidgets.QDialog()
            layout = QtWidgets.QVBoxLayout()
            message = QtWidgets.QLabel("Please make sure both fields are filled.")
            layout.addWidget(message)
            popup.setLayout(layout)
            popup.exec()
        else:
            self.appList.append(
                {
                    "appName": self.lineEdit_appName.text(),
                    "appId": self.lineEdit_appId.text(),
                }
            )
            self.parent.close()

    def onClick_pushButton_cancel(self):
        self.parent.close()


class ChangeAppDialog(object):
    def __init__(self, appList, itemIndex):
        self.appList = appList
        self.itemIndex = itemIndex

    def setupUi(self, Dialog):
        self.parent = Dialog

        Dialog.setObjectName("Dialog")
        Dialog.resize(420, 134)

        self.formLayoutWidget = QtWidgets.QWidget(parent=Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 30, 381, 61))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        self.label_appName = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.label_appName.setObjectName("label_appName")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_appName
        )

        self.lineEdit_appName = QtWidgets.QLineEdit(parent=self.formLayoutWidget)
        self.lineEdit_appName.setObjectName("lineEdit_appName")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEdit_appName
        )
        self.lineEdit_appName.setText(self.appList[self.itemIndex]["appName"])

        self.label_appId = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.label_appId.setObjectName("label_appId")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_appId
        )

        self.lineEdit_appId = QtWidgets.QLineEdit(parent=self.formLayoutWidget)
        self.lineEdit_appId.setObjectName("lineEdit_appId")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lineEdit_appId
        )
        self.lineEdit_appId.setText(self.appList[self.itemIndex]["appId"])

        self.pushButton_deleteApp = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_deleteApp.setGeometry(QtCore.QRect(20, 100, 75, 24))
        self.pushButton_deleteApp.setObjectName("pushButton")
        self.pushButton_deleteApp.clicked.connect(self.onClick_pushButton_deleteApp)

        self.pushButton_save = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_save.setGeometry(QtCore.QRect(240, 100, 75, 24))
        self.pushButton_save.setObjectName("pushButton_ok")
        self.pushButton_save.clicked.connect(self.onClick_pushButton_save)

        self.pushButton_cancel = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_cancel.setGeometry(QtCore.QRect(320, 100, 75, 24))
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.pushButton_cancel.clicked.connect(self.onClick_pushButton_cancel)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

        self.label_appName.setText(_translate("Dialog", "App Name :"))
        self.label_appId.setText(_translate("Dialog", "App Id :"))

        self.pushButton_deleteApp.setText(_translate("Dialog", "Delete App"))
        self.pushButton_save.setText(_translate("Dialog", "Save"))
        self.pushButton_cancel.setText(_translate("Dialog", "Cancel"))

    def onClick_pushButton_deleteApp(self):
        dialog_confirmDelete = QtWidgets.QDialog()
        obj_confirmDelete = ConfirmDelete(
            "Are you sure you want to delete this app?",
            self.appList,
            self.itemIndex,
            self.parent,
        )
        obj_confirmDelete.setupUi(dialog_confirmDelete)
        dialog_confirmDelete.exec()

    def onClick_pushButton_save(self):
        if (
            self.lineEdit_appName.text() != self.appList[self.itemIndex]["appName"]
            or self.lineEdit_appId.text() != self.appList[self.itemIndex]["appId"]
        ):
            self.appList[self.itemIndex]["appName"] = self.lineEdit_appName.text()
            self.appList[self.itemIndex]["appId"] = self.lineEdit_appId.text()
        self.parent.close()

    def onClick_pushButton_cancel(self):
        if (
            self.lineEdit_appName.text() != self.appList[self.itemIndex]["appName"]
            or self.lineEdit_appId.text() != self.appList[self.itemIndex]["appId"]
        ):
            dialog_confirmDiscardChange = QtWidgets.QDialog()
            obj_confirmDiscardChange = ConfirmDiscardChange(
                "App has unsaved changes. \nDo you want to discard changes?",
                self.parent,
            )
            obj_confirmDiscardChange.setupUi(dialog_confirmDiscardChange)
            dialog_confirmDiscardChange.exec()
        else:
            self.parent.close()


class ConfirmDelete(confirmDialog):
    def __init__(self, text, appList, itemIndex, editDeleteDialog):
        super().__init__(text)
        self.appList = appList
        self.itemIndex = itemIndex
        self.parentDialog = editDeleteDialog

    def onClick_pushButton_no(self):
        return super().onClick_pushButton_no()

    def onClick_pushButton_yes(self):
        self.appList.pop(self.itemIndex)
        self.parent.close()
        self.parentDialog.close()


class ConfirmDiscardChange(confirmDialog):
    def __init__(self, text, editDeleteDialog):
        super().__init__(text)
        self.parentDialog = editDeleteDialog

    def onClick_pushButton_no(self):
        return super().onClick_pushButton_no()

    def onClick_pushButton_yes(self):
        self.parent.close()
        self.parentDialog.close()


class ShowTextDialog(object):
    def __init__(self, text, alignH="c", fontSize=15):
        self.text = text
        self.alignH = alignH
        self.fontSize = fontSize

    def setupUi(self, Dialog):
        self.parent = Dialog
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(311, 100)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.label.setGeometry(QtCore.QRect(20, 10, 281, 71))
        font = QtGui.QFont()
        font.setPointSize(self.fontSize)
        self.label.setFont(font)
        match self.alignH:
            case "c":
                self.label.setAlignment(QtCore.Qt.AlignCenter)
            case "l":
                self.label.setAlignment(QtCore.Qt.AlignLeft)
            case "r":
                self.label.setAlignment(QtCore.Qt.AlignRight)

        self.retranslateUi(Dialog)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(
            QtCore.QCoreApplication.translate("Dialog", "Dialog", None)
        )
        self.label.setText(QtCore.QCoreApplication.translate("Dialog", self.text, None))

    def updateText(self, newText):
        self.text = newText
        self.label.setText(newText)


class SelectStartDateDialog(object):
    def __init__(self, parentDialog, appName, appId) -> None:
        super().__init__()
        self.parentDialog = parentDialog
        self.appName = appName
        self.appId = appId

    def setupUi(self, Dialog):
        self.parent = Dialog
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(247, 100)
        self.horizontalLayoutWidget = QWidget(Dialog)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(20, 10, 211, 61))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")

        self.horizontalLayout.addWidget(self.label)

        self.dateEdit_startDate = QDateEdit(self.horizontalLayoutWidget)
        self.dateEdit_startDate.setObjectName("dateEdit")
        self.dateEdit_startDate.setDateTime(
            QDateTime(QDate(2020, 1, 1), QTime(0, 0, 0))
        )
        self.dateEdit_startDate.setCalendarPopup(True)

        self.horizontalLayout.addWidget(self.dateEdit_startDate)

        self.pushButton_select = QPushButton(Dialog)
        self.pushButton_select.setObjectName("pushButton")
        self.pushButton_select.setGeometry(QRect(80, 70, 75, 24))
        self.pushButton_select.clicked.connect(self.onClick_pushButton_select)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "Dialog", None))
        self.label.setText(
            QCoreApplication.translate("Dialog", "Select Start Date:", None)
        )
        self.pushButton_select.setText(
            QCoreApplication.translate("Dialog", "Select", None)
        )

    def onClick_pushButton_select(self):
        startDate = datetime.strptime(self.dateEdit_startDate.text(), "%d-%m-%Y")
        print(f"Crawling till : {startDate}")
        driverCrawler(self.appName, self.appId, start_date=startDate)
        self.parentDialog.close()
        self.parent.close()


class SelectNumReviewsDialog(object):
    def __init__(self, parentDialog, appName, appId) -> None:
        super().__init__()
        self.parentDialog = parentDialog
        self.appName = appName
        self.appId = appId

    def setupUi(self, Dialog):
        self.parent = Dialog
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(311, 100)
        self.horizontalLayoutWidget = QWidget(Dialog)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 10, 301, 61))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")

        self.horizontalLayout.addWidget(self.label)

        self.spinBox = QSpinBox(self.horizontalLayoutWidget)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.spinBox.setMaximum(999999999)
        self.spinBox.setValue(10000)

        self.horizontalLayout.addWidget(self.spinBox)

        self.pushButton_select = QPushButton(Dialog)
        self.pushButton_select.setObjectName("pushButton")
        self.pushButton_select.setGeometry(QRect(120, 70, 75, 24))
        self.pushButton_select.clicked.connect(self.onClick_pushButton_select)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "Dialog", None))
        self.label.setText(
            QCoreApplication.translate("Dialog", "Select Number of Reviews:", None)
        )
        self.pushButton_select.setText(
            QCoreApplication.translate("Dialog", "Select", None)
        )

    def onClick_pushButton_select(self):
        numReviews = int(self.spinBox.text())
        if numReviews > 1000 and numReviews % 1000 == 0:
            batch_size = 1000
        elif numReviews > 100:
            batch_size = 100
        else:
            batch_size = 1

        epochs = numReviews // batch_size
        print(f"Crawling till : {numReviews} reviews")
        driverCrawler(self.appName, self.appId, epochs=epochs, batch_size=batch_size)
        self.parentDialog.close()
        self.parent.close()


class RunCrawlerDialog(object):
    def __init__(self, appName, appId) -> None:
        self.appName = appName
        self.appId = appId

    def setupUi(self, Dialog):
        self.parent = Dialog
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(400, 175)
        self.label_main = QLabel(Dialog)
        self.label_main.setObjectName("label")
        self.label_main.setGeometry(QRect(30, 30, 321, 31))
        font = QFont()
        font.setPointSize(15)
        font.setBold(False)
        self.label_main.setFont(font)
        self.label_main.setAlignment(Qt.AlignCenter)
        self.horizontalLayoutWidget = QWidget(Dialog)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(20, 60, 352, 80))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.radioButton_num_of_reviews = QRadioButton(self.horizontalLayoutWidget)
        self.radioButton_num_of_reviews.setObjectName("radioButton")
        self.radioButton_num_of_reviews.setEnabled(True)
        self.radioButton_num_of_reviews.setChecked(True)

        self.horizontalLayout.addWidget(self.radioButton_num_of_reviews)

        self.radioButton_start_date_reviews = QRadioButton(self.horizontalLayoutWidget)
        self.radioButton_start_date_reviews.setObjectName("radioButton_2")

        self.horizontalLayout.addWidget(self.radioButton_start_date_reviews)

        self.pushButton_select = QPushButton(Dialog)
        self.pushButton_select.setObjectName("pushButton")
        self.pushButton_select.setGeometry(QRect(310, 140, 75, 24))
        self.pushButton_select.clicked.connect(self.onClick_pushButton_select)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "Dialog", None))
        self.label_main.setText(
            QCoreApplication.translate("Dialog", "Select method of crawling...", None)
        )
        self.radioButton_num_of_reviews.setText(
            QCoreApplication.translate("Dialog", "Crawl by number of review", None)
        )
        self.radioButton_start_date_reviews.setText(
            QCoreApplication.translate("Dialog", "Crawl by start date of reviews", None)
        )
        self.pushButton_select.setText(
            QCoreApplication.translate("Dialog", "Select", None)
        )

    # retranslateUi

    def onClick_pushButton_select(self):
        dialog_showText = QtWidgets.QDialog()
        if self.radioButton_num_of_reviews.isChecked():
            obj_showText = SelectNumReviewsDialog(self.parent, self.appName, self.appId)
        else:
            obj_showText = SelectStartDateDialog(self.parent, self.appName, self.appId)
        obj_showText.setupUi(dialog_showText)
        dialog_showText.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = RunCrawlerDialog("blah", "blah")
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec())
