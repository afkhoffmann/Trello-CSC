import requests
import json
from time import sleep
from PyQt5.QtCore import pyqtSignal, QObject


class TrelloService(QObject):
    msgLog = pyqtSignal(str)

    def __init__(self, trello_key, trello_token):
        super().__init__()
        self.api_key = trello_key
        self.api_token = trello_token

    def send_request(self, method: str, url: str, **kwargs) -> requests.request:
        """
        Envia uma requisição HTTP e testa se a resposta foi bem sucedida.
        :return: Resposta da requisição.
        """

        response = requests.request(method, url, **kwargs)
        while not response.ok:
            if response.status_code == 429:
                self.msgLog.emit("Limite da API excedido. Tentando novamente em 10 segundos...")
                sleep(8)
            else:
                self.msgLog.emit(f'Algo deu errado! {response} \n Tentando novamente em 2 segundos...')
            sleep(2)
            response = requests.request(method, url, **kwargs)
            if response.status_code == 200:
                self.msgLog.emit(f'Tudo certo, retomando os comandos do BOT.')
        return response

    def get_boards(self) -> dict:
        """
        Retorna uma lista de boards.
        :return: Lista de boards.
        """
        url = f"https://api.trello.com/1/members/me/boards"
        headers = {"Accept": "application/json"}
        query = {
            'key': self.api_key,
            'token': self.api_token
        }

        response = self.send_request("GET", url, headers=headers, params=query)
        response = json.loads(response.text)
        boards = {}
        for board in response:
            boards[board['name']] = board['id']

        self.msgLog.emit(f'{len(boards)} quadros encontrados.')

        return boards

    def get_board_lists(self, idBoard: str) -> json:
        """
        Requisita informações das listas existentes em um quadro ao servidor da API Trello.
        :return: Objeto JSON com os dados das listas encontradas.
        """

        url = f"https://api.trello.com/1/boards/{idBoard}/lists"
        headers = {"Accept": "application/json"}
        query = {
            'key': self.api_key,
            'token': self.api_token
        }

        response = requests.request("GET", url, headers=headers, params=query)
        response = json.loads(response.text)
        lists = {}
        for list_ in response:
            lists[list_['name']] = list_['id']

        self.msgLog.emit(f'{len(lists)} listas encontradas.')

        return lists

    def get_user_name(self):
        url = f"https://api.trello.com/1/members/me"
        headers = {"Accept": "application/json"}
        query = {
            'key': self.api_key,
            'token': self.api_token
        }

        response = requests.request("GET", url, headers=headers, params=query)
        response = json.loads(response.text)
        return response['fullName']

    def get_board(self, idBoard: str, cards='visible') -> json:
        """
        Requisita um único quadro ao servidor da API Trello.
        :return: Objeto JSON com os dados do quadro obtido.
        """

        url = f"https://api.trello.com/1/boards/{idBoard}"
        headers = {"Accept": "application/json"}
        query = {
            'key': self.api_key,
            'token': self.api_token,
            'lists': 'open',
            'cards': cards,
            'labels': 'all'
        }
        response = self.send_request("GET", url, headers=headers, params=query)

        return json.loads(response.text)

    def move_card(self, idCard: str, idList: str, idBoard: str = None, pos: str = 'top'):
        """
        Requisita a transposição de um cartão para uma lista ao servidor da API Trello.
        """

        url = f"https://api.trello.com/1/cards/{idCard}"

        headers = {"Accept": "application/json"}

        query = {
            'key': self.api_key,
            'token': self.api_token,
            'idList': idList,
            'pos': pos
        }
        if idBoard:
            query['idBoard'] = idBoard

        self.send_request("PUT", url, headers=headers, params=query)
        self.msgLog.emit(f'Cartão {idCard} movido.')

