#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;


int main() {

    Mat frame;
    // VideoCapture cap("black_line.avi");
    VideoCapture cap(0);
    
    if(!cap.isOpened()) {
        cout << "Unable to open video source" << endl;
        return 1;
    }
    // // Устанавливаем высоту кадров, которые будем считывать с веб-камеры
    // cap.set(cv::CAP_PROP_FRAME_WIDTH, 640);
    // // Устанавливаем высоту кадров, которые будем считывать с веб-камеры
    // cap.set(cv::CAP_PROP_FRAME_HEIGHT, 480);


    cap.read(frame);
        // Проверяем успешно ли считали кадр
        // Метод "empty()" возвращает true, если в массиве "Mat" нет элементов.
    if(!frame.empty()) {
        imwrite("img.png", frame);
    }
    return 0;
}
