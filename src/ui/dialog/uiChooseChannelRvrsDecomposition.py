from PyQt5 import QtCore, QtWidgets

from src.data_container.dataContainer import DataContainer
from src.library.libraryApi import reverse_decompose_single_channel
from src.ui.available_actions.availableActionsApi import AvailableActionsApi
from src.ui.available_actions.enum.actionTypeEnum import ActionTypeEnum
from src.ui.dialog.abstractDialog.abstractDialog import AbstractDialog


class UiChooseChannelRvrsDecomposition(AbstractDialog):

    def __init__(self, data_container: DataContainer):
        super().__init__(data_container)

        self.setupUi()

        self.set_channels_List()

    def setupUi(self):
        self.frameWidget.setObjectName("self.frameWidget")
        self.frameWidget.resize(622, 504)
        self.pushButton_submit = QtWidgets.QPushButton(self.frameWidget)
        self.pushButton_submit.setGeometry(QtCore.QRect(390, 190, 231, 91))
        self.pushButton_submit.setObjectName("pushButton_submit")
        self.pushButton_submit.clicked.connect(lambda: self.on_submit())

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

        header = self.tableWidget_channels.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)

        self.label_instruction.setText(_translate("self.frameWidget", "Choose one channel"))

    def set_channels_List(self):
        available_channels = AvailableActionsApi.find_channels_available_for_action(
            self.data_container, ActionTypeEnum.REVERSE_DECOMPOSE_SINGLE_CHANNEL_RESOLUTION)

        for index, av_channel in enumerate(available_channels):
            self.tableWidget_channels.insertRow(index)
            self.tableWidget_channels.setItem(index, 0, QtWidgets.QTableWidgetItem(av_channel[0]))

    def on_submit(self):
        current_cell_row = self.tableWidget_channels.currentRow()
        if current_cell_row == -1:
            print("Choose cell for rvrs decomposition!")
            return

        channel_name = str(self.tableWidget_channels.item(current_cell_row, 0).text())

        reverse_decompose_single_channel(self.data_container, channel_name)

        self.hide()
