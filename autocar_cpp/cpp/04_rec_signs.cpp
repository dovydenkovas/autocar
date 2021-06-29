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
        filename = "videos/all_input.avi";
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
        if(waitKey(33) >= 0) break;
        if(frame.empty()) continue;

        // Обозначаем область интереса синим прямоугольником
        rectangle(frame, area_sign, Scalar(255, 0, 0), 2);

        /*
         * Обнаружение контуров дорожных знаков
         */

        // Создаём копию кадра "frame"
        Mat gray = frame(area_sign); // Необходим для обнаружения контуров.
        Mat area_frame = frame(area_sign); // Необходим для распознавания знаков среди контуров.
        //.copyTo(gray);
        //.copyTo(area_frame);
        // Переводим кадр из BGR в оттенки серого
        cvtColor(gray, gray, COLOR_BGR2GRAY);
        // Массив с найденными контурами на изображении
        vector<vector<Point>> contours;
        // Аппроксимированный (упрощенный) контур
        vector<Point> approx;
        // Находим все контуры на изображении
        Canny(gray, gray, 70, 210, 3);
        findContours(gray, contours, RETR_TREE, CHAIN_APPROX_SIMPLE);

        // Проходимся по всем найденным контурам в цикле
		for (size_t i = 0; i < contours.size(); i++) {
            // Аппроксимируем контур до более простой фигуры
            approxPolyDP(Mat(contours[i]), approx, 3, true);

            // Вычисляем площадь контура с помощью функции "contourArea"
            double area = fabs(contourArea((Mat)contours[i]));
            // Игнорируем слишком маленькие контуры
            if (area < 480)
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
            Mat rr = area_frame(boundingarea);

            // Подсчитываем процентное соотношение красного, жёлтого, синего и чёрных цветов на вырезанной области
            // "rr" - область для подсчёта
            int blue = 0;
            int black = 0;
            int red = 0;
            // Считаем количество пикселей красного, жёлтого, синего, чёрного цвета
        	for(size_t y = 0; y < rr.rows; y++) {
        		for(size_t x = 0; x < rr.cols; x++) {
                    Vec3b pixel = rr.at<Vec3b>(Point(x, y));
                    // pixel[0] - синяя компонента
                    // pixel[1] - зелёная компонента
                    // pixel[2] - красная компонента

                    // Для определения чёрного цвета
                    if ((pixel[0] <= 100 && abs(pixel[0] - pixel[1]) < 25 &&
                         abs(pixel[0] - pixel[2]) < 25 &&
                         abs(pixel[2] - pixel[1]) < 25)) black++;
                    // Для определения красного цвета
                    if (pixel[2] > (pixel[1] + pixel[0]) * 0.7)
                        red++;
        			// Для определения синего цвета
                    if ((pixel[0] - max(pixel[1], pixel[2])) > 10)
                        blue++;
        		}
        	}

            // Узнаём процентное соотношение цветов
        	float count = rr.cols * rr.rows;
            red = (float)red / count * 100;
        	blue = (float)blue / count * 100;
        	black = (float)black / count * 100;

            /*
             * Распознавание знаков
             */
            // Для определения знака направления движения используется положение стойки стрелки,
            // то есть если стойка стрелки находится слева, то это знак "движение направо" и т.д.
            // Для нахождения положения стойки стрелки используется всего одна строчка пикселей в нижней части знака.
            cout << "\rb:" << black << "\tbl:" << blue;
            cout << "\tr:" << red << "\t";
            if (red > 40) {
                cout << "Stop sign." << endl;
                rectangle(frame(area_sign), boundingarea, Scalar(0, 255, 0), 2);
            } else if (black > 5 and blue > 40) {
                cout << "Pedestrian sign." << endl;
                rectangle(frame(area_sign), boundingarea, Scalar(0, 255, 0), 2);
            } else if (blue > 60) { // Если более 60% пикселей имеют синий цвет
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
                    cout << "Turn left sign. lp: " << light_position << endl;
                }else if(light_position >= 0.4) {
                    // Знак движения прямо
                    cout << "Go forward sign. lp: " << light_position << endl;
                }else if(light_position >= 0.0) {
                    // Знак движения направо
                    cout << "Turn right sign. lp: " << light_position << endl;
                }
                rectangle(frame(area_sign), boundingarea, Scalar(0, 255, 0), 2);
            } else {
                rectangle(frame(area_sign), boundingarea, Scalar(0, 0, 255), 2);
            }
        }

        imshow("frame", frame);
    }
    cout << endl;
    return 0;
}
