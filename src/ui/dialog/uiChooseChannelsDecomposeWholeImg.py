from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

from src.data_container.dataContainer import DataContainer
from src.library.decomposition.enum.decompositionEnum import DecompositionEnum
from src.library.libraryApi import decompose_whole_image_channels
from src.ui.available_actions.availableActionsApi import AvailableActionsApi
from src.ui.available_actions.enum.actionTypeEnum import ActionTypeEnum
from src.ui.dialog.abstractDialog.abstractDialog import AbstractDialog


class UiChooseChannelsDecomposeWholeImg(AbstractDialog):

    def __init__(self, data_container: DataContainer):
        super().__init__(data_container)

        self.setupUi()

        self.set_channels_List()

    def setupUi(self):
        self.frameWidget.setObjectName("self.frameWidget")
        self.frameWidget.resize(622, 504)
        self.pushButton_submit = QtWidgets.QPushButton(self.frameWidget)
        self.pushButton_submit.setGeometry(QtCore.QRect(390, 110, 231, 91))
        self.pushButton_submit.setObjectName("pushButton_submit")
        self.pushButton_submit.clicked.connect(lambda: self.on_submit())

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
        self.comboBox_decomposition_type.currentTextChanged.connect(lambda: self.on_combobox_changed())

        self.label = QtWidgets.QLabel(self.frameWidget)
        self.label.setGeometry(QtCore.QRect(400, 350, 171, 17))
        self.label.setObjectName("label")
        self.textEdit_ica_n_components = QtWidgets.QTextEdit(self.frameWidget)
        self.textEdit_ica_n_components.setGeometry(QtCore.QRect(400, 370, 161, 31))
        self.textEdit_ica_n_components.setObjectName("textEdit_ica_n_components")
        self.textEdit_ica_n_components.textChanged.connect(lambda: self.on_fast_ica_n_components_changed())

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

        header = self.tableWidget_channels.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        self.comboBox_decomposition_type.setItemText(0, _translate("self.frameWidget", "PCA"))
        self.comboBox_decomposition_type.setItemText(1, _translate("self.frameWidget", "FAST ICA"))
        self.comboBox_decomposition_type.setItemText(2, _translate("self.frameWidget", "NMF"))
        self.label.setText(_translate("self.frameWidget", "FAST ICA n_components"))
        self.label_2.setText(_translate("self.frameWidget",
                                        "Firstly check choose std checkboxes, then choose multiple channels"))

    def set_channels_List(self):
        available_channels = AvailableActionsApi.find_channels_available_for_action(
            self.data_container, ActionTypeEnum.DECOMPOSE_WHOLE_IMAGE_CHANNELS)

        for index, av_channel in enumerate(available_channels):
            self.tableWidget_channels.insertRow(index)
            self.tableWidget_channels.setItem(index, 0, QtWidgets.QTableWidgetItem(av_channel[0]))

            if av_channel[1]:
                item = QTableWidgetItem('av'.format(index, 1))
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            else:
                item = QTableWidgetItem('not av'.format(index, 1))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)

            self.tableWidget_channels.setItem(index, 1, item)

    def on_submit(self):
        selected_channels = self.tableWidget_channels.selectedItems()
        if not selected_channels:
            print("Choose channels to decompose!")
            return

        channel_names_and_take_std_tuple = []

        for item in selected_channels:
            channel_name = item.data(0)
            take_std = bool((self.tableWidget_channels.item(item.row(), 1).checkState() == QtCore.Qt.Checked))

            channel_names_and_take_std_tuple.append((channel_name, take_std))

        chosen_decomposition_type = DecompositionEnum[str(self.comboBox_decomposition_type.currentText())]

        decompose_whole_image_channels(self.data_container, chosen_decomposition_type,
                                       channel_names_and_take_std_tuple)

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
