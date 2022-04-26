from csc_trello.view.login_window import LoginWindow
from csc_trello.view.sansys_login_dialog import SansysDialog
from csc_trello.view.trello_auth_dialog import TrelloAuthDialog
from csc_trello.controller.main_controller import MainController


class LoginController:
    def __init__(self):
        self._ui = LoginWindow()

        self.trello_dialog = None
        self.sansys_dialog = None
        self.main_window = None

        self.trello_key = None
        self.trello_token = None
        self.sansys_conn = None

        self._ui.btn_sansys.clicked.connect(self.auth_sansys)
        self._ui.btn_trello.clicked.connect(self.auth_trello)
        self._ui.btn_entrar.clicked.connect(self.login)

    def auth_sansys(self):
        self.sansys_dialog = SansysDialog(self)
        self.sansys_dialog.show()

    def auth_trello(self):
        self.trello_dialog = TrelloAuthDialog(self)
        self.trello_dialog.show()

    def unlock_login_button(self):
        if not (self._ui.btn_sansys.isEnabled() or self._ui.btn_trello.isEnabled()):
            self._ui.btn_entrar.setEnabled(True)

    def login(self):
        self.main_window = MainController(self.trello_key, self.trello_token, self.sansys_conn)
        self._ui.close()
