from PyQt5 import QtCore, QtGui, QtWidgets


class _UiMainWindow:

    def __init__(self):
        self.mainWindow = QtWidgets.QMainWindow()
        self._setup_ui_window()
        self._setup_ui()

    def show(self):
        self.mainWindow.show()

    def _setup_ui_window(self):
        self.mainWindow.setGeometry(200, 200, 300, 300)
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
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 130, 191, 16))
        self.label.setObjectName("label")
        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(1550, 160, 351, 711))
        self.listWidget_2.setObjectName("listWidget_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1670, 120, 141, 17))
        self.label_2.setScaledContents(False)
        self.label_2.setObjectName("label_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(350, 160, 1201, 711))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.toolButton = QtWidgets.QToolButton(self.frame)
        self.toolButton.setGeometry(QtCore.QRect(40, 30, 431, 71))
        self.toolButton.setObjectName("toolButton")
        self.toolButton_2 = QtWidgets.QToolButton(self.frame)
        self.toolButton_2.setGeometry(QtCore.QRect(40, 130, 431, 71))
        self.toolButton_2.setObjectName("toolButton_2")
        self.toolButton_3 = QtWidgets.QToolButton(self.frame)
        self.toolButton_3.setGeometry(QtCore.QRect(40, 230, 431, 71))
        self.toolButton_3.setObjectName("toolButton_3")
        self.toolButton_4 = QtWidgets.QToolButton(self.frame)
        self.toolButton_4.setGeometry(QtCore.QRect(40, 330, 431, 71))
        self.toolButton_4.setObjectName("toolButton_4")
        self.toolButton_5 = QtWidgets.QToolButton(self.frame)
        self.toolButton_5.setGeometry(QtCore.QRect(40, 430, 431, 71))
        self.toolButton_5.setObjectName("toolButton_5")
        self.toolButton_6 = QtWidgets.QToolButton(self.frame)
        self.toolButton_6.setGeometry(QtCore.QRect(40, 540, 661, 71))
        self.toolButton_6.setText("DECOMPOSE WHOLE IMAGE \n"
                                  " FROM CHOSEN CHANNELS")
        self.toolButton_6.setObjectName("toolButton_6")
        self.toolButton_7 = QtWidgets.QToolButton(self.frame)
        self.toolButton_7.setGeometry(QtCore.QRect(40, 630, 661, 71))
        self.toolButton_7.setText("REVERSE DECOMPOSE WHOLE IMAGE")
        self.toolButton_7.setObjectName("toolButton_7")
        self.toolButton_8 = QtWidgets.QToolButton(self.frame)
        self.toolButton_8.setGeometry(QtCore.QRect(730, 110, 381, 171))
        self.toolButton_8.setText("DISPLAY IMAGE")
        self.toolButton_8.setObjectName("toolButton_8")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(680, 20, 461, 91))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.toolButton_9 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_9.setGeometry(QtCore.QRect(1560, 10, 321, 81))
        self.toolButton_9.setObjectName("toolButton_9")
        self.listWidget_3 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_3.setGeometry(QtCore.QRect(0, 160, 351, 711))
        self.listWidget_3.setObjectName("listWidget_3")
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

    def _retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.mainWindow.setWindowTitle(_translate("self.mainWindow", "Multimodal Images"))
        self.label.setText(_translate("self.mainWindow", "Multimodal Image Channels"))
        self.label_2.setText(_translate("self.mainWindow", "Converted Channels"))
        self.toolButton.setText(_translate("self.mainWindow", "STANDARIZE \n"
                                                         "CHANNELS"))
        self.toolButton_2.setText(_translate("self.mainWindow", "DECOMPOSE SINGLE \n"
                                                           "CHANNEL RESOLUTION"))
        self.toolButton_3.setText(_translate("self.mainWindow", "REVERSE \n"
                                                           "DECOMPOSE SINGLE \n"
                                                           "CHANNEL RESOLUTION"))
        self.toolButton_4.setText(_translate("self.mainWindow", "DESTANDARIZE \n"
                                                           " CHANNEL BY NAME"))
        self.toolButton_5.setText(_translate("self.mainWindow", "CONVERT CHANNEL"))
        self.label_3.setText(_translate("self.mainWindow", "MULTIMODAL IMAGE VISUALIZATION"))
        self.toolButton_9.setText(_translate("self.mainWindow", "RESET ALL CONVERSIONS"))
        self.menuFile.setTitle(_translate("self.mainWindow", "File"))
        self.actionOpen_File.setText(_translate("self.mainWindow", "Open File"))
        self.actionCreate_new_Image.setText(_translate("self.mainWindow", "Create new Image"))
        self.actionAdd_channels_to_Image.setText(_translate("self.mainWindow", "Add channels to Image"))

