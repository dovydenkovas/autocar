"""
    This file is part of https://github.com/dovydenkovas/autocar project.

    Copyright 2021 The https://github.com/dovydenkovas/autocar contributors


    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

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
