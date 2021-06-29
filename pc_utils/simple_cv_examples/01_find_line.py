import cv2

# Читаем видео из файла
cap = cv2.VideoCapture("videos/black_line.avi")

if cap.isOpened():
    while True:
        # Считываем кадр с видео и записываем в frame
        ret, frame = cap.read()

        # Если пользователь нажал кнопку или кадр не считался, выходим из цикла
        if cv2.waitKey(20) == ord('q') or not ret:
            break

        # Выводим кадр в окно "Live"
        cv2.imshow("Live", frame);

