import cv2
import recognition


# Читаем видео из файла
cap = cv2.VideoCapture("../videos/black_line.avi")

if cap.isOpened():
    ret, frame = cap.read()
    # Пока пользователь нажал кнопку или кадр не считался, выходим из цикла
    while cv2.waitKey(20) != ord('q') and ret:
        # Находит координаты черной линии и помечает красной чертой
        line_x = recognition.find_line(frame)
        cv2.line(frame, (line_x, len(frame)-10), (line_x, len(frame)-50), (0, 0, 255), 3)

        sign_type, sign_coords = recognition.recognize_sign(frame)
        if sign_type:
            print(f'{sign_type} at {sign_coords}')

        # Выводим кадр в окно "Live"
        cv2.imshow("Recognition", frame)
        # Считываем следующий кадр с видео и записываем в frame
        ret, frame = cap.read()

