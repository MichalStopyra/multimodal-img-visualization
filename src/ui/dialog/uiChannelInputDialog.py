from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog

from src.data_container.channel.channelApi import ChannelApi
from src.data_container.channel.dto.channelInput import ChannelInput
from src.data_container.dataContainer import DataContainer
from src.library.libraryApi import add_channels_to_multimodal_img
from src.ui.dialog.abstractDialog.abstractDialog import AbstractDialog


class UiChannelInputDialog(AbstractDialog):

    def __init__(self, data_container: DataContainer):
        super().__init__(data_container)
        self.setupUi()

        self.source = []
        self.current_first_row_position = 0
        self.three_channels_from_img_source = False
        self.last_ch_indexes = []

    def setupUi(self):
        self.frameWidget.setObjectName("self.frameWidget")
        self.frameWidget.resize(624, 449)
        self.tableWidget_channelInput = QtWidgets.QTableWidget(self.frameWidget)
        self.tableWidget_channelInput.setGeometry(QtCore.QRect(0, 0, 491, 451))
        self.tableWidget_channelInput.setObjectName("tableWidget_channelInput")
        self.tableWidget_channelInput.setColumnCount(3)
        self.tableWidget_channelInput.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_channelInput.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_channelInput.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_channelInput.setHorizontalHeaderItem(2, item)

        self.toolButton = QtWidgets.QToolButton(self.frameWidget)
        self.toolButton.setGeometry(QtCore.QRect(510, 20, 101, 111))
        self.toolButton.setObjectName("toolButton_add_new_channel")
        self.toolButton.clicked.connect(lambda: self.get_file_source())

        self.checkBox_3_channels_from_img = QtWidgets.QCheckBox(self.frameWidget)
        self.checkBox_3_channels_from_img.setGeometry(QtCore.QRect(550, 105, 101, 111))
        self.checkBox_3_channels_from_img.setText("")
        self.checkBox_3_channels_from_img.setObjectName("checkBox_3_channels_from_img")
        self.checkBox_3_channels_from_img.stateChanged.connect(lambda:
                                                               self.on_checkBox_3_channels_from_img())

        self.label_3_channels_from_img = QtWidgets.QLabel(self.frameWidget)
        self.label_3_channels_from_img.setGeometry(QtCore.QRect(505, 165, 111, 71))
        self.label_3_channels_from_img.setWordWrap(True)
        self.label_3_channels_from_img.setObjectName("label_3_channels_from_img")

        self.toolButton_2 = QtWidgets.QToolButton(self.frameWidget)
        self.toolButton_2.setGeometry(QtCore.QRect(510, 310, 101, 81))
        self.toolButton_2.setObjectName("toolButton_submit")
        self.toolButton_2.clicked.connect(lambda: self.on_submit())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.frameWidget)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.frameWidget.setWindowTitle(_translate("self.frameWidget", "Create Multimodal Image"))
        item = self.tableWidget_channelInput.horizontalHeaderItem(0)
        item.setText(_translate("self.frameWidget", "Source"))
        item = self.tableWidget_channelInput.horizontalHeaderItem(1)
        item.setText(_translate("self.frameWidget", "Channel Name"))
        item = self.tableWidget_channelInput.horizontalHeaderItem(2)
        item.setText(_translate("self.frameWidget", "Max Bit Size"))

        header = self.tableWidget_channelInput.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        self.toolButton.setText(_translate("self.frameWidget", "Add channel"))
        self.toolButton_2.setText(_translate("self.frameWidget", "Submit"))

        self.label_3_channels_from_img.setText(_translate("self.frameWidget", "3 channels from one RGB source"))

    def get_file_source(self):
        self.current_first_row_position = self.tableWidget_channelInput.rowCount()

        self.tableWidget_channelInput.insertRow(self.current_first_row_position)

        self.source.append(QFileDialog.getOpenFileName(self.frameWidget, "Open File", "",
                                                       options=QtWidgets.QFileDialog.DontUseNativeDialog)[0])
        current_source_idx = len(self.source) - 1

        self.tableWidget_channelInput.setItem(self.current_first_row_position,
                                              0, QtWidgets.QTableWidgetItem(self.source[current_source_idx]))

        if self.three_channels_from_img_source:
            self.tableWidget_channelInput.insertRow(self.current_first_row_position + 1)
            self.tableWidget_channelInput.insertRow(self.current_first_row_position + 2)

            self.tableWidget_channelInput.setItem(self.current_first_row_position + 1,
                                                  0, QtWidgets.QTableWidgetItem(self.source[current_source_idx]))
            self.tableWidget_channelInput.setItem(self.current_first_row_position + 2,
                                                  0, QtWidgets.QTableWidgetItem(self.source[current_source_idx]))

            self.last_ch_indexes.append(self.current_first_row_position + 2)
        else:
            self.last_ch_indexes.append(self.current_first_row_position)

    def on_submit(self):
        channel_names_and_max_bit_values = []
        source_idx = 0
        for i in range(self.tableWidget_channelInput.rowCount()):
            if not self.tableWidget_channelInput.item(i, 1) or not self.tableWidget_channelInput.item(i, 2):
                print("WARNING - set all necessary values!")
                return

            channel_name = str(self.tableWidget_channelInput.item(i, 1).text())
            channel_max_bit_size = int(str(self.tableWidget_channelInput.item(i, 2).text()))

            if ChannelApi.check_if_channel_name_occupied(self.data_container.get_channels_data_map(), channel_name):
                print("ERROR - Name: ", channel_name, " is already occupied! Chose another one")
                return

            channel_names_and_max_bit_values.append((channel_name, channel_max_bit_size))

            if i in self.last_ch_indexes:
                add_channels_to_multimodal_img(self.data_container,
                                               [ChannelInput(self.source[source_idx],
                                                             channel_names_and_max_bit_values)])
                channel_names_and_max_bit_values = []
                source_idx += 1

        self.hide()

    def on_checkBox_3_channels_from_img(self):
        self.three_channels_from_img_source = self.checkBox_3_channels_from_img.isChecked()
