""" Отправляет картинку и состояние машинки (broadcast, port 7777),
    Принимает команды остановки и запуска машинки.

    Изображение получает через frames_queue.
    Отправляет команды и получает состояние через control_queue.

"""

import socket
import pickle
import time


def mainloop(control_queue, frames_queue):
    """ Отправляет картинку и состояние машинки (broadcast, port 7777)
        TODO: Это тестовый вариант

    """
    print("Видео сервер запустился")

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.settimeout(0.2)

    data = {'frame': [],
            'logs': ''
            }


    while True:
        if not frames_queue.empty():
            data['frame'] = [1,2,3] #frames_queue.get()

        data['logs'] = control_queue.get() if not control_queue.empty() else ""

        message = pickle.dumps(data)
        server.sendto(message, ('<broadcast>', 7777))
        time.sleep(1)
