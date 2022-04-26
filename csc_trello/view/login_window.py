from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from csc_trello.utils.resource_import import resource_path


FORM_CLASS, _ = uic.loadUiType(resource_path('view\\ui\\login_window.ui'))

class LoginWindow(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setupUi(self)

        self.showNormal()