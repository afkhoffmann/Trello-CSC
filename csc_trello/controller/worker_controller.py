import sys
import traceback
import re
from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot
from time import sleep


class WorkerSignals(QObject):
    error = pyqtSignal(tuple)
    progress = pyqtSignal(str)


class Worker(QRunnable):
    def __init__(self, sansys_service, trello_service):
        super(Worker, self).__init__()

        self.sansys = sansys_service
        self.trello = trello_service

        self.id_board = None
        self.id_list_finished = None
        self.protocols = None
        self.cards_to_conclude = None

        self.keep_running = True
        self.regex = re.compile('\d{6,8}')
        self.task = 'GET'

        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            while self.keep_running:
                self.manager_tasks()
                for i in range(20):
                    self.signals.progress.emit('')
                    sleep(0.5)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))

    def manager_tasks(self):
        if not self.keep_running:
            return

        if self.task == 'GET':
            self.get_protocols_to_verify()
            self.task = 'VERIFY'

        elif self.task == 'VERIFY':
            self.verify_protocols()
            self.task = 'CONCLUDE'

        elif self.task == 'CONCLUDE':
            self.conclude_cards()
            self.task = 'GET'

    def get_protocols_to_verify(self):
        payload = self.trello.get_board(self.id_board)

        protocols = {}
        for card in payload['cards']:
            if card['idList'] != self.id_list_finished:
                protocol = self.regex.search(card['name'])
                if protocol:
                    protocols[protocol.group()] = card['id']

        self.protocols = protocols

    def verify_protocols(self):
        if not self.protocols:
            self.task = 'GET'
            self.cards_to_conclude = []
            return

        self.sansys.build_query(self.protocols.keys())
        concluded_protocols = self.sansys.execute_query()
        cards_to_conclude = []

        for protocol in concluded_protocols['ID_SERVICO'].to_list():
            cards_to_conclude.append(self.protocols[str(protocol)])

        self.cards_to_conclude = cards_to_conclude

    def conclude_cards(self):
        if not self.cards_to_conclude:
            self.task = 'GET'
            return

        for id_card in self.cards_to_conclude:
            self.trello.move_card(id_card, self.id_list_finished)
