""" Принимает """
import socket
import cv2
import pickle
import struct
from threading import Thread


class VideoServer:
    def __init__(self):
        self.frame = None
        HOST = ''
        PORT = 7777

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')
        self.sock.bind((HOST, PORT))
        print('Socket bind complete')
        self.sock.listen(10)
        print('Socket now listening')

    def mainloop(self):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        while True:
            conn, addr = self.sock.accept()
            try:
                while True:
                    if type(self.frame) != None:
                        result, frame = cv2.imencode('.jpg', self.frame, encode_param)
                        data = pickle.dumps(frame, 0)
                        size = len(data)
                        conn.sendall(struct.pack(">L", size) + data)
            except BrokenPipeError:
                print("BrokenPipeError (Connection was closed)")
            except ConnectionResetError:
                print("ConnectionResetError (Connection was closed)")

    def start(self):
        th = Thread(target=self.mainloop, daemon=True)
        th.start()


if __name__ == "__main__":
    srv = VideoServer()
    srv.start()

    cam = cv2.VideoCapture(0)

    while True:
        ret, srv.frame = cam.read()

    cam.release()

