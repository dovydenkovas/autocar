/**
 * Обнаружение черной линии, распознавание знаков и цветов светофора.
 */
#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

// Структура для хранения процентного соотношения цветов в изображении.
struct Colors {
    int black = 0;
    int blue = 0;
    int red = 0;
    int yellow = 0;
};

// Структура для хранения результатов поиска знаков и светофоров.
enum Sign {NONE=0, FORWARD, RIGHT, LEFT, STOP,
           PEDESTRIAN, TR_RED, TR_YELLOW, TR_GREEN};


/**
 * Принимает фрагмент изображения и
 * возвращает количество красного, черного, синего и желтого в изображении.
 */
Colors count_colors(Mat &frame);

/**
 * Принимает фрагмент изображения, содержащий только знак и
 * возвращает тип знака или NONE в случае его отсутствия.
 */
Sign get_type_of_sign(Mat &sign);

/**
 * Принимает фрагмент изображения, содержащий только светофор и
 * возвращает цвет сигнала светофора или NONE в случае его отсутствия.
 */
Sign get_tr_color(Mat &trafic_lights);

/**
 * Принимет изображение,
 * находит на нем знак или светофор и
 * возвращает тип знака или цвет светофора
 */
Sign recognize_sign(Mat &frame);

/**
 * Принимает изображение и координату где была черная линия в последний раз,
 * возвращает координату центра черной линии.
 */
int find_line(const cv::Mat &frame, int last_line);


int main(int argc, char *argv[])
{
    // Считывание имени входного файла из аргумента командной строки.
    string filename;
    if (argc > 1) {
        filename = argv[1];
    } else {
        // Значение по-умолчанию при отсутствии аргумента.
        filename = "videos/all_input.avi";
    }

   Mat frame;
   VideoCapture cap(filename);

   int line = 320; // Координаты ценра линии
   int last_line = 320; // Координаты центра линии на предыдущем шаге

   // Счетчик циклов для паузы в поиске следующего знака после обнаружения предыдущего.
   // Необходим чтобы не прореагировать на  один и тот же знак дважды.
   int after_sign = 1000;
   int n_iter_delay = 25;

   // Список возможных событий для вывода в консоль.
   string sign_types[8] = {"Forward", "Right", "Left", "STOP", "Pedestrian",
                            "Red", "Yellow", "Green"};
   Sign sign = NONE; // Хранит последний обнаруженный знак или NONE.

   if(!cap.isOpened()) {
        cout << "Unable to open video source" << endl;
        return 1;
    }

    // Устанавливает размер кадров, которые будем считывать с веб-камеры
    cap.set(cv::CAP_PROP_FRAME_WIDTH, 640);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 480);

    while(true) {
        cap.read(frame);
        if(waitKey(33) >= 0) break; // примерно 30 кадров в секунду.
        if(frame.empty()) continue;

        // Нахождение черной линии
        line = find_line(frame, last_line);
        last_line = line;
        cv::line(frame, cv::Point(line, frame.rows),
                        cv::Point(line, frame.rows-50),
                        cv::Scalar(255, 0, 0), 3);

        // Распознование знаков и цветов светофора.
        // Если после последнего знака прошло необходимое количество итераций.
        if (after_sign > n_iter_delay) {
            after_sign = n_iter_delay;
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


Colors count_colors(Mat &frame)
{
    /**
     * Принимает фрагмент изображения и
     * возвращает количество красного, черного, синего и желтого в изображении.
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
            // Для определения жёлтого цвета
            if (pixel[1] - pixel[0] > 20 && pixel[2] - pixel[0] > 20)
                colors.yellow++;
        }
    }

    // Узнаём процентное соотношение цветов
    float count = frame.cols * frame.rows;
    colors.red = (float)colors.red / count * 100;
    colors.blue = (float)colors.blue / count * 100;
    colors.black = (float)colors.black / count * 100;
    colors.yellow = (float)colors.yellow / count * 100;
    return colors;
}


Sign get_type_of_sign(Mat &sign)
{
    /**
     * Принимает фрагмент изображения, содержащий только знак и
     * возвращает тип знака или NONE в случае его отсутствия.
     */

     // Подсчет количества цвета
     Colors colors = count_colors(sign);

     if (colors.red > 40) {
         return STOP;
     } else if (colors.black > 5 and colors.blue > 40) {
         return PEDESTRIAN;
     } else if (colors.blue > 60) {
         // Знак направления движения.
         // Для определения знака направления движения используется
         // положение стойки стрелки, то есть если стойка стрелки
         // находится слева, то это знак "движение направо" и т.д.
         // Для нахождения положения стойки стрелки используется всего
         // одна строчка пикселей в нижней части знака.
         int scan_row = sign.rows * 0.7;
         // Количество белых пикселей в строчке
         int white_pixels = 0;
         // Сумма X-координат белых пикселей в строчке
         int pixels_offset = 0;

         // Проходимся по пикселям строчки, пропуская 4 первых и 4 последних пикселя
         for (int offset = 4; offset < (sign.cols - 4); offset++) {
             // Если нашли белый пиксель в строчке
             if (
                 ((sign.at<Vec3b>(Point(offset, scan_row))[2]) > 90) &&
                 ((sign.at<Vec3b>(Point(offset, scan_row))[1]) > 90) &&
                 ((sign.at<Vec3b>(Point(offset, scan_row))[0]) > 90))
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
             return NONE;

         // Узнаём положение белой стойки стрелки
         float center = pixels_offset / white_pixels;
         // Узнаём положение в процентах
         float light_position = center / sign.cols;

         // Определяем, какой знак направления движения нашли
         if(light_position >= 0.6) {
             // Знак движения налево
             return LEFT;
         }else if(light_position >= 0.4) {
             // Знак движения прямо
             return FORWARD;
         }else if(light_position >= 0.0) {
             // Знак движения направо
             return RIGHT;
         }
     }
     return NONE;
}


Sign get_tr_color(Mat &trafic_lights)
{
    /**
     * Принимает фрагмент изображения, содержащий только светофор и
     * возвращает цвет сигнала светофора или NONE в случае его отсутствия.
     */
     Colors colors = count_colors(trafic_lights);
    // Если количество чёрных пикселей больше 40%, то мы нашли чёрную бленду светофора
    if(colors.black < 70 or colors.yellow > 10) return NONE;
    // cout << colors.black << endl;
    // cout << colors.red << endl;
    // cout << colors.blue << endl;
    // cout << colors.yellow << endl;
    // ***** Распознавание сигналов светофора *****

    // Сигнал светофора определяется по положению, то есть цвет сигнала не учитывается.
    const int column = trafic_lights.cols * 0.5;
    // Количество белых пикселей
    int32_t white_pixels = 0,
    // Сумма порядковых номеров белых пикселей
    white_pixels_offset = 0;

    for (int32_t offset = 0; offset < trafic_lights.rows; offset++) {
        Vec3b pixel = trafic_lights.at<Vec3b>(Point(column, offset));
        // 40 40 120
        if (cv::max(pixel[0], cv::max(pixel[2], pixel[1])) >= 70) {
            white_pixels++;
            white_pixels_offset += offset;
        }
    }

    // Если количество белых пикселей в строке меньше 10, то
    // останавливаем определения сигнала светофора
    if(white_pixels <= 2) return NONE;

    // Координата y, зажжённого сигнала
    float signal_center = white_pixels_offset / white_pixels,
        light_position = signal_center / trafic_lights.rows;

    // Переменная lightPosition, определяет положение зажжённого сигнала
    // светофора (0.7 - зеленый, 0.46 желтый, 0.23 - красный)

    // Зелёный сигнал светофора
    if(light_position >= 0.75) {
        return TR_GREEN;
    }
    // Жёлтый сигнал светофора
    else if(light_position >= 0.4) {
        //cout << "Yellow traffic light signal" << endl;
        return TR_YELLOW;
    }
    // Красный сигнал светофора
    else if(light_position >= 0.1) {
        return TR_RED;
        //cout << "Red traffic light signal" << endl;
    }
    return NONE;
}


Sign recognize_sign(Mat &frame)
{
    /**
     * Принимет изображение,
     * находит на нем знак или светофор и
     * возвращает тип знака или цвет светофора
     */

    // Область в которой ищем дорожный знак или светофор.
    Rect area_sign(400,     // X-координата вехнего левого угла области
                   200,     // Y-координата вехнего левого угла области
                   240,     // Ширина области интереса в пикселях
                   120);    // Высота области интереса в пикселях

    // Создаём копии кадра "frame"
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
        if (area < 500)
            continue;

        // Узнаём, в каком месте кадра находится контур с помощью функции "boundingRect"
        Rect boundingarea = boundingRect(approx);

        // Находим соотношение сторон найденного контура
        double ratio = boundingarea.width / boundingarea.height;

        // Если знак примерно квадратный значит это потенциальный знак.
        if (0.8 < ratio < 1.2) {
            Mat sign = area_frame(boundingarea); // Вырезает потенциальный знак
            Sign sign_type = get_type_of_sign(sign); // Пытается его распознать
            if (sign_type != NONE) { // Если получилось
                return sign_type; // Возвращает тип знака
            }
        }
        if( 0.2 < ratio < 0.8) {
            Mat trafic_lights = area_frame(boundingarea); // Вырезает потенциальный светофор
            Sign trafic_color = get_tr_color(trafic_lights); // Пытается его распознать
            if (trafic_color != NONE) { // Если получилось
                //rectangle(frame(area_sign), boundingarea, Scalar(255, 0, 0), 2); // Обводит в рамку
                return trafic_color; // Возвращает цвет светофора
            }
        }
    }
    return NONE;
}


int find_line(const cv::Mat &frame, int last_line)
{
    /**
     * Принимает изображение и координату где была черная линия в последний раз,
     * возвращает координату центра черной линии.
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
