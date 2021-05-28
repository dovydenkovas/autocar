from vidgear.gears import NetGear
import cv2

def find_line(frame):
    """ Ищет черную линию.
        Принимает кадр.
        Возвращает координату центра черной линии.
    """

    left_side = 100  # Координаты левой границы линии
    right_side = 540  # Координаты правой границы линии
    scan_row = 470

    for x in range(50, len(frame)-50, 2):
        if frame[scan_row][x][2] < 40:
            left_side = x
            break

    for x in range(len(frame)-50, 50, -2):
        if frame[scan_row][x][2] < 40:
            right_side = x
            break

    return (right_side + left_side) // 2


cap = cv2.VideoCapture(0)
server = NetGear()

if cap.isOpened():
    ret, frame = cap.read()
    # Пока пользователь нажал кнопку или кадр не считался, выходим из цикла
    while ret:
        # Находит координаты черной линии и помечает красной чертой
        line_x = find_line(frame)
        cv2.line(frame, (line_x, len(frame)-10), (line_x, len(frame)-50), (0, 0, 255), 3)

        # Выводим кадр в окно "Live"
        server.send(frame)
        # Считываем следующий кадр с видео и записываем в frame
        ret, frame = cap.read()

cap.stop()
server.close()

