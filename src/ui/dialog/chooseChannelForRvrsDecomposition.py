from PyQt5 import QtCore, QtGui, QtWidgets

from src.data_container.dataContainer import DataContainer


class UiQFrame_rvrs_decomposition():

    def __init__(self, data_container: DataContainer):
        self.frameWidget = QtWidgets.QFrame()
        self.data_container = data_container

        self.setupUi()

    def setupUi(self):
        self.frameWidget.setObjectName("self.frameWidget")
        self.frameWidget.resize(622, 504)
        self.pushButton_submit = QtWidgets.QPushButton(self.frameWidget)
        self.pushButton_submit.setGeometry(QtCore.QRect(390, 190, 231, 91))
        self.pushButton_submit.setObjectName("pushButton_submit")
        self.tableWidget_channels = QtWidgets.QTableWidget(self.frameWidget)
        self.tableWidget_channels.setGeometry(QtCore.QRect(0, 0, 381, 501))
        self.tableWidget_channels.setObjectName("tableWidget_channels")
        self.tableWidget_channels.setColumnCount(1)
        self.tableWidget_channels.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_channels.setHorizontalHeaderItem(0, item)
        self.label_instruction = QtWidgets.QLabel(self.frameWidget)
        self.label_instruction.setGeometry(QtCore.QRect(410, 40, 171, 91))
        self.label_instruction.setWordWrap(True)
        self.label_instruction.setObjectName("label_instruction")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.frameWidget)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.frameWidget.setWindowTitle(_translate("self.frameWidget", "Choose channel for rvrs decomposition"))
        self.pushButton_submit.setText(_translate("self.frameWidget", "Submit"))
        item = self.tableWidget_channels.horizontalHeaderItem(0)
        item.setText(_translate("self.frameWidget", "Channel Name"))
        self.label_instruction.setText(_translate("self.frameWidget", "Choose one channel"))
