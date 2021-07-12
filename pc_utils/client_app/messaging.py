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


class Messager:
    def __init__(self):
        self.message = {'logs': '', 'info': ''}
        self.frame = None
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client.bind(("", 7777))
        self.server_addr = None
        self.data = b''
        self.local_ip = get_network_ip()


    def get_frame(self):
        return self.message['frame']

    def get_logs(self):
        message = self.message['logs']
        self.message['logs'] = ''
        return message

    def send(self, message):
        self.client.sendto(pickle.dumps(message), self.server_addr)


    def connect(self):
        data, addr = self.client.recvfrom(1024)
        if len(data) > 0:
            self.data = data
            self.server_addr = addr
            log_thread = threading.Thread(target=self.log_mainloop, daemon=True)
            log_thread.start()
            video_thread = threading.Thread(target=self.video_mainloop, daemon=True)
            video_thread.start()
            return True
        return False

    def log_mainloop(self):
        while True:
            if len(self.data) > 0:
                 self.message = pickle.loads(self.data)
            self.data, addr = self.client.recvfrom(1024)


    def video_mainloop(self):
        from vidgear.gears import NetGear
        video_client = NetGear(receive_mode=True, address=self.local_ip)
        while True:
            frame = video_client.recv()
            if frame is not None:
                self.frame = frame
