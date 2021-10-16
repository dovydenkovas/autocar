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

""" Класс для упраления ардуинкой.
    Осуществляет подключение к ардуинке и отправку команд управления.
"""
import serial


class Arduino:
    def __init__(self, port="/dev/ttyUSB0"):
        try:
            self.serial = serial.Serial(port, 115200, timeout=1)
        except:
            self.serial = None

    def isOpened(self):
        return self.serial != None

    def run(self, speed, angle=90):
        direction = 0 if speed >= 0 else 1
        angle = min(125, max(65, angle))
        command = f"SPD {angle}, {direction}, {abs(speed)} "
        self.serial.write(command.encode())
