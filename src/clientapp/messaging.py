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

""" Реализует сетевое взаимодействие с машинкой. """

import threading
import socket
import pickle
import time
from collections import deque


def get_network_ip():
    """ Возвращает локалььный ip адрес в виде строки. """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.connect(('<broadcast>', 0))
    return sock.getsockname()[0]


STATUS = ["Нет соединения", "Еду", "Стою", "Ищу Ардуинку"]


class Messager:
    """
        Содержит методы для коммуникации с
        машинкой и информацию, полученную с ней.
    """

    def __init__(self):
        self.message = None
        self.logs = ''
        self.params = [0, 0, 0, 0]

        self.frame = None
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client.bind(("", 7777))
        self.server_addr = None
        self.data = b''
        self.local_ip = get_network_ip()
        self.is_connected = False # Есть ли соединение
        self.is_running = False  # Движется ли машинка
        self.autocar_status = 0  # Информация о текущес состоянии соединения/машинки
        self.autocar_error = 0  # Степень отклонения машинки от линии
        self.sending_messages = deque() # Сообщения для отправки на машинку

    def get_frame(self):
        return self.frame

    def get_logs(self):
        if len(self.logs) > 0:
            result = self.logs + '\n'
            self.logs = ''
            return result
        return ''

    def send(self, message):
        """ Добавляет сообщение в очередь на отправку. """
        self.sending_messages.append(message)

    def _send(self):
        """ Отправляет сообщения из очереди на машинку. """
        while True:
            if len(self.sending_messages) > 0:
                message = self.sending_messages.popleft()
                self.client.sendto(pickle.dumps(message), self.server_addr)
            time.sleep(0.25)

    def send_quickly(self, message):
        """ Отправляет сообщение на машинку минуя очередь сообщений.
            ВНИМАНИЕ: рекомендуется испольщовать только
                      для отправки сообщений на завершение.
        """
        self.client.sendto(pickle.dumps(message), self.server_addr)

    def open(self):
        """ Открывает соединение с машинкой. """
        log_thread = threading.Thread(target=self.log_mainloop, daemon=True)
        log_thread.start()
        return False

    def log_mainloop(self):
        """ В случае успешного подключения создает потоки приема
            видео с машики и передачи команд на машинку, после чего
            в цикле принимает входящую информацию.
        """

        data, addr = self.client.recvfrom(1024)
        if len(data) <= 0:
            # Connection failed
            return

        self.is_connected = True
        self.data = data
        self.server_addr = addr

        video_thread = threading.Thread(target=self.video_mainloop, daemon=True)
        video_thread.start()

        send_thread = threading.Thread(target=self._send, daemon=True)
        send_thread.start()

        self.send(('hi',))
        self.send(('get',))

        # Log mainloop
        while True:
            if len(self.data) > 0:
                self.message = pickle.loads(self.data)
                if self.message[0] == 'log':
                    self.logs = self.message[1]
                elif self.message[0] == 'arg':
                    self.autocar_status, self.autocar_error, *_ = self.message[1:]
                    self.is_running = self.autocar_status == 1
                elif self.message[0] == 'var':
                    self.params = self.message[1:]
            self.data, addr = self.client.recvfrom(1024)
        time.sleep(0.15)


    def video_mainloop(self):
        """ Принимет изображение с машинки и сохраняет его в self.frame. """
        from vidgear.gears import NetGear
        video_client = NetGear(receive_mode=True, address=self.local_ip)
        while True:
            frame = video_client.recv()
            if frame is not None:
                self.frame = frame

    def close(self):
        """ Завершает соединение с машинкой. """
        if self.is_connected:
            self.send_quickly(('buy',))
