""" Отправляет картинку и состояние машинки (broadcast, port 7777),
    Принимает команды остановки и запуска машинки.

    Изображение получает через frames_queue.
    Отправляет команды и получает состояние через control_queue.

"""

import socket
import pickle
import time
import cv2

from vidgear.gears import VideoGear, CamGear
from vidgear.gears import NetGear


def mainloop(control_queue, frames_queue):
    """ Отправляет картинку и состояние машинки (broadcast, port 7777)
        TODO: Это тестовый вариант

    """
    print("Видео сервер запустился")

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.settimeout(0.2)

    stream = CamGear(0).start()
    video_server = NetGear()

    data = {'logs': ''
            }


    while True:
        # if not frames_queue.empty():
        #     data['frame'] = [1,2,3] #frames_queue.get()

        data['logs'] = control_queue.get() if not control_queue.empty() else ""

        message = pickle.dumps(data)
        server.sendto(message, ('<broadcast>', 7777))

        try:
            frame = stream.read()
            frame = cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2))
            if frame is None:
                break
            video_server.send(frame)

        except KeyboardInterrupt:
            stream.stop()
            break

        time.sleep(0.05)
