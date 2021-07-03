import threading
import socket
import pickle
import time
import struct
#import cv2


class Messager:
    def __init__(self):
        self.message = {'logs': ''}
        self.frame = None
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client.bind(("", 7777))
        self.data = b''

    def get_frame(self):
        return self.message['frame']

    def get_logs(self):
            _ = self.message['logs']
            self.message['logs'] == ''
            return _

    def send(self, message):
        pass
    #__client.sendto(message.encode(), ('<broadcast>', 7777))


    def connect(self):
        data, addr = self.client.recvfrom(9000)
        if len(data) > 0:
            self.data = data
            thread = threading.Thread(target=self.mainloop, daemon=True)
            thread.start()
            return True
        return False

    def mainloop(self):
        from vidgear.gears import NetGear
        client = NetGear(receive_mode = True)

        while True:
            self.message = pickle.loads(self.data)
            self.data, addr = self.client.recvfrom(9000)

            frame = client.recv()
            if frame is None:
                continue
            self.frame = frame


def get_video():

    import cv2



    while True:
        frame = client.recv()
        if frame is None:
            continue


        cv2.imshow("Output Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
    client.close()


if __name__ == '__main__':
    get_video()



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
