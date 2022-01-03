from PyQt5 import QtCore, QtGui, QtWidgets

from src.data_container.dataContainer import DataContainer


class UiChooseChannelOneStdDialog():

    def __init__(self, data_container: DataContainer):
        self.frameWidget = QtWidgets.QFrame()
        self.setupUi()

        self.data_container = data_container

    def setupUi(self):
        self.frameWidget.setObjectName("self.frameWidget")
        self.frameWidget.resize(622, 504)
        self.pushButton = QtWidgets.QPushButton(self.frameWidget)
        self.pushButton.setGeometry(QtCore.QRect(390, 110, 231, 91))
        self.pushButton.setObjectName("pushButton")
        self.tableWidget = QtWidgets.QTableWidget(self.frameWidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 381, 501))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.frameWidget)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.frameWidget.setWindowTitle(_translate("self.frameWidget", "Choose channel for action"))
        self.pushButton.setText(_translate("self.frameWidget", "Submit"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("self.frameWidget", "New Column"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("self.frameWidget", "Choose Standarized"))

    def show(self):
        self.frameWidget.show()

    def hide(self):
        self.frameWidget.hide()