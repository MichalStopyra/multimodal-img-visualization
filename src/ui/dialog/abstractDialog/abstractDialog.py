from abc import ABCMeta

from PyQt5 import QtWidgets

from src.data_container.dataContainer import DataContainer


class AbstractDialog():
    __metaclass__ = ABCMeta

    def __init__(self, data_container: DataContainer):
        self.frameWidget = QtWidgets.QFrame()
        self.data_container = data_container

    def show(self):
        self.frameWidget.show()

    def hide(self):
        self.frameWidget.hide()
