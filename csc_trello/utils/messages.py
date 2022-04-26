from PyQt5.QtWidgets import QLabel


def error_msg(label: QLabel, msg):
    """
    Mensagem de erro (vermelho)
    :param label: label (QLabel) a ser exibido a mensagem
    :param msg: Mensagem a ser exibida
    :return:
    """
    label.setText(f'<font color=red>{msg}</font>')


def info_msg(label: QLabel, msg):
    """
    Mensagem de informação (azul)
    :param label: label (QLabel) a ser exibido a mensagem
    :param msg: Mensagem a ser exibida
    :return:
    """
    label.setText(f'<font color="#5d9cec">{msg}</font>')


def attention_msg(label: QLabel, msg):
    """
    Mensagem de atenção (amarelo)
    :param label: label (QLabel) a ser exibido a mensagem
    :param msg: Mensagem a ser exibida
    :return:
    """
    label.setText(f'<font color="#f6bb42">{msg}</font>')


def custom_msg(label: QLabel, msg, color_hex=None):
    """
    Mensagem de customizada
    :param label: label (QLabel) a ser exibido a mensagem
    :param msg: Mensagem a ser exibida
    :param color_hex: Cor em hexadecimal para o label, caso não informado será na cor preta (black)
    :return:
    """
    label.setText(f'<font color="{color_hex if color_hex else "black"}">{msg}</font>')
