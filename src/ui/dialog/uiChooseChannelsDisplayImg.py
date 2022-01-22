from PyQt5 import QtCore, QtWidgets

from src.data_container.dataContainer import DataContainer
from src.library.libraryApi import multimodal_image_df_to_result_image
from src.library.visualization.enum.visualizationChannelsEnum import VisualizationChannelsEnum
from src.ui.available_actions.availableActionsApi import AvailableActionsApi
from src.ui.available_actions.enum.actionTypeEnum import ActionTypeEnum
from src.ui.dialog.abstractDialog.abstractDialog import AbstractDialog
from src.ui.dialog.uiResultDialog import UiResultDialog
from src.ui.properties.uiProperties import OUTPUT_IMAGE_NAME_RESULT, OUTPUT_IMAGE_FORMAT, OUTPUT_IMAGE_WIDTH, \
    OUTPUT_IMAGE_HEIGHT


class UiChooseChannelsDisplayImg(AbstractDialog):

    def __init__(self, data_container: DataContainer):
        super().__init__(data_container)

        self.result_dialog = None
        self.setupUi()

        self.set_possible_channels()

    def setupUi(self):
        self.frameWidget.setObjectName("self.frameWidget")
        self.frameWidget.resize(622, 504)
        self.pushButton_submit = QtWidgets.QPushButton(self.frameWidget)
        self.pushButton_submit.setGeometry(QtCore.QRect(350, 340, 231, 91))
        self.pushButton_submit.setObjectName("pushButton_submit")
        self.pushButton_submit.clicked.connect(lambda: self.on_submit())

        self.comboBox_visualization_type = QtWidgets.QComboBox(self.frameWidget)
        self.comboBox_visualization_type.setGeometry(QtCore.QRect(100, 360, 141, 51))
        self.comboBox_visualization_type.setObjectName("comboBox_visualization_type")
        self.comboBox_visualization_type.addItem("")
        self.comboBox_visualization_type.addItem("")
        self.comboBox_visualization_type.addItem("")
        self.comboBox_visualization_type.currentTextChanged.connect(lambda: self.set_possible_channels())

        self.label_2_instruction = QtWidgets.QLabel(self.frameWidget)
        self.label_2_instruction.setGeometry(QtCore.QRect(50, 10, 311, 81))
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

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.frameWidget)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.frameWidget.setWindowTitle(_translate("self.frameWidget", "Choose channels to display image"))
        self.pushButton_submit.setText(_translate("self.frameWidget", "Submit"))
        self.comboBox_visualization_type.setItemText(0, _translate("self.frameWidget", "GRAY_SCALE"))
        self.comboBox_visualization_type.setItemText(1, _translate("self.frameWidget", "RGB"))
        self.comboBox_visualization_type.setItemText(2, _translate("self.frameWidget", "HSV"))
        self.label_2_instruction.setText(_translate("self.frameWidget", "Choose channels and Visualization Type"))
        self.label_channel_1.setText(_translate("self.frameWidget", "Channel 1"))
        self.label_channel_2.setText(_translate("self.frameWidget", "Channel 2"))
        self.label_channel_3.setText(_translate("self.frameWidget", "Channel 3"))

    def set_possible_channels(self):
        self.comboBox_ch_1.clear()
        self.comboBox_ch_2.clear()
        self.comboBox_ch_3.clear()

        if VisualizationChannelsEnum[str(self.comboBox_visualization_type.currentText())] == \
                VisualizationChannelsEnum.GRAY_SCALE:
            self.comboBox_ch_2.setDisabled(True)
            self.comboBox_ch_3.setDisabled(True)
            self.label_channel_2.setStyleSheet("color: gray")
            self.label_channel_3.setStyleSheet("color: gray")

            self.comboBox_ch_1.addItems(AvailableActionsApi.find_channels_available_for_action(
                self.data_container, ActionTypeEnum.DISPLAY_IMAGE_REGULAR_ACTIONS,
                VisualizationChannelsEnum.GRAY_SCALE))
        else:
            self.label_channel_2.setStyleSheet("color: black")
            self.label_channel_3.setStyleSheet("color: black")

            self.comboBox_ch_2.setDisabled(False)
            self.comboBox_ch_3.setDisabled(False)

            if VisualizationChannelsEnum[str(self.comboBox_visualization_type.currentText())] == \
                    VisualizationChannelsEnum.HSV:
                available_channels = AvailableActionsApi.find_channels_available_for_action(
                    self.data_container, ActionTypeEnum.DISPLAY_IMAGE_REGULAR_ACTIONS,
                    VisualizationChannelsEnum.HSV)

                self.comboBox_ch_1.addItems(available_channels)
                self.comboBox_ch_2.addItems(available_channels)
                self.comboBox_ch_3.addItems(available_channels)
            else:
                available_channels = AvailableActionsApi.find_channels_available_for_action(
                    self.data_container, ActionTypeEnum.DISPLAY_IMAGE_REGULAR_ACTIONS,
                    VisualizationChannelsEnum.RGB)

                self.comboBox_ch_1.addItems(available_channels)
                self.comboBox_ch_2.addItems(available_channels)
                self.comboBox_ch_3.addItems(available_channels)

    def on_submit(self):
        if self.comboBox_ch_1.currentText() == '-' or self.comboBox_ch_2.currentText() == '-' \
                or self.comboBox_ch_3.currentText() == '-':
            return

        chosen_visualization_type = VisualizationChannelsEnum[str(self.comboBox_visualization_type.currentText())]

        multimodal_image_df_to_result_image(self.data_container, OUTPUT_IMAGE_NAME_RESULT,
                                            OUTPUT_IMAGE_WIDTH, OUTPUT_IMAGE_HEIGHT,
                                            OUTPUT_IMAGE_FORMAT, chosen_visualization_type,
                                            self.comboBox_ch_1.currentText(),
                                            self.comboBox_ch_2.currentText(),
                                            self.comboBox_ch_3.currentText())

        self.hide()
        self.open_result_dialog()

    def open_result_dialog(self):
        self.result_dialog = UiResultDialog(self.data_container, self.comboBox_ch_1.currentText(),
                                            self.comboBox_ch_2.currentText(), self.comboBox_ch_3.currentText())
        self.result_dialog.show()
