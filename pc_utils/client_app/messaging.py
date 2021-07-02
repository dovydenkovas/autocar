import threading
import socket
import pickle
import time
import struct


__message = {'frame': None, 'logs': ''}
__client = None


def get_frame():
    return __message['frame']


def get_logs():
    _ = __message['logs']
    __message['logs'] == ''
    return _



def send(message):
    pass
    #__client.sendto(message.encode(), ('<broadcast>', 7777))


def connect():
    global __client
    thread = threading.Thread(target=mainloop, daemon=True)
    thread.start()
    time.sleep(0.5)
    return __message['frame'] != None


def mainloop():
    global __client, __message
    __client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
    __client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    __client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    __client.bind(("", 7777))
    while True:
        data, addr = __client.recvfrom(9000)
        __message = pickle.loads(data)


    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.connect(('10.1.1.1', 7777))
    # connection = sock.makefile('wb')
    #
    # data = b""
    # payload_size = struct.calcsize(">L")
    # while True:
    #     while len(data) < payload_size:
    #         print("Recv: {}".format(len(data)))
    #         data += sock.recv(1024)
    #
    #     packed_msg_size = data[:payload_size]
    #     data = data[payload_size:]
    #     msg_size = struct.unpack(">L", packed_msg_size)[0]
    #     while len(data) < msg_size:
    #         data += sock.recv(1024)
    #     frame_data = data[:msg_size]
    #     data = data[msg_size:]
    #
    #     frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    #     frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    #
    #     cv2.imshow('VideoCar',frame)
    #     cv2.waitKey(1)
