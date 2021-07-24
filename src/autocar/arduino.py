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
