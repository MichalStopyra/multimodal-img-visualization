from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

from src.data_container.dataContainer import DataContainer
from src.library.decomposition.enum.decompositionEnum import DecompositionEnum
from src.library.libraryApi import decompose_channel_resolution_wrapper
from src.ui.available_actions.availableActionsApi import AvailableActionsApi
from src.ui.available_actions.enum.actionTypeEnum import ActionTypeEnum


class UiChooseChannelOneStdDialog():

    def __init__(self, data_container: DataContainer):
        self.frameWidget = QtWidgets.QFrame()
        self.data_container = data_container
        self.fast_ica_n_components = None

        self.setupUi()

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
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        self.set_channels_List()

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)

        self.comboBox_decomposition_type = QtWidgets.QComboBox(self.frameWidget)
        self.comboBox_decomposition_type.setGeometry(QtCore.QRect(440, 250, 141, 51))
        self.comboBox_decomposition_type.setObjectName("comboBox_decompositio_type")
        self.comboBox_decomposition_type.addItem("")
        self.comboBox_decomposition_type.addItem("")
        self.comboBox_decomposition_type.addItem("")
        self.comboBox_decomposition_type.currentTextChanged.connect(lambda: self.on_combobox_changed())

        self.label = QtWidgets.QLabel(self.frameWidget)
        self.label.setGeometry(QtCore.QRect(400, 350, 171, 17))
        self.label.setObjectName("label")

        self.textEdit_ica_n_components = QtWidgets.QTextEdit(self.frameWidget)
        self.textEdit_ica_n_components.setGeometry(QtCore.QRect(400, 370, 161, 31))
        self.textEdit_ica_n_components.setObjectName("textEdit_ica_n_components")
        self.textEdit_ica_n_components.setText('')
        self.textEdit_ica_n_components.textChanged.connect(lambda: self.on_fast_ica_n_components_changed())

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

        self.comboBox_decomposition_type.setItemText(0, _translate("QFrame_choose_channel_one_std", "PCA"))
        self.comboBox_decomposition_type.setItemText(1, _translate("QFrame_choose_channel_one_std", "FAST_ICA"))
        self.comboBox_decomposition_type.setItemText(2, _translate("QFrame_choose_channel_one_std", "NMF"))
        self.label.setText(_translate("QFrame_choose_channel_one_std", "FAST ICA n_components"))

    def show(self):
        self.frameWidget.show()

    def hide(self):
        self.frameWidget.hide()

    def set_channels_List(self):
        available_channels = AvailableActionsApi.find_channels_available_for_action(
            self.data_container, ActionTypeEnum.DECOMPOSE_SINGLE_CHANNEL_RESOLUTION)

        for index, av_channel in enumerate(available_channels):
            self.tableWidget.insertRow(index)
            self.tableWidget.setItem(index, 0, QtWidgets.QTableWidgetItem(av_channel[0]))

            if av_channel[1]:
                item = QTableWidgetItem('av'.format(index, 1))
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            else:
                item = QTableWidgetItem('not av'.format(index, 1))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)

            self.tableWidget.setItem(index, 1, item)

    def on_submit(self):
        current_cell_row = self.tableWidget.currentRow()
        if current_cell_row == -1:
            print ("Choose cell for action!")
            return
        channel_name = str(self.tableWidget.item(current_cell_row, 0).text())
        take_std = bool((self.tableWidget.item(current_cell_row, 1).checkState() == QtCore.Qt.Checked))

        chosen_decomposition_type = DecompositionEnum[str(self.comboBox_decomposition_type.currentText())]

        decompose_channel_resolution_wrapper(self.data_container, channel_name, chosen_decomposition_type,
                                             take_std, self.fast_ica_n_components)

        self.hide()


    def on_combobox_changed(self):
        if DecompositionEnum[str(self.comboBox_decomposition_type.currentText())] == DecompositionEnum.FAST_ICA:
            self.textEdit_ica_n_components.setReadOnly(False)
            self.label.setStyleSheet("color: black")
        else:
            self.label.setStyleSheet("color: gray")
            self.textEdit_ica_n_components.setReadOnly(True)
            self.fast_ica_n_components = None


    def on_fast_ica_n_components_changed(self):
        try:
            self.fast_ica_n_components = int(self.textEdit_ica_n_components.toPlainText())
        except ValueError:
            print("N channels not an int value - assigning value = 1")
            self.fast_ica_n_components = 1
