#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>


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



int main(int argc, char *argv[]) {
    std::string filename;
    // Если существует аргумент командной строки
    if (argc > 1) {
        // Значит это имя файла
        filename = argv[1];
    } else {
        // В противном случае используем заданное имя файла
        filename = "videos/black_line.avi";
    }

    cv::Mat frame;
    cv::VideoCapture cap(filename);

    int line = 320; // Координаты ценра линии
    int last_line = 320; // Координаты центра линии на предыдущем шаге

    if (!cap.isOpened()) {
        std::cout << "Error: unable to open camera." << std::endl;
        return 1;
    }

    while (true) {
        cap.read(frame);
        if (cv::waitKey(20) >= 0 or frame.empty()) break;

        line = find_line(frame, last_line);
        last_line = line;

        cv::line(frame, cv::Point(line, frame.rows), cv::Point(line, frame.rows-50), cv::Scalar(255, 0, 0), 3);
        cv::imshow("Live", frame);
    }

    return 0;
}
