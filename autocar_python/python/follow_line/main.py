import cv2
from arduino import Arduino


def find_line(frame):
    """ Ищет черную линию.
        Принимает кадр.
        Возвращает координату центра черной линии.
    """

    left_side = len(frame[0]) // 10  # Координаты левой границы линии
    right_side = len(frame[0]) // 10 * 9  # Координаты правой границы линии
    scan_row = 470

    for x in range(50, len(frame[0])-50, 2):
        if frame[scan_row][x][2] < 40:
            left_side = x
            break

    for x in range(len(frame[0])-50, 50, -2):
        if frame[scan_row][x][2] < 40:
            right_side = x
            break

    return (right_side + left_side) // 2



arduino = Arduino()
cap = cv2.VideoCapture(0)


if not arduino.isOpened():
    print("Ардуинка не обнаружена")
else:
    print("Соединение установлено")
    speed = 50

    ret, frame = cap.read()
    while ret:
        line_x = find_line(frame) 
        print("Координата линии:", line_x)
        arduino.run(speed, 90+line_x)
        ret, frame = cap.read()

