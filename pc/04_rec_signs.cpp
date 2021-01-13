/*
 * Распознавание контуров дорожных знаков.
 */
#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

struct SimpleHist {
    int red,
        yellow,
        blue,
        black;

    SimpleHist(int red_ = 0, int yellow_ = 0, int blue_ = 0, int black_ = 0):
        red(red_),
        yellow(yellow_),
        blue(blue_),
        black(black_)
    {
    }
};


// Функция вычисляет процентное соотношение красной, жёлтой, синий, черной
// компоненты на изображении "frame"
SimpleHist count_colors(Mat& frame) {
    SimpleHist colors;
    // Считаем количество пикселей красного, жёлтого, синего, чёрного цвета
	for(size_t y = 0; y < frame.rows; y++) {
		for(size_t x = 0; x < frame.cols; x++) {
            Vec3b pixel = frame.at<Vec3b>(Point(x, y));
            // pixel[0] - синяя компонента
            // pixel[1] - зелёная компонента
            // pixel[2] - красная компонента

            // Для определения чёрного цвета
            /*if ((pixel[0] <= 100 && abs(pixel[0] - pixel[1]) < 25 &&
                 abs(pixel[0] - pixel[2]) < 25 &&
                 abs(pixel[2] - pixel[1]) < 25)) colors.black++;*/
            if (pixel[0] <= 25 and pixel[1] <= 25 and pixel[1] <= 25)
                colors.black++;
			// Для определения красного цвета
            if (pixel[2] > (pixel[1] + pixel[0]) * 0.7)
                colors.red++;
			// Для определения синего цвета
            if ((pixel[0] - max(pixel[1], pixel[2])) > 10)
                colors.blue++;
			// Для определения жёлтого цвета
            if (pixel[1] - pixel[0] > 20 && pixel[2] - pixel[0] > 20)
                colors.yellow++;
		}
	}

    // Узнаём процентное соотношение цветов
	float count = frame.cols * frame.rows;
    colors.red = (float)colors.red / count * 100;
	colors.yellow = (float)colors.yellow / count * 100;
	colors.blue = (float)colors.blue / count * 100;
	colors.black = (float)colors.black / count * 100;
	return colors;
}



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
        if(waitKey(100) >= 0) break;
        if(frame.empty()) continue;

        // Обозначаем область интереса синим прямоугольником
        rectangle(frame, area_sign, Scalar(255, 0, 0), 2);

        // ***** Распознавание дорожных знаков на изображении *****
        SimpleHist colors;
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
        Canny(result, result, 50, 150, 3);
        findContours(result, contours, RETR_TREE, CHAIN_APPROX_SIMPLE);

        // Проходимся по всем найденным контурам в цикле
		for (size_t i = 0; i < contours.size(); i++) {
            // Аппроксимируем контур до более простой фигуры
            approxPolyDP(Mat(contours[i]), approx, 3, true);

            // Вычисляем площадь контура с помощью функции "contourArea"
            double area = fabs(contourArea((Mat)contours[i]));
            // Игнорируем слишком маленькие контуры
            if (area < 400)
                continue;

            // Узнаём, в каком месте кадра находится контур с помощью функции "boundingRect"
			Rect boundingarea = boundingRect(approx);

            // Находим соотношение сторон найденного контура
            double ratio = boundingarea.width / boundingarea.height;

            // Так как знак квадратный, то и стороны найденного контура должны
            // быть равны примерно равны. Если это не так - пропускаем контур.
            if(ratio < 0.8 || ratio > 1.2) continue;

            // Подсчет количества цвета
            // Вырезаем из всего кадра область boundingarea
            Mat rr = copy_frame(boundingarea);

            // Подсчитываем процентное соотношение красного, жёлтого, синего и чёрных цветов на вырезанной области
            // "rr" - область для подсчёта
            // "colors" - структура с соотношением цветов на изображении
            colors = count_colors(rr);

            // ***** Пример распознавания знаков направления движения *****
            // Для определения знака направления движения используется положение стойки стрелки,
            // то есть если стойка стрелки находится слева, то это знак "движение направо" и т.д.
            // Для нахождения положения стойки стрелки используется всего одна строчка пикселей в нижней части знака.

            if (colors.red > 45) {
                cout << "Stop sign." << endl;
                rectangle(frame(area_sign), boundingarea, Scalar(0, 255, 0), 2);
            } else if (colors.blue > 60) { // Если более 60% пикселей имеют синий цвет
                // Рассчитываем положение строчки пикселей для сканирования
                int scan_row = rr.rows * 0.7,
                // Количество белых пикселей в строчке
                    white_pixels = 0,
                // Сумма X-координат белых пикселей в строчке
					pixels_offset = 0;

                // Проходимся по пикселям строчки, пропуская 4 первых и 4 последних пикселя
				for (int offset = 4; offset < (rr.cols - 4); offset++) {
                    // Если нашли белый пиксель в строчке
                    if (
						((rr.at<Vec3b>(Point(offset, scan_row))[2]) > 90) &&
						((rr.at<Vec3b>(Point(offset, scan_row))[1]) > 90) &&
						((rr.at<Vec3b>(Point(offset, scan_row))[0]) > 90))
				    {
                        // Увеличиваем счетчик белых пикселей на 1
					    white_pixels++;
                        // Прибавляем X-координату белого пикселя
					    pixels_offset += offset;
				    }
                }

                // Проверяем количество найденных белых пикселей
                // Если количество белых пикселей меньше 1
				if (white_pixels < 1)
                    continue;

                // Узнаём положение белой стойки стрелки
				float center = pixels_offset / white_pixels;
                // Узнаём положение в процентах
				float light_position = center / rr.cols;

                // Определяем, какой знак направления движения нашли
                if(light_position >= 0.6) {
                    // Знак движения налево
                    cout << "Turn left sign." << endl;
                }else if(light_position >= 0.4) {
                    // Знак движения прямо
                    cout << "Go forward sign." << endl;
                }else if(light_position >= 0.1) {
                    // Знак движения направо
                    cout << "Turn right sign." << endl;
                }
                rectangle(frame(area_sign), boundingarea, Scalar(0, 255, 0), 2);
            } else {
                rectangle(frame(area_sign), boundingarea, Scalar(0, 0, 255), 2);
            }
        }

        imshow("frame", frame);
    }
    return 0;
}
