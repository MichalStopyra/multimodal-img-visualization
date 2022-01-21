from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

from src.data_container.dataContainer import DataContainer
from src.library.libraryApi import standarize_image_channels
from src.ui.available_actions.availableActionsApi import AvailableActionsApi
from src.ui.available_actions.enum.actionTypeEnum import ActionTypeEnum
from src.ui.dialog.abstractDialog.abstractDialog import AbstractDialog


class UiChooseChannelsStandarization(AbstractDialog):

    def __init__(self, data_container: DataContainer):
        super().__init__(data_container)

        self.setupUi()

        self.set_channels_List()

    def setupUi(self):
        self.frameWidget.setObjectName("self.frameWidget")
        self.frameWidget.resize(622, 504)
        self.pushButton = QtWidgets.QPushButton(self.frameWidget)
        self.pushButton.setGeometry(QtCore.QRect(390, 190, 231, 91))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.on_submit())

        self.tableWidget = QtWidgets.QTableWidget(self.frameWidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 381, 501))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)

        self.label = QtWidgets.QLabel(self.frameWidget)
        self.label.setGeometry(QtCore.QRect(410, 40, 171, 91))
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.frameWidget)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.frameWidget.setWindowTitle(_translate("self.frameWidget", "Choose channels for standarization"))
        self.pushButton.setText(_translate("self.frameWidget", "Submit"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("self.frameWidget", "Channel Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("self.frameWidget", "Max Bit Size Standarization"))

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        self.label.setText(_translate("self.frameWidget",
                                      "Firstly check max bit size checkboxes and then select multiple channels"))

    def set_channels_List(self):
        available_channels = AvailableActionsApi.find_channels_available_for_action(
            self.data_container, ActionTypeEnum.STANDARIZE_CHANNELS)

        for index, av_channel in enumerate(available_channels):
            self.tableWidget.insertRow(index)
            self.tableWidget.setItem(index, 0, QtWidgets.QTableWidgetItem(av_channel[0]))

            item = QTableWidgetItem(''.format(index, 1))
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)

            self.tableWidget.setItem(index, 1, item)

    def on_submit(self):
        selected_channels = self.tableWidget.selectedItems()
        if not selected_channels:
            print("Choose cells to standarize!")
            return

        channels_to_exclude = []
        standarization_modes = []

        row_range = self.tableWidget.rowCount()
        for idx in range(row_range):
            channel_name = str(self.tableWidget.item(idx, 0).text())

            item_list = list(filter(lambda selected_ch: selected_ch.data(0) == channel_name, selected_channels))
            if not item_list or len(item_list) != 1:
                channels_to_exclude.append(str(self.tableWidget.item(idx, 0).text()))
            else:
                take_bit_max_value = bool((self.tableWidget.item(idx, 1).checkState() == QtCore.Qt.Checked))
                standarization_modes.append((channel_name, take_bit_max_value))

        standarize_image_channels(self.data_container, channels_to_exclude, standarization_modes)

        self.hide()
