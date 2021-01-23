/*
 * Распознавание контуров дорожных знаков.
 */
#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;


int main(int argc, char *argv[]) {
    // Считывание имени входного файла из аргумента командной строки.
    string filename;
    if (argc > 1) {
        filename = argv[1];
    } else {
        filename = "videos/stop_sign.avi";
    }

    // Область в которой ищем дорожный знак.
    Rect area_sign(400,     // X-координата вехнего левого угла области
                   200,     // Y-координата вехнего левого угла области
                   240,     // Ширина области интереса в пикселях
                   120);    // Высота области интереса в пикселях

   Mat frame;
   VideoCapture cap(filename);

   if(!cap.isOpened()) {
        cout << "Unable to open video source" << endl;
        return 1;
    }

    // Устанавливаем размер кадров, которые будем считывать с веб-камеры
    cap.set(cv::CAP_PROP_FRAME_WIDTH, 640);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 480);

    while(true) {
        cap.read(frame);
        if(waitKey(50) >= 0) break;
        if(frame.empty()) continue;

        // Обозначаем область интереса синим прямоугольником
        rectangle(frame, area_sign, Scalar(255, 0, 0), 2);

        // ***** Распознавание дорожных знаков на изображении *****
        // SimpleHist colors;
        // Создаём копию кадра "frame"
        Mat result, copy_frame;
        frame(area_sign).copyTo(result);
        frame(area_sign).copyTo(copy_frame);
        // Переводим кадр из BGR в оттенки серого
        cvtColor(result, result, COLOR_BGR2GRAY);
        // Массив с найденными контурами на изображении
        vector<vector<Point>> contours;
        // Аппроксимированный контур
        vector<Point> approx;
        // Находим все контуры на изображении
        Canny(result, result, 50, 150, 5);
        findContours(result, contours, RETR_TREE, CHAIN_APPROX_SIMPLE);

        // Проходимся по всем найденным контурам в цикле
		for (size_t i = 0; i < contours.size(); i++) {
            // Аппроксимируем контур до более простой фигуры
            // "contours" - входной контур для аппроксимации
            // "approx" - выходной аппроксимированный контур
            approxPolyDP(Mat(contours[i]), approx, 3, true);

            // Вычисляем площадь контура с помощью функции "contourArea"
            // "fabs" возвращает положительное значение
            // (беззнаковое) с плавающей точкой (поэтому не "abs")
            // "area" - площадь контура
            double area = fabs(contourArea((Mat)contours[i]));
            // Игнорируем слишком маленькие контуры
            if (area < 400)
                continue;

            // Узнаём, в каком месте кадра находится контур с помощью функции "boundingRect"
            // "approx" - контур, расположение которого необходимо узнать
            // "boundingarea" - область, в которой находится контур
            // "boundingarea.x" - x координата верхнего левого края области
            // "boundingarea.y" - y координата верхнего левого края области
            // "boundingarea.width" - ширина области
            // "boundingarea.height" - высота области
			Rect boundingarea = boundingRect(approx);

            // Находим соотношение сторон найденного контура
            double ratio = boundingarea.width / boundingarea.height;

            // Так как знак квадратный, то и стороны найденного контура должны
            // быть равны примерно равны. Если это не так - пропускаем контур.
            if(ratio < 0.8 || ratio > 1.2) continue;

            rectangle(frame(area_sign), boundingarea, Scalar(0, 0, 255), 2);
        }

        imshow("frame", frame);
    }
    return 0;
}
