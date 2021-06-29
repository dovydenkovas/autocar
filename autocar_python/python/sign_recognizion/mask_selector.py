# 48 51 142 184 251 218
import cv2 as cv


def nothing(x):
    pass

#cap = cv.VideoCapture(0)

cv.namedWindow('result')

cv.createTrackbar("min blue", 'result', 0, 255, nothing)
cv.createTrackbar("min green", 'result', 0, 255, nothing)
cv.createTrackbar("min red", 'result', 0, 255, nothing)

cv.createTrackbar("max blue", 'result', 0, 255, nothing)
cv.createTrackbar("max green", 'result', 0, 255, nothing)
cv.createTrackbar("max red", 'result', 0, 255, nothing)

while cv.waitKey(10) != ord('q'):
    minb = cv.getTrackbarPos('min blue', 'result')
    ming = cv.getTrackbarPos('min green', 'result')
    minr = cv.getTrackbarPos('min red', 'result')

    maxb = cv.getTrackbarPos('max blue', 'result')
    maxg = cv.getTrackbarPos('max green', 'result')
    maxr = cv.getTrackbarPos('max red', 'result')

    frame = cv.imread("img/2_signs.png")
    frame = cv.resize(frame, (400, 200))

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  # Смена кодировки изображения
    hsv = cv.blur(hsv, (5, 5))  # Размытие для устранения дефектов изображения
    mask = cv.inRange(hsv, (minb, ming, minr), (maxb, maxg, maxr))

    maskEr = cv.erode(mask, None, iterations=2)

    maskDi = cv.dilate(maskEr, None, iterations=4)
    cv.imshow("dilate", maskDi)

    result = cv.bitwise_and(frame, frame, mask=mask)
    cv.imshow('result', result)

# cap.release()
cv.destroyAllWindows()