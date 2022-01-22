from PyQt5 import QtCore, QtWidgets

from src.data_container.dataContainer import DataContainer
from src.library.libraryApi import decomposed_image_channels_df_to_image_save_file, \
    decomposed_rvrs_dcmpsd_image_channels_df_to_image_save_file
from src.ui.properties.uiProperties import OUTPUT_IMAGE_NAME_RESULT, OUTPUT_IMAGE_FORMAT, OUTPUT_IMAGE_WIDTH, \
    OUTPUT_IMAGE_HEIGHT
from src.library.visualization.enum.visualizationChannelsEnum import VisualizationChannelsEnum
from src.ui.available_actions.availableActionsApi import AvailableActionsApi
from src.ui.available_actions.enum.actionTypeEnum import ActionTypeEnum
from src.ui.dialog.abstractDialog.abstractDialog import AbstractDialog
from src.ui.dialog.uiResultDialog import UiResultDialog


class UiChooseChannelsDisplayImgWholeImgDecomposition(AbstractDialog):

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
        self.comboBox_visualization_type.setObjectName("comboBox_decomposition_type")
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

        self.label_ch_by_idx = QtWidgets.QLabel(self.frame)
        self.label_ch_by_idx.setGeometry(QtCore.QRect(160, 130, 201, 31))
        self.label_ch_by_idx.setObjectName("label_ch_by_idx")

        self.checkBox_after_rvrs_decomposition = QtWidgets.QCheckBox(self.frameWidget)
        self.checkBox_after_rvrs_decomposition.setGeometry(QtCore.QRect(440, 40, 21, 31))
        self.checkBox_after_rvrs_decomposition.setText("")
        self.checkBox_after_rvrs_decomposition.setObjectName("checkBox_after_rvrs_decomposition")
        self.checkBox_after_rvrs_decomposition.setVisible(
            self.data_container.decomposed_rvrs_dcmpsd_image_df is not None)
        self.checkBox_after_rvrs_decomposition.stateChanged.connect(lambda:
                                                                    self.on_checkBox_after_rvrs_decomposition_checked())

        self.label_after_rvrs_decomposition = QtWidgets.QLabel(self.frameWidget)
        self.label_after_rvrs_decomposition.setGeometry(QtCore.QRect(470, 20, 111, 71))
        self.label_after_rvrs_decomposition.setWordWrap(True)
        self.label_after_rvrs_decomposition.setObjectName("label_full_img_decomposition")
        self.label_after_rvrs_decomposition.setVisible(
            self.data_container.decomposed_rvrs_dcmpsd_image_df is not None)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.frameWidget)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.frameWidget.setWindowTitle(_translate("self.frameWidget", "Choose channels to display image"))
        self.pushButton_submit.setText(_translate("self.frameWidget", "Submit"))
        self.comboBox_visualization_type.setItemText(0, _translate("self.frameWidget", "GRAY_SCALE"))
        self.comboBox_visualization_type.setItemText(1, _translate("self.frameWidget", "RGB"))
        self.comboBox_visualization_type.setItemText(2, _translate("self.frameWidget", "HSV"))
        self.label_2_instruction.setText(
            _translate("self.frameWidget", "Choose channel indexes and Visualization Type"))
        self.label_channel_1.setText(_translate("self.frameWidget", "Channel 1"))
        self.label_channel_2.setText(_translate("self.frameWidget", "Channel 2"))
        self.label_channel_3.setText(_translate("self.frameWidget", "Channel 3"))
        self.label_ch_by_idx.setText(_translate("self.frameWidget", "Channels labelled by indexes"))
        self.label_after_rvrs_decomposition.setText(_translate("self.frameWidget", "After reverse decomposition"))

    def on_checkBox_after_rvrs_decomposition_checked(self):
        _translate = QtCore.QCoreApplication.translate

        self.comboBox_visualization_type.clear()
        self.comboBox_visualization_type.addItem("RGB")
        self.comboBox_visualization_type.addItem("GRAY_SCALE")

        if not self.checkBox_after_rvrs_decomposition.isChecked():
            self.comboBox_visualization_type.addItem("HSV")

        self.comboBox_visualization_type.setCurrentText("RGB")
        self.set_possible_channels()

    def set_possible_channels(self):
        self.comboBox_ch_1.clear()
        self.comboBox_ch_2.clear()
        self.comboBox_ch_3.clear()

        if self.checkBox_after_rvrs_decomposition.isChecked():
            action_type = ActionTypeEnum.DISPLAY_IMAGE_AFTER_WHOLE_IMG_RVRS_DECOMPOSITION
        else:
            action_type = ActionTypeEnum.DISPLAY_IMAGE_AFTER_WHOLE_IMG_DECOMPOSITION

        if not self.comboBox_visualization_type.currentText():
            return

        chosen_visualization_type = VisualizationChannelsEnum[str(self.comboBox_visualization_type.currentText())]
        available_channel_indexes = AvailableActionsApi.find_channels_available_for_action(
            self.data_container, action_type, chosen_visualization_type)

        self.comboBox_ch_1.addItems(available_channel_indexes)

        if chosen_visualization_type == \
                VisualizationChannelsEnum.GRAY_SCALE:
            self.comboBox_ch_2.setDisabled(True)
            self.comboBox_ch_3.setDisabled(True)
            self.label_channel_2.setStyleSheet("color: gray")
            self.label_channel_3.setStyleSheet("color: gray")

        else:
            self.label_channel_2.setStyleSheet("color: black")
            self.label_channel_3.setStyleSheet("color: black")

            self.comboBox_ch_2.setDisabled(False)
            self.comboBox_ch_3.setDisabled(False)

            self.comboBox_ch_2.addItems(available_channel_indexes)
            self.comboBox_ch_3.addItems(available_channel_indexes)

    def on_submit(self):
        chosen_visualization_type = VisualizationChannelsEnum[str(self.comboBox_visualization_type.currentText())]
        if self.comboBox_ch_1.currentText() == '-' or self.comboBox_ch_2.currentText() == '-' \
                or self.comboBox_ch_3.currentText() == '-':
            return

        channels_indexes = [int(self.comboBox_ch_1.currentText())]

        if chosen_visualization_type != VisualizationChannelsEnum.GRAY_SCALE:
            channels_indexes.append(int(self.comboBox_ch_2.currentText()))
            channels_indexes.append(int(self.comboBox_ch_3.currentText()))

        if self.checkBox_after_rvrs_decomposition.isChecked():
            decomposed_rvrs_dcmpsd_image_channels_df_to_image_save_file(self.data_container, OUTPUT_IMAGE_NAME_RESULT,
                                                                        OUTPUT_IMAGE_WIDTH, OUTPUT_IMAGE_HEIGHT,
                                                                        OUTPUT_IMAGE_FORMAT, chosen_visualization_type,
                                                                        channels_indexes)
        else:
            decomposed_image_channels_df_to_image_save_file(self.data_container, OUTPUT_IMAGE_NAME_RESULT,
                                                            OUTPUT_IMAGE_WIDTH, OUTPUT_IMAGE_HEIGHT,
                                                            OUTPUT_IMAGE_FORMAT, chosen_visualization_type,
                                                            channels_indexes)

        self.hide()
        self.open_result_dialog()

    def open_result_dialog(self):
        self.result_dialog = UiResultDialog(self.data_container, self.comboBox_ch_1.currentText(),
                                            self.comboBox_ch_2.currentText(), self.comboBox_ch_3.currentText())
        self.result_dialog.show()
