from PyQt5 import QtCore, QtWidgets

from src.data_container.dataContainer import DataContainer
from src.ui.dialog.abstractDialog.abstractDialog import AbstractDialog


class UiChooseChannelsDisplayImg(AbstractDialog):

    def __init__(self, data_container: DataContainer):
        super().__init__()
        self.data_container = data_container

        self.setupUi()

    def setupUi(self):
        self.frameWidget.setObjectName("self.frameWidget")
        self.frameWidget.resize(622, 504)
        self.pushButton_submit = QtWidgets.QPushButton(self.frameWidget)
        self.pushButton_submit.setGeometry(QtCore.QRect(350, 340, 231, 91))
        self.pushButton_submit.setObjectName("pushButton_submit")
        self.comboBox_decomposition_type = QtWidgets.QComboBox(self.frameWidget)
        self.comboBox_decomposition_type.setGeometry(QtCore.QRect(100, 360, 141, 51))
        self.comboBox_decomposition_type.setObjectName("comboBox_decomposition_type")
        self.comboBox_decomposition_type.addItem("")
        self.comboBox_decomposition_type.addItem("")
        self.comboBox_decomposition_type.addItem("")
        self.label_2_instruction = QtWidgets.QLabel(self.frameWidget)
        self.label_2_instruction.setGeometry(QtCore.QRect(160, 10, 311, 81))
        self.label_2_instruction.setWordWrap(True)
        self.label_2_instruction.setObjectName("label_2_instruction")
        self.frame = QtWidgets.QFrame(self.frameWidget)
        self.frame.setGeometry(QtCore.QRect(60, 110, 491, 171))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_channel_1 = QtWidgets.QLabel(self.frame)
        self.label_channel_1.setGeometry(QtCore.QRect(30, 30, 67, 17))
        self.label_channel_1.setObjectName("label_channel_1")
        self.label_channel_2 = QtWidgets.QLabel(self.frame)
        self.label_channel_2.setGeometry(QtCore.QRect(200, 30, 67, 17))
        self.label_channel_2.setObjectName("label_channel_2")
        self.label_channel_3 = QtWidgets.QLabel(self.frame)
        self.label_channel_3.setGeometry(QtCore.QRect(360, 30, 67, 17))
        self.label_channel_3.setObjectName("label_channel_3")
        self.comboBox_ch_1 = QtWidgets.QComboBox(self.frame)
        self.comboBox_ch_1.setGeometry(QtCore.QRect(10, 80, 121, 31))
        self.comboBox_ch_1.setObjectName("comboBox_ch_1")
        self.comboBox_ch_2 = QtWidgets.QComboBox(self.frame)
        self.comboBox_ch_2.setGeometry(QtCore.QRect(180, 80, 121, 31))
        self.comboBox_ch_2.setObjectName("comboBox_ch_2")
        self.comboBox_ch_3 = QtWidgets.QComboBox(self.frame)
        self.comboBox_ch_3.setGeometry(QtCore.QRect(340, 80, 121, 31))
        self.comboBox_ch_3.setObjectName("comboBox_ch_3")
        self.label_ch_by_idx = QtWidgets.QLabel(self.frame)
        self.label_ch_by_idx.setGeometry(QtCore.QRect(160, 130, 201, 31))
        self.label_ch_by_idx.setObjectName("label_ch_by_idx")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.frameWidget)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.frameWidget.setWindowTitle(_translate("self.frameWidget", "Choose channels to display image"))
        self.pushButton_submit.setText(_translate("self.frameWidget", "Submit"))
        self.comboBox_decomposition_type.setItemText(0, _translate("self.frameWidget", "GrayScale"))
        self.comboBox_decomposition_type.setItemText(1, _translate("self.frameWidget", "RGB"))
        self.comboBox_decomposition_type.setItemText(2, _translate("self.frameWidget", "HSV"))
        self.label_2_instruction.setText(_translate("self.frameWidget", "Choose channels and Visualization Type"))
        self.label_channel_1.setText(_translate("self.frameWidget", "Channel 1"))
        self.label_channel_2.setText(_translate("self.frameWidget", "Channel 2"))
        self.label_channel_3.setText(_translate("self.frameWidget", "Channel 3"))
        self.label_ch_by_idx.setText(_translate("self.frameWidget", "Channels labelled by indexes"))
