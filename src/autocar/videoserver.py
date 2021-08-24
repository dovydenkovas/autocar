""" Отправляет картинку и состояние машинки (broadcast, port 7777),
    Принимает команды остановки и запуска машинки.

    Изображение получает через frames_queue.
    Отправляет команды и получает состояние через control_queue.

"""

import threading
import socket
import pickle
import time
import cv2

from vidgear.gears import VideoGear, CamGear
from vidgear.gears import NetGear


is_streamig = False
ip = ''
old_ip = 'old ip'

def feedback_mainloop(server, control_queue):
    global is_streamig, ip
    while True:
        data, addr = server.recvfrom(1024)
        if len(data) > 0:
            ip = addr[0]
            message = pickle.loads(data)
            if message[0] == "hi":
                is_streamig = True
            elif message[0] == "buy":
                is_streamig = False
            else:
                control_queue.put(message)
        time.sleep(0.15)


def mainloop(control_queue, frames_queue, logs_queue):
    """ Отправляет картинку и состояние машинки (broadcast, port 7777)  """

    global ip, is_streamig, old_ip
    print("Видео сервер запустился")

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    #server.settimeout(0.2)

    thread = threading.Thread(target=feedback_mainloop, daemon=True, args=(server, control_queue))
    thread.start()


    data = None
    video_server = NetGear()

    while True:
        if not logs_queue.empty():
            data = logs_queue.get()
            message = pickle.dumps(data)
            server.sendto(message, ('<broadcast>', 7777))

        try:
            if not frames_queue.empty():
                frame = frames_queue.get()
                if frame is not None and is_streamig:
                    if is_streamig and ip and ip != old_ip:
                        video_server = NetGear(address=ip)
                        print('Connected to', ip)
                        old_ip = ip
                        ip = ''
                    else:
                        video_server.send(frame)
        except RuntimeError:
            video_server = NetGear()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Ошибка видеосервера: {e}")

        time.sleep(0.02)
