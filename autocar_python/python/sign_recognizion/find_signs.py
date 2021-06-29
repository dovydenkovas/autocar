import cv2 as cv


# def recognize_sign(frame):
#     """
#         Обнаружение контуров дорожных знаков.
#     :param frame:
#     :return:
#     """
#
#
#     # Область в которой ищем дорожный знак.
#     area_sign = (400,     # X-координата вехнего левого угла области
#                  200,     # Y-координата вехнего левого угла области
#                  240,     # Ширина области интереса в пикселях
#                  120)     # Высота области интереса в пикселях
#
#     # Создаём копию кадра "frame"
#     gray = frame(area_sign)  # Необходим для обнаружения контуров.
#     area_frame = frame(area_sign)  # Необходим для распознавания знаков среди контуров.
#
#     # Обозначаем область интереса синим прямоугольником
#     cv2.rectangle(frame, area_sign, (255, 0, 0), 2)

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


#cap = cv.VideoCapture(0)


while cv.waitKey(10) != ord('q'):
    frame = cv.imread("signs.png")

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  # Смена кодировки изображения
    hsv = cv.blur(hsv, (5, 5))  # Размытие для устранения дефектов изображения
    mask = cv.inRange(hsv, (48, 51, 142), (184, 251, 218))  # Бинаризация изображения

    mask = cv.erode(mask, None, iterations=2)  # Устранение мелких белых пятен (случайно совпадающих цветов)
    mask = cv.dilate(mask, None, iterations=4)  # ...
    # cv.imshow("dilate", mask)

    # Поиск контуров
    contours = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    contours = contours[0]  # Из разной информации нас интересуют только контуры
    if contours:
        contours = sorted(contours, key=cv.contourArea, reverse=True)[:10]  # Выбираем 10 самых больших контуров
        #cv.drawContours(frame, contours, -1, (255, 0, 255), 3)

        for contour in contours:
            x, y, w, h = cv.boundingRect(contour)
            roImg = frame[y:y + h, x:x + w]
            cv.imshow(f'{x},{y}', roImg)
            cv.rectangle(frame,(x, y), (x+w, y+h), (0, 0, 255), 2)




    #result = cv.bitwise_and(frame, frame, mask=mask)
    cv.imshow('result', frame)
