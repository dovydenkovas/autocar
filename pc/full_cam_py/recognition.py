import cv2
import numpy as np


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


def count_colors(frame):
    """
        Подсчитывает процентное соотношение красного, *синего и чёрных цветов на вырезанной области.
        :param frame: матрица на которой подсчитываются цвета.
        :return: список из четырех чисел.
    """

    colors = [0, 0, 0, 0]  # количество: красного, синего и черного
    # Считаем количество пикселей красного, синего и чёрного цвета
    for y in range(frame.rows):
        for x in range(frame.cols):
            pixel = frame[y][x]
            # pixel[0] - синяя компонента
            # pixel[1] - зелёная компонента
            # pixel[2] - красная компонента

            # Для определения чёрного цвета
            if pixel[0] <= 100 and abs(pixel[0] - pixel[1]) < 25 and abs(pixel[0] - pixel[2]) < 25 and abs(pixel[2] - pixel[1]) < 25:
                colors[2] += 1

            # Для определения красного цвета
            if pixel[2] > (pixel[1] + pixel[0]) * 0.7:
                colors[0] += 1

            # Для определения синего цвета
            if (pixel[0] - max(pixel[1], pixel[2])) > 10:
                colors[1] += 1

            # Узнаём процентное соотношение цветов
            n_pixels = frame.cols * frame.rows
            colors[0] = colors[0] / n_pixels * 100;
            colors[1] = colors[1] / n_pixels * 100;
            colors[2] = colors[2] / n_pixels * 100;
            return colors


def recognize_sign(frame):
    """
        Обнаружение контуров дорожных знаков.
    :param frame:
    :return:
    """


    # Область в которой ищем дорожный знак.
    area_sign = (400,     # X-координата вехнего левого угла области
                 200,     # Y-координата вехнего левого угла области
                 240,     # Ширина области интереса в пикселях
                 120)     # Высота области интереса в пикселях

    # Создаём копию кадра "frame"
    gray = frame(area_sign)  # Необходим для обнаружения контуров.
    area_frame = frame(area_sign)  # Необходим для распознавания знаков среди контуров.

    # Обозначаем область интереса синим прямоугольником
    cv2.rectangle(frame, area_sign, (255, 0, 0), 2)

    # # Переводим кадр из BGR в оттенки серого
    # cv2.cvtColor(gray, gray, cv2.COLOR_BGR2GRAY)
    # # Массив с найденными контурами на изображении
    # contours = []
    # # Аппроксимированный (упрощенный) контур
    # approx = []
    # # Находим все контуры на изображении
    # cv2.Canny(gray, gray, 70, 210, 3)
    # cv2.findContours(gray, contours, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #
    # # Проходимся по всем найденным контурам в цикле
    # for i in range(len(contours)):
    #     # Аппроксимируем контур до более простой фигуры
    #     cv2.approxPolyDP(contours[i], approx, 3, True)
    #
    #     # Вычисляем площадь контура с помощью функции "contourArea"
    #     area = cv2.contourArea(contours[i])
    #     # Игнорируем слишком маленькие контуры
    #     if area < 480:
    #         continue
    #
    #     # Узнаём, в каком месте кадра находится контур с помощью функции "boundingRect"
    #     boundingarea = cv2.boundingRect(approx)
    #
    #     # Находим соотношение сторон найденного контура
    #     ratio = boundingarea.width / boundingarea.height
    #
    #     # Так как знак квадратный, то и стороны найденного контура должны
    #     # быть равны примерно равны. Если это не так - пропускаем контур.
    #     if ratio < 0.8 or ratio > 1.2:
    #         continue
    #
    #     # Подсчет количества цвета
    #     # Вырезаем из всего кадра область boundingarea
    #     rr = area_frame(boundingarea)
    #     colors = count_colors(rr)
    #
    #     """
    #       Распознавание знаков
    #     """
    #     #  Для определения знака направления движения используется положение стойки стрелки,
    #     #  то есть если стойка стрелки находится слева, то это знак "движение направо" и т.д.
    #     #  Для нахождения положения стойки стрелки используется всего одна строчка пикселей в нижней части знака.
    #     if colors[0] > 40:
    #         print("Stop sign.")
    #     elif colors[2] > 5 and colors[1] > 40:
    #         print("Pedestrian sign.")
    #     elif colors[2] > 60:  # Если более 60% пикселей имеют синий цвет
    #         # Рассчитываем положение строчки пикселей для сканирования
    #         scan_row = rr.rows * 0.7
    #         # Количество белых пикселей в строчке
    #         white_pixels = 0
    #         # Сумма X-координат белых пикселей в строчке
    #         pixels_offset = 0
    #
    #         # Проходимся по пикселям строчки, пропуская 4 первых и 4 последних пикселя
    #         for  offset in range(4, rr.cols - 4):
    #             # Если нашли белый пиксель в строчке
    #             if rr[offset, scan_row][2] > 90 and rr[offset, scan_row][1] > 90 and rr[offset, scan_row][0] > 90:
    #                 # Увеличиваем счетчик белых пикселей на 1
    #                 white_pixels += 1
    #                 # Прибавляем X-координату белого пикселя
    #                 pixels_offset += offset
    #
    #         # Проверяем количество найденных белых пикселей
    #         # Если количество белых пикселей меньше 1
    #         if white_pixels < 1:
    #             continue
    #
    #         # Узнаём положение белой стойки стрелки
    #         center = pixels_offset / white_pixels
    #         # Узнаём положение в процентах
    #         light_position = center / rr.cols
    #
    #         # Определяем, какой знак направления движения нашли
    #         if light_position >= 0.6:
    #             # Знак движения налево
    #             print("Turn left sign")
    #         elif light_position >= 0.4:
    #             # Знак движения прямо
    #             print("Go forward sign")
    #
    #         elif light_position >= 0.0:
    #             # Знак движения направо
    #             print("Turn right sign")
            #cv2.rectangle(frame(area_sign), boundingarea, Scalar(0, 255, 0), 2);
        #else:
        #    rectangle(frame(area_sign), boundingarea, Scalar(0, 0, 255), 2);
