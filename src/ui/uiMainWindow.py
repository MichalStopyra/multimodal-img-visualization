from PyQt5 import QtCore, QtGui, QtWidgets


class UiMainWindow:

    def __init__(self):
        self.mainWindow = QtWidgets.QMainWindow()
        self.setup_ui_window()
        self.setup_ui()

    def show(self):
        self.mainWindow.show()

    def setup_ui_window(self):
        self.mainWindow.setGeometry(200, 200, 300, 300)
        self.mainWindow.setWindowTitle("Multimodal images visualization")

    def setup_ui(self):
        self.mainWindow.setObjectName("self.mainWindow")
        self.mainWindow.resize(1136, 916)
        self.centralwidget = QtWidgets.QWidget(self.mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.input_image = QtWidgets.QLabel(self.centralwidget)
        self.input_image.setGeometry(QtCore.QRect(10, 10, 261, 241))
        self.input_image.setText("")
        self.input_image.setPixmap(QtGui.QPixmap("./resources/sample_images/kingfisher.jpeg"))
        self.input_image.setScaledContents(True)
        self.input_image.setObjectName("input_image")
        self.decomposition_type_label = QtWidgets.QLabel(self.centralwidget)
        self.decomposition_type_label.setGeometry(QtCore.QRect(10, 270, 261, 51))
        self.decomposition_type_label.setObjectName("decomposition_type_label")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 330, 261, 161))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.b_decomposition_type_nmf = QtWidgets.QPushButton(self.frame)
        self.b_decomposition_type_nmf.setGeometry(QtCore.QRect(0, 120, 261, 41))
        self.b_decomposition_type_nmf.setObjectName("b_decomposition_type_nmf")
        self.b_decomposition_type_fast_ica = QtWidgets.QPushButton(self.frame)
        self.b_decomposition_type_fast_ica.setGeometry(QtCore.QRect(0, 60, 261, 41))
        self.b_decomposition_type_fast_ica.setObjectName("b_decomposition_type_fast_ica")
        self.b_decomposition_type_pca = QtWidgets.QPushButton(self.frame)
        self.b_decomposition_type_pca.setGeometry(QtCore.QRect(0, 0, 261, 41))
        self.b_decomposition_type_pca.setObjectName("b_decomposition_type_pca")
        self.mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self.mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1136, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.mainWindow)
        self.statusbar.setObjectName("statusbar")
        self.mainWindow.setStatusBar(self.statusbar)
        self.actionOpen_File = QtWidgets.QAction(self.mainWindow)
        self.actionOpen_File.setObjectName("actionOpen_File")
        self.menuFile.addAction(self.actionOpen_File)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.mainWindow)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.mainWindow.setWindowTitle(_translate("self.mainWindow", "Multimodal Images"))
        self.decomposition_type_label.setText(_translate("self.mainWindow", "Choose Decomposition Type"))
        self.b_decomposition_type_nmf.setText(_translate("self.mainWindow", "NMF"))
        self.b_decomposition_type_fast_ica.setText(_translate("self.mainWindow", "Fast ICA"))
        self.b_decomposition_type_pca.setText(_translate("self.mainWindow", "PCA"))
        self.menuFile.setTitle(_translate("self.mainWindow", "File"))
        self.actionOpen_File.setText(_translate("self.mainWindow", "Open File"))