"""
    This file is part of https://github.com/dovydenkovas/autocar project.

    Copyright 2021 The https://github.com/dovydenkovas/autocar contributors


    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

""" Считывает изображение с камеры, находит на нем линии, знаки, светофоры.
    Выбирает необходимое направление движения и рисует опознавательные знаки
    на картинке (отмечает линию, знаки и светофоры). Картинку передает
    в frames_queue, а необходимое направление движения в errors_queue.

"""


import time
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


def mainloop(errors_queue, frames_queue, logs_queue):
    print("Анализатор дороги запустился")

    ret = None
    while not ret:
        capture = cv.VideoCapture(0)
        ret, frame = capture.read()

    line_y1 = int(len(frame) * 0.95)
    line_y2 = int(len(frame) * 0.85)
    center_x = len(frame[0]) // 2
    line_x1 = line_x2 = center_x
    old_x = -1
    n_rows = 10

    while ret:
        # Находит координаты черной линии и помечает чертой
        for i in range(n_rows):
            line_x1 += find_line(frame, line_y1+i, old_x)
            line_x2 += find_line(frame, line_y2+i, old_x)

        line_x1 //= n_rows + 1
        line_x2 //= n_rows + 1

        cv.line(frame, (line_x1, line_y1), (line_x2, line_y2), (250, 120, 120), 3)
        old_x = line_x1

        frames_queue.put(frame)
        ret, frame = capture.read()
        time.sleep(0.025)
