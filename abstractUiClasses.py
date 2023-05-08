from PySide6 import QtCore, QtGui, QtWidgets
from abc import ABC, abstractmethod


class confirmDialog(ABC):
    def __init__(self, text):
        self.text = text

    def setupUi(self, Dialog):
        self.parent = Dialog

        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 100)

        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 381, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")

        self.pushButton_yes = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_yes.setGeometry(QtCore.QRect(80, 60, 75, 24))
        self.pushButton_yes.setObjectName("pushButton_yes")
        self.pushButton_yes.clicked.connect(self.onClick_pushButton_yes)

        self.pushButton_no = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_no.setGeometry(QtCore.QRect(250, 60, 75, 24))
        self.pushButton_no.setObjectName("pushButton_no")
        self.pushButton_no.clicked.connect(self.onClick_pushButton_no)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

        self.label.setText(_translate("Dialog", self.text))

        self.pushButton_yes.setText(_translate("Dialog", "Yes"))
        self.pushButton_no.setText(_translate("Dialog", "No"))

    @abstractmethod
    def onClick_pushButton_no(self):
        self.parent.close()

    @abstractmethod
    def onClick_pushButton_yes(self):
        pass
