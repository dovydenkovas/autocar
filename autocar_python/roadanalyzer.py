""" Считывает изображение с камеры, находит на нем линии, знаки, светофоры.
    Выбирает необходимое направление движения и рисует опознавательные знаки
    на картинке (отмечает линию, знаки и светофоры). Картинку передает
    в frames_queue, а необходимое направление движения в errors_queue.

"""


import cv2 as cv


def find_line(frame, scan_row, old_center=-1):
    """ Ищет черную линию.
        Принимает кадр.
        Возвращает координату центра черной линии.

    """

    left_side = 100  # Координаты левой границы линии
    right_side = 540  # Координаты правой границы линии

    if old_center == -1:
        old_center = len(frame[0]) // 2
    left_border = max(int(len(frame[0]) * 0.05), old_center - int(len(frame[0]) * 0.25))
    right_border = min(int(len(frame[0]) * 0.95), old_center + int(len(frame[0]) * 0.25))

    for x in range(left_border, right_border, 2):
        if frame[scan_row][x][2] < 60:
            left_side = x
            break

    for x in range(right_border, left_border, -2):
        if frame[scan_row][x][2] < 60:
            right_side = x
            break

    return (right_side + left_side) // 2


def mainloop(errors_queue, frames_queue):
    print("Аналищатор дороги запустился")
    capture = cv.VideoCapture("videos/all_input.avi")
    ret, frame = capture.read()

    line_y1 = int(len(frame) * 0.95)
    line_y2 = int(len(frame) * 0.85)
    center_x = len(frame[0]) // 2
    line_x1 = line_x2 = center_x
    old_x = -1
    n_rows = 10

    while True:
        ret, frame = capture.read()

        if ret and False:
            # Находит координаты черной линии и помечает чертой
            for i in range(n_rows):
                line_x1 += find_line(frame, line_y1+i, old_x)
                line_x2 += find_line(frame, line_y2+i, old_x)

            line_x1 //= n_rows + 1
            line_x2 //= n_rows + 1

            cv.line(frame, (line_x1, line_y1), (line_x2, line_y2), (250, 120, 120), 3)
            old_x = line_x1
