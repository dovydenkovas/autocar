#include <iostream>
// Библиотека технического зрения
#include <opencv2/opencv.hpp> 


int main() 
{
    cv::Mat frame; // n-мерный числовой массив для хранения изображений.
    cv::VideoCapture cap("videos/black_line.avi"); // Захватываем видео из видиофайла
    // cv::VideoCapture cap(0); // Захватываем видео с веб-камеры

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
        
        cv::imshow("Live", frame); // Выводим кадр в окно "Live"
    }

    return 0;    
}
