from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer

from src.data_container.channel.dto.channelInput import ChannelInput
from src.data_container.dataContainer import DataContainer
from src.library.libraryApi import standarize_image_channels, add_channels_to_multimodal_img
from src.library.standarization.enum.standarizationModeEnum import StandarizationModeEnum
from src.ui.mainWindowDialogHelper import *
from src.ui.refresh_gui.refreshGui import refresh_gui


class _UiMainWindow:

    def __init__(self):
        self.mainWindow = QtWidgets.QMainWindow()
        self._setup_ui_window()

        self.data_container = DataContainer()
        self._setup_ui()

        self.setup_timer()

    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: refresh_gui(self))
        self.timer.start(1000)

    def show(self):
        self.mainWindow.show()

    def _setup_ui_window(self):
        self.mainWindow.setGeometry(500, 500, 700, 700)
        self.mainWindow.setWindowTitle("Multimodal images visualization")

    def _setup_ui(self):
        self.mainWindow.setObjectName("self.mainWindow")
        self.mainWindow.resize(1136, 916)
        self.centralwidget = QtWidgets.QWidget(self.mainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.input_image = QtWidgets.QLabel(self.centralwidget)
        self.input_image.setGeometry(QtCore.QRect(0, 0, 121, 111))
        self.input_image.setText("")
        self.input_image.setPixmap(QtGui.QPixmap("../resources/sample_images/kingfisher.jpeg"))
        self.input_image.setScaledContents(True)
        self.input_image.setObjectName("input_image")

        self.label_multimodal_image_channels_list = QtWidgets.QLabel(self.centralwidget)
        self.label_multimodal_image_channels_list.setGeometry(QtCore.QRect(20, 130, 191, 16))
        self.label_multimodal_image_channels_list.setObjectName("label_multimodal_image_channels_list")

        self.listWidget_converted_channels = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_converted_channels.setGeometry(QtCore.QRect(1550, 160, 351, 711))
        self.listWidget_converted_channels.setObjectName("listWidget_converted_channels")

        self.label_converted_channels = QtWidgets.QLabel(self.centralwidget)
        self.label_converted_channels.setGeometry(QtCore.QRect(1670, 120, 141, 17))
        self.label_converted_channels.setScaledContents(False)
        self.label_converted_channels.setObjectName("label_converted_channels")

        self.frame_buttons = QtWidgets.QFrame(self.centralwidget)
        self.frame_buttons.setGeometry(QtCore.QRect(350, 160, 1201, 711))
        self.frame_buttons.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_buttons.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_buttons.setObjectName("frame_buttons")

        # BUTTONS
        self.toolButton_standarize_channels = QtWidgets.QToolButton(self.frame_buttons)
        self.toolButton_standarize_channels.setGeometry(QtCore.QRect(40, 30, 431, 71))
        self.toolButton_standarize_channels.setObjectName("toolButton_standarize_channels")
        self.toolButton_standarize_channels.clicked.connect(lambda:
                                                            standarize_image_channels(self.data_container, ["P"], {
                                                                'r': StandarizationModeEnum.BIT_SIZE_MIN_MAX,
                                                                'g': StandarizationModeEnum.BIT_SIZE_MIN_MAX,
                                                                'b': StandarizationModeEnum.BIT_SIZE_MIN_MAX
                                                            }))

        self.toolButton_decompose_single_channel_resolution = QtWidgets.QToolButton(self.frame_buttons)
        self.toolButton_decompose_single_channel_resolution.setGeometry(QtCore.QRect(40, 130, 431, 71))
        self.toolButton_decompose_single_channel_resolution.setObjectName(
            "toolButton_decompose_single_channel_resolution")
        self.toolButton_decompose_single_channel_resolution.clicked.connect(
            lambda: open_choose_channel_one_std_dialog(self.mainWindow, self.data_container))

        self.toolButton_reverse_decompose_single_channel_resolution = QtWidgets.QToolButton(self.frame_buttons)
        self.toolButton_reverse_decompose_single_channel_resolution.setGeometry(QtCore.QRect(40, 230, 431, 71))
        self.toolButton_reverse_decompose_single_channel_resolution.setObjectName(
            "toolButton_reverse_decompose_single_channel_resolution")

        self.toolButton_destandarize_channel_by_name = QtWidgets.QToolButton(self.frame_buttons)
        self.toolButton_destandarize_channel_by_name.setGeometry(QtCore.QRect(40, 330, 431, 71))
        self.toolButton_destandarize_channel_by_name.setObjectName("toolButton_destandarize_channel_by_name")

        self.toolButton_convert_channel = QtWidgets.QToolButton(self.frame_buttons)
        self.toolButton_convert_channel.setGeometry(QtCore.QRect(40, 430, 431, 71))
        self.toolButton_convert_channel.setObjectName("toolButton_convert_channel")

        self.toolButton_decompose_whole_image = QtWidgets.QToolButton(self.frame_buttons)
        self.toolButton_decompose_whole_image.setGeometry(QtCore.QRect(40, 540, 661, 71))
        self.toolButton_decompose_whole_image.setText("DECOMPOSE WHOLE IMAGE \n"
                                                      " FROM CHOSEN CHANNELS")
        self.toolButton_decompose_whole_image.setObjectName("toolButton_decompose_whole_image")

        self.toolButton_rvrs_decompose_whole_image = QtWidgets.QToolButton(self.frame_buttons)
        self.toolButton_rvrs_decompose_whole_image.setGeometry(QtCore.QRect(40, 630, 661, 71))
        self.toolButton_rvrs_decompose_whole_image.setText("REVERSE DECOMPOSE WHOLE IMAGE")
        self.toolButton_rvrs_decompose_whole_image.setObjectName("toolButton_rvrs_decompose_whole_image")

        self.toolButton_display_img = QtWidgets.QToolButton(self.frame_buttons)
        self.toolButton_display_img.setGeometry(QtCore.QRect(730, 110, 381, 171))
        self.toolButton_display_img.setText("DISPLAY IMAGE")
        self.toolButton_display_img.setObjectName("toolButton_display_img")

        self.label_multimodal_image_visualization = QtWidgets.QLabel(self.centralwidget)
        self.label_multimodal_image_visualization.setGeometry(QtCore.QRect(680, 20, 461, 91))

        self.toolButton_reset = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_reset.setGeometry(QtCore.QRect(1560, 10, 321, 81))
        self.toolButton_reset.setObjectName("toolButton_reset")

        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_multimodal_image_visualization.setFont(font)
        self.label_multimodal_image_visualization.setObjectName("label_multimodal_image_visualization")

        self.list_widget_multimodal_image_channels = QtWidgets.QListWidget(self.centralwidget)
        self.list_widget_multimodal_image_channels.setGeometry(QtCore.QRect(0, 160, 351, 711))
        self.list_widget_multimodal_image_channels.setFont(font)
        self.listWidget_converted_channels.setFont(font)
        self.list_widget_multimodal_image_channels.setObjectName("list_widget_multimodal_image_channels")

        self.mainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self.mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1897, 22))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.mainWindow)
        self.statusbar.setObjectName("statusbar")
        self.mainWindow.setStatusBar(self.statusbar)
        self.actionOpen_File = QtWidgets.QAction(self.mainWindow)
        self.actionOpen_File.setObjectName("actionOpen_File")
        self.actionCreate_new_Image = QtWidgets.QAction(self.mainWindow)
        self.actionCreate_new_Image.setObjectName("actionCreate_new_Image")
        self.actionAdd_channels_to_Image = QtWidgets.QAction(self.mainWindow)
        self.actionAdd_channels_to_Image.setObjectName("actionAdd_channels_to_Image")
        self.menuFile.addAction(self.actionCreate_new_Image)
        self.menuFile.addAction(self.actionAdd_channels_to_Image)
        self.menubar.addAction(self.menuFile.menuAction())

        self._retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.mainWindow)


        self.actionCreate_new_Image.triggered.connect(lambda: open_channel_input_dialog(self, self.data_container))

        add_channels_to_multimodal_img(self.data_container, [ChannelInput(
            'resources/sample_images/ball/ball_hsv_B.png',
            [
                ('r', 8), ('g', 8), ('b', 8)
            ]
        )])


    def _retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.mainWindow.setWindowTitle(_translate("MainWindow", "Multimodal Images"))
        self.label_multimodal_image_channels_list.setText(_translate("MainWindow", "Multimodal Image Channels"))
        self.label_converted_channels.setText(_translate("MainWindow", "Converted Channels"))
        self.toolButton_standarize_channels.setText(_translate("MainWindow", "STANDARIZE \n"
                                                                             "CHANNELS"))
        self.toolButton_decompose_single_channel_resolution.setText(_translate("MainWindow", "DECOMPOSE SINGLE \n"
                                                                                             "CHANNEL RESOLUTION"))
        self.toolButton_reverse_decompose_single_channel_resolution.setText(_translate("MainWindow", "REVERSE \n"
                                                                                                     "DECOMPOSE SINGLE \n"
                                                                                                     "CHANNEL RESOLUTION"))
        self.toolButton_destandarize_channel_by_name.setText(_translate("MainWindow", "DESTANDARIZE \n"
                                                                                      " CHANNEL BY NAME"))
        self.toolButton_convert_channel.setText(_translate("MainWindow", "CONVERT CHANNEL"))
        self.label_multimodal_image_visualization.setText(_translate("MainWindow", "MULTIMODAL IMAGE VISUALIZATION"))
        self.toolButton_reset.setText(_translate("MainWindow", "RESET ALL CONVERSIONS"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen_File.setText(_translate("MainWindow", "Open File"))
        self.actionCreate_new_Image.setText(_translate("MainWindow", "Create new Image"))
        self.actionAdd_channels_to_Image.setText(_translate("MainWindow", "Add channels to Image"))
