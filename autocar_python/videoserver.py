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

    video_server = NetGear()

    data = {'logs': ''
            }


    while True:
        if not control_queue.empty():
             data['logs'] = control_queue.get()
             message = pickle.dumps(data)
             server.sendto(message, ('<broadcast>', 7777))

        try:
            if not frames_queue.empty():
                frame = frames_queue.get()
                if frame is not None:
                    #frame = cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2))
                    video_server.send(frame)
        except RuntimeError:
            video_server = NetGear()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Ошибка видеосервера: {e}")

        time.sleep(0.01)
