from bs4 import BeautifulSoup
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from csc_trello.utils.resource_import import resource_path


FORM_CLASS, _ = uic.loadUiType(resource_path('view\\ui\\trello_auth.ui'))


class TrelloAuthDialog(QDialog, FORM_CLASS):

    def __init__(self, main_controller, parent=None):
        super(TrelloAuthDialog, self).__init__(parent)
        self.setupUi(self)
        self.main_controller = main_controller

        self.webscrap = None
        self.html = None
        self.soup = None
        self.api_key = None
        self.token = None
        self.cicle_counter = 0

        self.label.setWordWrap(True)

        self.widget.setContextMenuPolicy(Qt.NoContextMenu)
        self.widget.load(QUrl('https://trello.com/login'))
        self.widget.show()

        self.widget.loadFinished.connect(self.page_loaded)
        self.widget.loadStarted.connect(self.page_loading)

    def page_loaded(self):
        current_url = self.widget.page().url().toString()

        if current_url == 'https://trello.com/login':
            self.label.setText('Faça login com sua conta Trello')

        if current_url == 'https://trello.com/app-key':
            self.cicle_counter += 1
            if self.cicle_counter == 2:
                self.webscrap = 'key'
                self.get_html()

        if '1/authorize?expiration=' in current_url:
            self.label.setText('Role até o final da página e clique em "Permitir"')

        if current_url == 'https://trello.com/1/token/approve':
            self.webscrap = 'token'
            self.get_html()

    def page_loading(self):
        self.label.setText('Aguarde...')
        url = self.widget.page().url().toString()
        if 'client-side-redirect' in url:
            url_apikey = 'https://trello.com/app-key'
            self.widget.setUrl(QUrl(url_apikey))

    def get_html(self):
        self.widget.page().toHtml(self.callable)

    def callable(self, data):
        self.html = data
        self.web_scraping()

    def web_scraping(self):
        self.soup = BeautifulSoup(self.html, 'html.parser')
        if self.webscrap == 'key':
            self.scrap_api_key()

        elif self.webscrap == 'token':
            self.scrap_token()

    def scrap_api_key(self):
        self.api_key = self.soup.body.section.div.div.input.get('value')
        url_token = f'''https://trello.com/1/authorize?expiration=never&scope=read,write,account&response_type=token&
        name=Server%20Token&key={self.api_key}'''
        self.widget.setUrl(QUrl(url_token))

    def scrap_token(self):
        self.token = self.soup.body.div.div.pre.getText()
        self.return_credentials()

    def return_credentials(self):
        self.main_controller.trello_key = self.api_key
        self.main_controller.trello_token = self.token
        self.main_controller._ui.btn_trello.setEnabled(False)
        self.main_controller.unlock_login_button()
        self.hide()
