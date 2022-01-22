from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

from src.data_container.dataContainer import DataContainer
from src.library.conversion.enum.conversionTypeEnum import ConversionTypeEnum
from src.library.decomposition.enum.decompositionEnum import DecompositionEnum
from src.library.libraryApi import decompose_channel_resolution_wrapper, convert_channel
from src.ui.available_actions.availableActionsApi import AvailableActionsApi
from src.ui.available_actions.enum.actionTypeEnum import ActionTypeEnum
from src.ui.dialog.abstractDialog.abstractDialog import AbstractDialog


class uiChooseChannelConversion(AbstractDialog):

    def __init__(self, data_container: DataContainer):
        super().__init__(data_container)
        self.fast_ica_n_components = None

        self.setupUi()

        self.set_channels_List()

    def setupUi(self):
        self.frameWidget.setObjectName("self.frameWidget")
        self.frameWidget.resize(622, 504)

        self.pushButton = QtWidgets.QPushButton(self.frameWidget)
        self.pushButton.setGeometry(QtCore.QRect(390, 110, 231, 91))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.on_submit())

        self.tableWidget = QtWidgets.QTableWidget(self.frameWidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 381, 501))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)

        self.comboBox_conversion_type = QtWidgets.QComboBox(self.frameWidget)
        self.comboBox_conversion_type.setGeometry(QtCore.QRect(440, 250, 141, 51))
        self.comboBox_conversion_type.setObjectName("comboBox_conversion_type")
        self.comboBox_conversion_type.addItem("")
        self.comboBox_conversion_type.addItem("")
        self.comboBox_conversion_type.addItem("")
        self.comboBox_conversion_type.currentTextChanged.connect(lambda: self.set_channels_List())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.frameWidget)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.frameWidget.setWindowTitle(_translate("self.frameWidget", "Choose channel for conversion"))
        self.pushButton.setText(_translate("self.frameWidget", "Submit"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("self.frameWidget", "Channel name"))

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)

        self.comboBox_conversion_type.setItemText(0, _translate("uiChooseChannelConversion", "INTENSITY"))
        self.comboBox_conversion_type.setItemText(1, _translate("uiChooseChannelConversion", "DOLP"))
        self.comboBox_conversion_type.setItemText(2, _translate("uiChooseChannelConversion", "AOLP"))

    def set_channels_List(self):
        self.tableWidget.setRowCount(0)
        chosen_conversion_type = ConversionTypeEnum[str(self.comboBox_conversion_type.currentText())]

        available_channels = AvailableActionsApi.find_channels_available_for_action(
            self.data_container, ActionTypeEnum.CONVERT_CHANNEL, None, chosen_conversion_type)

        for index, av_channel in enumerate(available_channels):
            self.tableWidget.insertRow(index)
            self.tableWidget.setItem(index, 0, QtWidgets.QTableWidgetItem(av_channel[0]))

    def on_submit(self):
        current_cell_row = self.tableWidget.currentRow()
        if current_cell_row == -1:
            print("Choose cell for action!")
            return

        channel_name = str(self.tableWidget.item(current_cell_row, 0).text())

        chosen_conversion_type = ConversionTypeEnum[str(self.comboBox_conversion_type.currentText())]

        convert_channel(self.data_container, channel_name, chosen_conversion_type)

        self.hide()
