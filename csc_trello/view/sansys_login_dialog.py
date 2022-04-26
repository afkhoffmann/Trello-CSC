from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QLineEdit
from csc_trello.utils.messages import error_msg
from csc_trello.model.sansys_user import SansysUser
from csc_trello.utils.resource_import import resource_path


FORM_CLASS, _ = uic.loadUiType(resource_path('view\\ui\\login_sansys.ui'))


class SansysDialog(QDialog, FORM_CLASS):

    def __init__(self, main_controller, parent=None):
        super(SansysDialog, self).__init__(parent)
        self.setupUi(self)

        self.user = None
        self.main_controller = main_controller

        self.lineEdit_password.setEchoMode(QLineEdit.Password)

        self.btn_login.clicked.connect(self.check_user)

    def login(self):
        conn = self.user.connect()
        if conn:
            self.label.setText('')
            self.main_controller.sansys_conn = conn
            self.main_controller._ui.btn_sansys.setEnabled(False)
            self.main_controller.unlock_login_button()
            self.hide()
        else:
            error_msg(self.label, 'Usuário/senha incorreto(s)')

    def check_user(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()

        if not username or not password:
            error_msg(self.label, 'Usuário/senha devem ser informados')
            return

        self.user = SansysUser(username, password)

        self.login()
