#include <iostream>
#include <opencv2/opencv.hpp> 


int get_point_red(cv::Mat frame, cv::Point point)
{
    /*  
     *  Принимает кадр и точку.
     *  Возвращает значение красного цвета в этой точке.
     */
    cv::Vec3b color = frame.at<cv::Vec3b>(point);
    return color[2];
}

    
int main() 
{
    cv::Mat frame; // n-мерный числовой массив для хранения изображений.
    // Разрешение видиофайла 640x480
    cv::VideoCapture cap("videos/black_line.avi"); // Захватываем видео из видиофайла
    // cv::VideoCapture cap(0); // Захватываем видео с веб-камеры
    
    const int scan_row = 470; // координата "y" изображения на которой ищем границу линии
    int left_side = 100; // Координаты левой границы линии
    int right_side = 540; // Координаты правой границы линии

    if (!cap.isOpened()) {
        std::cout << "Error: unable to open camera." << std::endl;
        return 1;
    }

    while (true) {
        cap.read(frame); // Считываем кадр с видео и записаваем в frame     

        // Если пользователь нажал кнопку или кадр не считался, выходим из цикла
        if (cv::waitKey(20) >= 0 or frame.empty()) {
            break;
        }
        
        // Поиск левой границы черной линии
        for (int x=100; x<500; x++) {
            if (get_point_red(frame, cv::Point(x, scan_row)) < 40) {
                left_side = x;
                break;
            }
        }


        // Поиск правой границы черной линии
        for (int x=500; x>100; x--) {
            if (get_point_red(frame, cv::Point(x, scan_row)) < 40) {
                right_side = x;
                break;
            }
        }

        // Обозначаем левую границу черной линии синей полоской
        cv::line(frame, cv::Point(left_side, frame.rows), cv::Point(left_side, frame.rows-50), cv::Scalar(255, 0, 0), 3);        
        // Обозначаем правую границу черной линии красной полоской
        cv::line(frame, cv::Point(right_side, frame.rows), cv::Point(right_side, frame.rows-50), cv::Scalar(0, 0, 255), 3);
  
        cv::imshow("Live", frame); // Выводим кадр в окно "Live"
    }

    return 0;    
}
