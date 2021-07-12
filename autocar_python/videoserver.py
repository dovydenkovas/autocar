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

def feedback_mainloop(server, control_queue):
    global is_streamig, ip
    while True:
        data, addr = server.recvfrom(1024)
        if len(data) > 0:
             ip = addr[0]
             message = pickle.loads(data)
             if message['command'] == "start_video":
                 #ip = message['ip']
                 is_streamig = True
             elif message['command'] == "stop_video":
                 is_streamig = False
             else:
                 control_queue.put(message)


def mainloop(control_queue, frames_queue, logs_queue):
    """ Отправляет картинку и состояние машинки (broadcast, port 7777)
        TODO: Это тестовый вариант

    """
    global ip, is_streamig
    print("Видео сервер запустился")

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    #server.settimeout(0.2)

    thread = threading.Thread(target=feedback_mainloop, daemon=True, args=(server, control_queue))
    thread.start()


    data = {'logs': '',  # Выводятся как логи
            'info': ''   # Обрабатываются програмно
            }

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
                    if is_streamig and ip:
                        video_server = NetGear(address=ip)
                        print(ip)
                        ip = ''
                    else:
                        #frame = cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2))
                        video_server.send(frame)
        except RuntimeError:
            video_server = NetGear()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Ошибка видеосервера: {e}")

        time.sleep(0.01)
