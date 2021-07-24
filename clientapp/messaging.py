import threading
import socket
import pickle
import time
import struct
#import cv2

def get_network_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]


STATUS = ["Нет соединения", "Еду", "Стою", "Ищу Ардуинку"]

class Messager:
    def __init__(self):
        self.message = None
        self.logs = ''
        self.params = [0, 0, 0, 0]

        self.frame = None
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # (Dont Work in Windows):
        # self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client.bind(("", 7777))
        self.server_addr = None
        self.data = b''
        self.local_ip = get_network_ip()
        self.is_connected = False # Есть ли соединение
        self.is_running = False  # Движется ли машинка
        self.autocar_status = 0  # Информация о текущес состоянии соединения/машинки
        self.autocar_error = 0  # Степень отклонения машинки от линии


    def get_frame(self):
        return self.frame

    def get_logs(self):
        if len(self.logs) > 0:
            _ = self.logs + '\n'
            self.logs = ''
            return _
        return ''

    def send(self, message):
        self.client.sendto(pickle.dumps(message), self.server_addr)


    def connect(self):
        log_thread = threading.Thread(target=self.log_mainloop, daemon=True)
        log_thread.start()
        return False

    def log_mainloop(self):
        data, addr = self.client.recvfrom(1024)
        if len(data) <= 0:
            # Connection failed
            return

        self.is_connected = True
        self.data = data
        self.server_addr = addr

        video_thread = threading.Thread(target=self.video_mainloop, daemon=True)
        video_thread.start()

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
                 elif self.message[0] == 'var':
                     self.params = self.message[1:]
            self.data, addr = self.client.recvfrom(1024)
        time.sleep(0.05)


    def video_mainloop(self):
        from vidgear.gears import NetGear
        video_client = NetGear(receive_mode=True, address=self.local_ip)
        while True:
            frame = video_client.recv()
            if frame is not None:
                self.frame = frame
