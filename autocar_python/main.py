""" Главный файл программы.
Создает процессы:
1. Видиосервера
2. Следования по линии
"""

from multiprocessing import Process, Queue
import cv2

import server
import line
import recognition


class AutoCar:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.video_server = server.VideoServer()

        self.queue = Queue()
        self.video_server_process = Process(target=self.video_server.mainloop, args=(self.queue,))


    def mainloop(self):
        ret, frame = self.cap.read()
        line_y1 = int(len(frame) * 0.95)
        line_y2 = int(len(frame) * 0.85)
        center_x = len(frame[0]) // 2
        line_x1 = line_x2 = center_x
        old_x = -1
        n_rows = 10

        while ret:
            ret, frame = self.cap.read()

            # Находит координаты черной линии и помечает чертой
            for i in range(n_rows):
                line_x1 += recognition.find_line(frame, line_y1+i, old_x)
                line_x2 += recognition.find_line(frame, line_y2+i, old_x)

            line_x1 //= n_rows + 1
            line_x2 //= n_rows + 1

            cv2.line(frame, (line_x1, line_y1), (line_x2, line_y2), (250, 120, 120), 3)
            old_x = line_x1

            self.queue.put(frame)



if __name__ == "__main__":
    car = AutoCar()
    car.mainloop()




# # Читаем видео из файла
# cap = cv2.VideoCapture("../cpp/videos/all_input.avi")
#
# if cap.isOpened():
#     ret, frame = cap.read()
#     line_y1 = int(len(frame) * 0.95)
#     line_y2 = int(len(frame) * 0.85)
#     center_x = len(frame[0]) // 2
#     line_x1 = line_x2 = center_x
#     old_x = -1
#     n_rows = 10
#
#     # Пока пользователь нажал кнопку или кадр не считался, выходим из цикла
#     while cv2.waitKey(20) != ord('q') and ret:
#         # Находит координаты черной линии и помечает чертой
#
#         for i in range(n_rows):
#             line_x1 += recognition.find_line(frame, line_y1+i, old_x)
#             line_x2 += recognition.find_line(frame, line_y2+i, old_x)
#
#         line_x1 //= n_rows + 1
#         line_x2 //= n_rows + 1
#
#         cv2.line(frame, (line_x1, line_y1), (line_x2, line_y2), (250, 120, 120), 3)
#         old_x = line_x1
#
#         # Распознает знаки
#         sign_type, *sign_coords = recognition.recognize_sign(frame)
#         if sign_type:
#             cv2.rectangle(frame, *sign_coords, (120, 250, 120), 3)
#             cv2.putText(frame, sign_type, (sign_coords[0][0]+10, sign_coords[1][1]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.95, (120, 250, 120), 2)
#             print(f'{sign_type} at {sign_coords}')
#
#         # Выводим кадр в окно "Live"
#         cv2.imshow("Recognition", frame)
#         # Считываем следующий кадр с видео и записываем в frame
#         ret, frame = cap.read()
