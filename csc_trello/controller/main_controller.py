from datetime import datetime

from csc_trello.view.main_window import MainWindow
from csc_trello.service.trello_service import TrelloService
from csc_trello.service.sansys_service import SansysService
from csc_trello.controller.worker_controller import Worker
from PyQt5.QtCore import QThreadPool


class MainController:
    def __init__(self, trello_key, trello_token, sansys_conn):
        self.sansys_conn = sansys_conn

        self.boards = {}
        self.id_board = None
        self.lists = {}
        self.id_list = None
        self.worker = None

        self.sansys_service = SansysService(self.sansys_conn)
        self.trello_service = TrelloService(trello_key, trello_token)

        self._ui = MainWindow()
        self.print_log('Trello: ' + self.trello_service.get_user_name())

        self.trello_service.msgLog.connect(self.print_log)
        self.populate_cb_boards()

        self._ui.cb_board.activated[str].connect(self.populate_cb_lists)
        self._ui.cb_list.activated[str].connect(self.get_list_id)
        self._ui.btn_start.clicked.connect(self.start_pause)

        self.threadpool = QThreadPool()

    def print_error(self, msg):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        new_log = f'({current_time}) ERRO:\n' + msg
        self._ui.btn_start.setStyleSheet("background:rgb(49, 49, 49);color: red")
        self._ui.lb_log.setText(new_log)

        self.worker.keep_running = False
        self._ui.cb_board.setEnabled(False)
        self._ui.cb_list.setEnabled(False)
        self._ui.btn_start.setEnabled(False)

    def print_log(self, msg):
        current_text = self._ui.lb_log.text()
        n = current_text.count('\n')
        if n > 12:
            current_text = current_text[:current_text.rfind('\n')]

        waiting_tags = [r'-', '\\', r'|', r'/']
        first_msg = current_text[:current_text.find('\n')]
        if first_msg in waiting_tags:
            current_text = current_text[current_text.find('\n') + 1:]
            waiting_tag = waiting_tags[waiting_tags.index(first_msg) - 1]
        else:
            waiting_tag = waiting_tags[0]

        if msg == '':
            new_log = waiting_tag + '\n' + current_text
        else:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            new_log = f'({current_time}) - ' + msg + '\n' + current_text

        self._ui.lb_log.setText(new_log)

    def populate_cb_boards(self):
        self.boards = self.trello_service.get_boards()
        self._ui.cb_board.addItems(sorted(self.boards.keys()))
        self.populate_cb_lists(self._ui.cb_board.currentText())

    def populate_cb_lists(self, board_name):
        self.id_board = self.boards[board_name]
        self.lists = self.trello_service.get_board_lists(self.id_board)

        self._ui.cb_list.clear()
        self._ui.cb_list.addItems(sorted(self.lists.keys()))
        self.get_list_id(self._ui.cb_list.currentText())

    def get_list_id(self, list_name):
        self.id_list = self.lists[list_name]

    def create_worker(self):
        self.worker = Worker(self.sansys_service, self.trello_service)
        self.worker.signals.error.connect(self.print_error)
        self.worker.signals.progress.connect(self.print_log)
        self.worker.setAutoDelete(True)

    def start_pause(self):
        # Check if button is checked
        if self._ui.btn_start.isChecked():
            self._ui.btn_start.setText('Parar')
            self._ui.btn_start.setStyleSheet("background-color: grey;color: black")
            self._ui.cb_board.setEnabled(False)
            self._ui.cb_list.setEnabled(False)

            # Clean the threadpool
            self.threadpool.clear()
            self.create_worker()
            self.worker.id_board = self.id_board
            self.worker.id_list_finished = self.id_list
            self.threadpool.start(self.worker)
            # print(self.threadpool.activeThreadCount())

            self.print_log('Processo iniciado.')
        else:
            self._ui.btn_start.setText('Iniciar')
            self._ui.btn_start.setStyleSheet("")
            self._ui.cb_board.setEnabled(True)
            self._ui.cb_list.setEnabled(True)

            self.worker.keep_running = False

            self.print_log('Processo parado.')
