""" Вспомогательные функции для логирования """

import datetime


def get_time():
    return datetime.datetime.now().strftime("[%H:%M:%S] ")


def log(message):
    return ('log', get_time() + message)


def arg(*args):
    return ('arg', *args)


def var(*vars):
    return ('var', *vars)
