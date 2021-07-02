# import cv2
# import socket
# import struct
# import pickle

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


def get_frame():
    return None


def get_logs():
    return "Nothing"


def send(message):
    pass

def connect():
    return False
