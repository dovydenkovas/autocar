import cv2
import recognition


# Читаем видео из файла
cap = cv2.VideoCapture("../cpp/videos/all_input.avi")

if cap.isOpened():
    ret, frame = cap.read()
    line_y1 = int(len(frame) * 0.95)
    line_y2 = int(len(frame) * 0.85)
    old_x = -1

    # Пока пользователь нажал кнопку или кадр не считался, выходим из цикла
    while cv2.waitKey(20) != ord('q') and ret:
        # Находит координаты черной линии и помечает красной чертой

        line_x1 = recognition.find_line(frame, line_y1, old_x)
        line_x2 = recognition.find_line(frame, line_y2, line_x1)
        cv2.line(frame, (line_x1, line_y1), (line_x2, line_y2), (250, 120, 120), 3)
        old_x = line_x1

        #sign_type, sign_coords = recognition.recognize_sign(frame)
        #if sign_type:
        #    print(f'{sign_type} at {sign_coords}')

        # Выводим кадр в окно "Live"
        cv2.imshow("Recognition", frame)
        # Считываем следующий кадр с видео и записываем в frame
        ret, frame = cap.read()

