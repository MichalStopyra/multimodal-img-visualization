from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer

from src.data_container.channel.dto.channelInput import ChannelInput
from src.library.libraryApi import add_channels_to_multimodal_img, rvrs_decompose_whole_image_channels
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
        self.mainWindow.showFullScreen()

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
        self.toolButton_standarize_channels.clicked.connect(
            lambda: open_choose_channels_standarization(self.mainWindow, self.data_container))

        self.toolButton_decompose_single_channel_resolution = QtWidgets.QToolButton(self.frame_buttons)
        self.toolButton_decompose_single_channel_resolution.setGeometry(QtCore.QRect(40, 130, 431, 71))
        self.toolButton_decompose_single_channel_resolution.setObjectName(
            "toolButton_decompose_single_channel_resolution")
        self.toolButton_decompose_single_channel_resolution.clicked.connect(
            lambda: open_choose_channel_decompose_single_channel(self.mainWindow, self.data_container))

        self.toolButton_reverse_decompose_single_channel_resolution = QtWidgets.QToolButton(self.frame_buttons)
        self.toolButton_reverse_decompose_single_channel_resolution.setGeometry(QtCore.QRect(40, 230, 431, 71))
        self.toolButton_reverse_decompose_single_channel_resolution.setObjectName(
            "toolButton_reverse_decompose_single_channel_resolution")
        self.toolButton_reverse_decompose_single_channel_resolution.clicked.connect(
            lambda: open_choose_channel_rvrs_decomposition(self.mainWindow, self.data_container))

        self.toolButton_destandarize_channel_by_name = QtWidgets.QToolButton(self.frame_buttons)
        self.toolButton_destandarize_channel_by_name.setGeometry(QtCore.QRect(40, 330, 431, 71))
        self.toolButton_destandarize_channel_by_name.setObjectName("toolButton_destandarize_channel_by_name")
        self.toolButton_destandarize_channel_by_name.clicked.connect(
            lambda: open_choose_channel_destandarization(self.mainWindow, self.data_container))

        self.toolButton_convert_channel = QtWidgets.QToolButton(self.frame_buttons)
        self.toolButton_convert_channel.setGeometry(QtCore.QRect(40, 430, 431, 71))
        self.toolButton_convert_channel.setObjectName("toolButton_convert_channel")
        self.toolButton_convert_channel.clicked.connect(
            lambda: open_choose_channels_conversion(self.mainWindow, self.data_container))

        self.toolButton_decompose_whole_image = QtWidgets.QToolButton(self.frame_buttons)
        self.toolButton_decompose_whole_image.setGeometry(QtCore.QRect(40, 540, 661, 71))
        self.toolButton_decompose_whole_image.setText("DECOMPOSE WHOLE IMAGE \n"
                                                      " FROM CHOSEN CHANNELS")
        self.toolButton_decompose_whole_image.setObjectName("toolButton_decompose_whole_image")
        self.toolButton_decompose_whole_image.clicked.connect(
            lambda: open_choose_channels_decompose_whole_img(self.mainWindow, self.data_container))

        self.toolButton_rvrs_decompose_whole_image = QtWidgets.QToolButton(self.frame_buttons)
        self.toolButton_rvrs_decompose_whole_image.setGeometry(QtCore.QRect(40, 630, 661, 71))
        self.toolButton_rvrs_decompose_whole_image.setText("REVERSE DECOMPOSE WHOLE IMAGE")
        self.toolButton_rvrs_decompose_whole_image.setObjectName("toolButton_rvrs_decompose_whole_image")
        self.toolButton_rvrs_decompose_whole_image.clicked.connect(
            lambda: rvrs_decompose_whole_image_channels(self.data_container))

        self.toolButton_display_img = QtWidgets.QToolButton(self.frame_buttons)
        self.toolButton_display_img.setGeometry(QtCore.QRect(730, 110, 381, 171))
        self.toolButton_display_img.setText("DISPLAY IMAGE")
        self.toolButton_display_img.setObjectName("toolButton_display_img")
        self.toolButton_display_img.clicked.connect(
            lambda: open_choose_channels_display_img(self.mainWindow, self.data_container))

        self.toolButton_display_img_2 = QtWidgets.QToolButton(self.frame_buttons)
        self.toolButton_display_img_2.setGeometry(QtCore.QRect(810, 570, 221, 101))
        self.toolButton_display_img_2.setText("DISPLAY IMAGE AFTER \n"
                                              "WHOLE IMG DECOMPOSITION")
        self.toolButton_display_img_2.setObjectName("toolButton_display_img_2")
        self.toolButton_display_img_2.clicked.connect(
            lambda: open_choose_channels_display_img_whole_img_decomposition(self.mainWindow, self.data_container))

        self.label_multimodal_image_visualization = QtWidgets.QLabel(self.centralwidget)
        self.label_multimodal_image_visualization.setGeometry(QtCore.QRect(680, 20, 461, 91))

        self.toolButton_reset = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_reset.setGeometry(QtCore.QRect(1560, 10, 321, 81))
        self.toolButton_reset.setObjectName("toolButton_reset")
        self.toolButton_reset.clicked.connect(lambda: self.reset_conversions())

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
        self.actionAdd_channels_to_Image = QtWidgets.QAction(self.mainWindow)
        self.actionAdd_channels_to_Image.setObjectName("actionCreate_new_Image")
        self.menuFile.addAction(self.actionAdd_channels_to_Image)
        self.menubar.addAction(self.menuFile.menuAction())
        self.actionAdd_channels_to_Image.triggered.connect(lambda: open_channel_input_dialog(self, self.data_container))

        self.draw_lines()

        self._retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.mainWindow)

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
        self.actionAdd_channels_to_Image.setText(_translate("MainWindow", "Add channels to Image"))

    def reset_conversions(self):
        self.data_container.reset_conversions()
        self.listWidget_converted_channels.clear()

    def draw_lines(self):
        self.line = QtWidgets.QFrame(self.frame_buttons)
        self.line.setGeometry(QtCore.QRect(470, 460, 211, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.frame_buttons)
        self.line_2.setGeometry(QtCore.QRect(470, 350, 211, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.frame_buttons)
        self.line_3.setGeometry(QtCore.QRect(470, 250, 211, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.frame_buttons)
        self.line_4.setGeometry(QtCore.QRect(470, 160, 211, 20))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(self.frame_buttons)
        self.line_5.setGeometry(QtCore.QRect(470, 50, 211, 20))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_6 = QtWidgets.QFrame(self.frame_buttons)
        self.line_6.setGeometry(QtCore.QRect(680, 190, 51, 20))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.line_7 = QtWidgets.QFrame(self.frame_buttons)
        self.line_7.setGeometry(QtCore.QRect(670, 60, 20, 411))
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")

        self.line_8 = QtWidgets.QFrame(self.frame_buttons)
        self.line_8.setGeometry(QtCore.QRect(700, 570, 51, 16))
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.line_9 = QtWidgets.QFrame(self.frame_buttons)
        self.line_9.setGeometry(QtCore.QRect(700, 660, 51, 16))
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.line_10 = QtWidgets.QFrame(self.frame_buttons)
        self.line_10.setGeometry(QtCore.QRect(750, 610, 61, 20))
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.line_11 = QtWidgets.QFrame(self.frame_buttons)
        self.line_11.setGeometry(QtCore.QRect(740, 580, 16, 91))
        self.line_11.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
