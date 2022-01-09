from PyQt5 import QtCore, QtWidgets

from src.data_container.dataContainer import DataContainer
from src.ui.dialog.abstractDialog.abstractDialog import AbstractDialog


class UiChooseChannelsDecomposeWholeImg(AbstractDialog):

    def __init__(self, data_container: DataContainer):
        super().__init__()
        self.data_container = data_container

        self.setupUi()

    def setupUi(self):
        self.frameWidget.setObjectName("self.frameWidget")
        self.frameWidget.resize(622, 504)
        self.pushButton_submit = QtWidgets.QPushButton(self.frameWidget)
        self.pushButton_submit.setGeometry(QtCore.QRect(390, 110, 231, 91))
        self.pushButton_submit.setObjectName("pushButton_submit")
        self.tableWidget_channels = QtWidgets.QTableWidget(self.frameWidget)
        self.tableWidget_channels.setGeometry(QtCore.QRect(0, 0, 381, 501))
        self.tableWidget_channels.setObjectName("tableWidget_channels")
        self.tableWidget_channels.setColumnCount(2)
        self.tableWidget_channels.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_channels.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_channels.setHorizontalHeaderItem(1, item)
        self.comboBox_decomposition_type = QtWidgets.QComboBox(self.frameWidget)
        self.comboBox_decomposition_type.setGeometry(QtCore.QRect(420, 250, 141, 51))
        self.comboBox_decomposition_type.setObjectName("comboBox_decomposition_type")
        self.comboBox_decomposition_type.addItem("")
        self.comboBox_decomposition_type.addItem("")
        self.comboBox_decomposition_type.addItem("")
        self.label = QtWidgets.QLabel(self.frameWidget)
        self.label.setGeometry(QtCore.QRect(400, 350, 171, 17))
        self.label.setObjectName("label")
        self.textEdit_ica_n_components = QtWidgets.QTextEdit(self.frameWidget)
        self.textEdit_ica_n_components.setGeometry(QtCore.QRect(400, 370, 161, 31))
        self.textEdit_ica_n_components.setObjectName("textEdit_ica_n_components")
        self.label_2 = QtWidgets.QLabel(self.frameWidget)
        self.label_2.setGeometry(QtCore.QRect(410, 20, 171, 71))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.frameWidget)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.frameWidget.setWindowTitle(
            _translate("self.frameWidget", "Choose channels for whole image decomposition"))
        self.pushButton_submit.setText(_translate("self.frameWidget", "Submit"))
        item = self.tableWidget_channels.horizontalHeaderItem(0)
        item.setText(_translate("self.frameWidget", "Channel Name"))
        item = self.tableWidget_channels.horizontalHeaderItem(1)
        item.setText(_translate("self.frameWidget", "Choose Standarized"))
        self.comboBox_decomposition_type.setItemText(0, _translate("self.frameWidget", "PCA"))
        self.comboBox_decomposition_type.setItemText(1, _translate("self.frameWidget", "FAST ICA"))
        self.comboBox_decomposition_type.setItemText(2, _translate("self.frameWidget", "NMF"))
        self.label.setText(_translate("self.frameWidget", "FAST ICA n_components"))
        self.label_2.setText(_translate("self.frameWidget",
                                        "Firstly check choose std checkboxes, then choose multiple channels"))
