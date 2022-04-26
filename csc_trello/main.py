import sys
from PyQt5.QtWidgets import QApplication
from csc_trello.controller.login_controller import LoginController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = LoginController()
    sys.exit(app.exec())
