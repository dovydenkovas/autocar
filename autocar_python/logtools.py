""" Вспомогательные функции для логирования """

import datetime


def get_time():
    return datetime.datetime.now().strftime("[%H:%M:%S]")


def log(message):
    return {'logs': f'{get_time()} {message}\n', 'info': ''}


def command(command):
    return {'logs': '', 'info': command}


def send(message, command):
    return {'logs': f'{get_time()} {message}\n', 'info': command}
