/*
 * Распознавание контуров дорожных знаков.
 */
#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;


struct Colors {
    int black = 0;
    int blue = 0;
    int red = 0;
};


enum Sign {NONE, FORWARD, RIGHT, LEFT, STOP, PEDESTRIAN};


Colors count_colors(Mat &frame)
{
    /*
     * Подсчитываем процентное соотношение красного,
     * синего и чёрных цветов на вырезанной области.
     */

    Colors colors;
    // Считаем количество пикселей красного, жёлтого, синего, чёрного цвета
    for(size_t y = 0; y < frame.rows; y++) {
        for(size_t x = 0; x < frame.cols; x++) {
            Vec3b pixel = frame.at<Vec3b>(Point(x, y));
            // pixel[0] - синяя компонента
            // pixel[1] - зелёная компонента
            // pixel[2] - красная компонента

            // Для определения чёрного цвета
            if ((pixel[0] <= 100 && abs(pixel[0] - pixel[1]) < 25 &&
                 abs(pixel[0] - pixel[2]) < 25 &&
                 abs(pixel[2] - pixel[1]) < 25)) colors.black++;
            // Для определения красного цвета
            if (pixel[2] > (pixel[1] + pixel[0]) * 0.7)
                colors.red++;
            // Для определения синего цвета
            if ((pixel[0] - max(pixel[1], pixel[2])) > 10)
                colors.blue++;
        }
    }

    // Узнаём процентное соотношение цветов
    float count = frame.cols * frame.rows;
    colors.red = (float)colors.red / count * 100;
    colors.blue = (float)colors.blue / count * 100;
    colors.black = (float)colors.black / count * 100;
    return colors;
}


Sign recognize_sign(Mat &frame)
{
    /*
     * Обнаружение контуров дорожных знаков
     */
    // Область в которой ищем дорожный знак.

    Rect area_sign(400,     // X-координата вехнего левого угла области
                   200,     // Y-координата вехнего левого угла области
                   240,     // Ширина области интереса в пикселях
                   120);    // Высота области интереса в пикселях

    // Создаём копию кадра "frame"
    Mat gray = frame(area_sign); // Необходим для обнаружения контуров.
    Mat area_frame = frame(area_sign); // Необходим для распознавания знаков среди контуров.

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
        Colors colors = count_colors(rr);

        /*
         * Распознавание знаков
         */
        // Для определения знака направления движения используется положение стойки стрелки,
        // то есть если стойка стрелки находится слева, то это знак "движение направо" и т.д.
        // Для нахождения положения стойки стрелки используется всего одна строчка пикселей в нижней части знака.
        // cout << "\rb:" << colors.black << "\tbl:" << colors.blue;
        // cout << "\tr:" << colors.red << "\t";
        if (colors.red > 40) {
            // cout << "Stop sign." << endl;
            return STOP;
        } else if (colors.black > 5 and colors.blue > 40) {
            // cout << "Pedestrian sign." << endl;
            return PEDESTRIAN;
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
                //cout << "Turn left sign. lp: " << light_position << endl;
                return LEFT;
            }else if(light_position >= 0.4) {
                // Знак движения прямо
                //cout << "Go forward sign. lp: " << light_position << endl;
                return FORWARD;
            }else if(light_position >= 0.0) {
                // Знак движения направо
                //cout << "Turn right sign. lp: " << light_position << endl;
                return RIGHT;
            }
        }
    }
    return NONE;
}


int find_line(const cv::Mat &frame, int last_line)
{
    /*
     * Принимает кадр и высоту сканирования.
     * Возвращает координаты правой и левой границ черной линии.
     */
    const int scan_row = 470;
    int left_side = 100;
    int right_side = 540;

    // Поиск левой границы черной линии
    for (int x=last_line-100; x<last_line+100; x+=2) {
         // Если количество красного < 40
        if (frame.at<cv::Vec3b>(cv::Point(x, scan_row))[2] < 40) {
            left_side = x;
            break;
        }
    }

    // Поиск правой границы черной линии
    for (int x=last_line+100; x>last_line-100; x-=2) {
        // Если количество красного < 40
        if (frame.at<cv::Vec3b>(cv::Point(x, scan_row))[2] < 40) {
            right_side = x;
            break;
        }
    }

    // Новое значение равно среднему координат краев.
    // Окончательный результат - среднее между новым и старым значением.
    int line = (left_side + right_side) / 2;
    return (line + last_line) / 2;
}


int main(int argc, char *argv[])
{
    // Считывание имени входного файла из аргумента командной строки.
    string filename;
    if (argc > 1) {
        filename = argv[1];
    } else {
        filename = "videos/all_input.avi";
    }

   Mat frame;
   VideoCapture cap(filename);

   int line = 320; // Координаты ценра линии
   int last_line = 320; // Координаты центра линии на предыдущем шаге
   int after_sign = 1000;
   string sign_types[5] = {"Forward", "Right", "Left", "STOP", "Pedestrian"};
   Sign sign;

   if(!cap.isOpened()) {
        cout << "Unable to open video source" << endl;
        return 1;
    }

    // Устанавливаем размер кадров, которые будем считывать с веб-камеры
    cap.set(cv::CAP_PROP_FRAME_WIDTH, 640);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 480);

    while(true) {
        cap.read(frame);
        if(waitKey(33) >= 0) break; // примерно 30 кадров в секунду.
        if(frame.empty()) continue;

        // Нахождение черной линии
        line = find_line(frame, last_line);
        last_line = line;
        cv::line(frame, cv::Point(line, frame.rows), cv::Point(line, frame.rows-50), cv::Scalar(255, 0, 0), 3);

        // Распознование знаков
        // Если после последнего знака прошло больше 20 итераций
        if (after_sign > 20) {
            after_sign = 20;
            sign = recognize_sign(frame); // Распознать знак
            if(sign != NONE) { // Если получилось
                cout << sign_types[sign-1] << endl; // Выводим его тип
                after_sign = 0; 
            }
        }
        after_sign++;

        imshow("frame", frame);
    }
    cout << endl;
    return 0;
}
