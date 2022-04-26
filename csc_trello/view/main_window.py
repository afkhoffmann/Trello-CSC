from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from csc_trello.utils.resource_import import resource_path


FORM_CLASS, _ = uic.loadUiType(resource_path('view\\ui\\main_window.ui'))


class MainWindow(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.showNormal()
