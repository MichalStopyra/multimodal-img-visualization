import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QFileDialog

from src.data_container.channel.channelApi import ChannelApi
from src.data_container.channel.dto.channelInput import ChannelInput
from src.data_container.dataContainer import DataContainer
from src.library.libraryApi import load_new_multimodal_image_from_input, add_channels_to_multimodal_img


class UiChannelInputDialog():

    def __init__(self, data_container: DataContainer):
        self.frameWidget = QtWidgets.QFrame()
        self.setupUi()

        self.data_container = data_container
        self.source = ""
        self.current_first_row_position = 0

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

        self.toolButton_3 = QtWidgets.QToolButton(self.frameWidget)
        self.toolButton_3.setGeometry(QtCore.QRect(510, 170, 101, 41))
        self.toolButton_3.setObjectName("toolButton_edit")

        self.toolButton_4 = QtWidgets.QToolButton(self.frameWidget)
        self.toolButton_4.setGeometry(QtCore.QRect(510, 230, 101, 41))
        self.toolButton_4.setObjectName("toolButton_remove")

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
        self.toolButton.setText(_translate("self.frameWidget", "Add channel"))
        self.toolButton_3.setText(_translate("self.frameWidget", "Edit"))
        self.toolButton_4.setText(_translate("self.frameWidget", "Remove "))
        self.toolButton_2.setText(_translate("self.frameWidget", "Submit"))

    def show(self):
        self.frameWidget.show()

    def hide(self):
        self.frameWidget.hide()

    def get_file_source(self):
        self.current_first_row_position = self.tableWidget_channelInput.rowCount()

        self.tableWidget_channelInput.insertRow(self.current_first_row_position)
        self.tableWidget_channelInput.insertRow(self.current_first_row_position + 1)
        self.tableWidget_channelInput.insertRow(self.current_first_row_position + 2)

        self.source = QFileDialog.getOpenFileName(self.frameWidget, "Open File", "",
                                                  options=QtWidgets.QFileDialog.DontUseNativeDialog)

        self.tableWidget_channelInput.setItem(self.current_first_row_position,
                                              0, QtWidgets.QTableWidgetItem(self.source[0]))
        self.tableWidget_channelInput.setItem(self.current_first_row_position + 1,
                                              0, QtWidgets.QTableWidgetItem(self.source[0]))
        self.tableWidget_channelInput.setItem(self.current_first_row_position + 2,
                                              0, QtWidgets.QTableWidgetItem(self.source[0]))

    def on_submit(self):
        channel_names_and_max_bit_values = []
        for i in range(self.current_first_row_position + 3):
            if not self.tableWidget_channelInput.item(i, 1) or not self.tableWidget_channelInput.item(i, 2):
                print("WARNING - set all necessary values!")
                return

            channel_name = str(self.tableWidget_channelInput.item(i, 1).text())
            channel_max_bit_size = int(str(self.tableWidget_channelInput.item(i, 2).text()))

            if ChannelApi.find_channel_by_name(self.data_container.get_channels_data_map(), channel_name):
                print("ERROR - Name: ", channel_name, " is already occupied! Chose another one")
                return

            channel_names_and_max_bit_values.append((channel_name, channel_max_bit_size))

        add_channels_to_multimodal_img(self.data_container,
                                       [ChannelInput(self.source[0], channel_names_and_max_bit_values)])

        self.hide()

