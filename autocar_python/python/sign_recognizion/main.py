import cv2 as cv


def get_mask(image):
    image = cv.resize(image, (128, 128))
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    hsv = cv.blur(hsv, (3, 3))
    mask = cv.inRange(hsv, (20, 140, 20), (250, 250, 250))
    return mask

def count_colors(frame):
    blue = 0
    black = 0
    red = 0
    # Считаем количество пикселей красного, жёлтого, синего, чёрного цвета
    for y in range(len(frame)):
        for x in range(len(frame[0])):
            pixel = frame[y, x]

            # Для определения чёрного цвета
            if ((pixel[0] <= 100 and abs(pixel[0] - pixel[1]) < 25 and
                 abs(pixel[0] - pixel[2]) < 25 and
                 abs(pixel[2] - pixel[1]) < 25)):
                 black += 1
            # Для определения красного цвета
            if (pixel[2] > (pixel[1] + pixel[0]) * 0.7):
                red += 1
            # Для определения синего цвета
            if ((pixel[0] - max(pixel[1], pixel[2])) > 10):
                blue += 1
    # Узнаём процентное соотношение цветов
    count = len(frame) * len(frame[0]) * 100
    red /= count
    blue /= count
    black /= count

    return red, blue, black

sign_pd = get_mask(cv.imread("pr.png"))
sign_stop = get_mask(cv.imread("stop.png"))


def recognize_sign(frame):
    mask = get_mask(frame)

    is_pd = 0
    is_stop = 0
    for y in range(64):
        for x in range(64):
            if mask[y][x].all() == sign_pd[y][x].all():
                is_pd += 1
            if mask[y][x].all() == sign_stop[y][x].all():
                is_stop += 1

    red, blue, black = count_colors(frame)

    if is_pd > 1900 and is_pd > is_stop + 200 and red < 10:
        return f"Pedestrian: {is_pd}"

    elif is_stop > 1900 and is_stop > is_pd + 200 and red > 40:
        return f"Stop: {is_stop}"

    else:
        return f"No sign: {is_pd}, {is_stop}"



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
            sign_type = recognize_sign(roImg)
            if not 'No sign' in sign_type:
                cv.imshow(sign_type, roImg)
            cv.rectangle(frame,(x, y), (x+w, y+h), (0, 0, 255), 2)




    #result = cv.bitwise_and(frame, frame, mask=mask)
    cv.imshow('result', frame)
