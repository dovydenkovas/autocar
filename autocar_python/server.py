""" Принимает """
from multiprocessing import Process, Queue
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
        self.sock.bind((HOST, PORT))
        self.sock.listen(10)

    def mainloop(self, queue):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        while True:  # Listen for request
            client_socket, addr = self.sock.accept()
            try:
                while True:  # Send frame
                    self.frame = queue.get()

                    if type(self.frame) != None:
                        result, frame = cv2.imencode('.jpg', self.frame, encode_param)
                        data = pickle.dumps(frame, 0)
                        size = len(data)
                        client_socket.sendall(struct.pack(">L", size) + data)
            except BrokenPipeError:
                print("BrokenPipeError (Connection was closed)")
            except ConnectionResetError:
                print("ConnectionResetError (Connection was closed)")




if __name__ == "__main__":
    srv = VideoServer()
    srv.start()

    cam = cv2.VideoCapture(0)

    while True:
        ret, srv.frame = cam.read()

    cam.release()
