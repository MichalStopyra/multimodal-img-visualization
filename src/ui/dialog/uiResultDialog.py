from PyQt5 import QtCore, QtGui, QtWidgets

from src.data_container.dataContainer import DataContainer
from src.library.properties.properties import OUTPUT_IMAGE_PATH, OUTPUT_IMAGE_NAME_RESULT, OUTPUT_IMAGE_FORMAT, \
    OUTPUT_IMAGE_WIDTH, OUTPUT_IMAGE_HEIGHT
from src.library.visualization.enum.outputImageFormatEnum import translate_output_format_enum
from src.ui.dialog.abstractDialog.abstractDialog import AbstractDialog


class UiResultDialog(AbstractDialog):

    def __init__(self, data_container: DataContainer, ch_1: str, ch_2: str, ch_3: str):
        super().__init__(data_container)

        self.ch_1 = ch_1
        self.ch_2 = ch_2
        self.ch_3 = ch_3

        self.setupUi()
        self.set_data()

    def setupUi(self):
        self.frameWidget.setObjectName("self.frameWidget")
        self.frameWidget.resize(861, 715)

        self.label = QtWidgets.QLabel(self.frameWidget)
        self.label.setGeometry(QtCore.QRect(0, 0, OUTPUT_IMAGE_WIDTH / 2, OUTPUT_IMAGE_HEIGHT / 2))
        self.label.setText("")
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.label_result_from = QtWidgets.QLabel(self.frameWidget)
        self.label_result_from.setGeometry(QtCore.QRect(20, 620, 91, 21))
        self.label_result_from.setObjectName("label_result_from")

        self.label_result_ch1 = QtWidgets.QLabel(self.frameWidget)
        self.label_result_ch1.setGeometry(QtCore.QRect(180, 620, 131, 21))
        self.label_result_ch1.setObjectName("label_result_ch1")

        self.label_result_ch_2 = QtWidgets.QLabel(self.frameWidget)
        self.label_result_ch_2.setGeometry(QtCore.QRect(370, 620, 141, 17))
        self.label_result_ch_2.setObjectName("label_result_ch1_2")
        self.label_result_ch_2.setHidden(not self.ch_2)

        self.label_result_ch_3 = QtWidgets.QLabel(self.frameWidget)
        self.label_result_ch_3.setGeometry(QtCore.QRect(610, 620, 141, 17))
        self.label_result_ch_3.setObjectName("label_result_ch1_3")
        self.label_result_ch_2.setHidden(not self.ch_3)

        self.retranslateUi()

        QtCore.QMetaObject.connectSlotsByName(self.frameWidget)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.frameWidget.setWindowTitle(_translate("self.frameWidget", "result"))
        self.label_result_from.setText(_translate("self.frameWidget", "Result from: "))
        self.label_result_ch1.setText(_translate("self.frameWidget", self.ch_1))
        if self.ch_2:
            self.label_result_ch_2.setText(_translate("self.frameWidget", self.ch_2))
        if self.ch_3:
            self.label_result_ch_3.setText(_translate("self.frameWidget", self.ch_3))

    def set_data(self):
        self.label.setPixmap(QtGui.QPixmap(OUTPUT_IMAGE_PATH + OUTPUT_IMAGE_NAME_RESULT +
                                           translate_output_format_enum(OUTPUT_IMAGE_FORMAT)))

