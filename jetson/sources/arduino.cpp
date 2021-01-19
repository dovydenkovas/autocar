#include "arduino.hpp"


ArduinoCtrl::ArduinoCtrl()
{
    /**
     * Конструктор класса без подключения к Arduino.
     */
}


ArduinoCtrl::ArduinoCtrl(std::string port)
{
    /**
     * Конструктор класса, в котором подключаемся к Arduino
     * port - порт подключения к ардуинке.
     * к которому подключена Arduino.
     */

    connect(port);
}


bool ArduinoCtrl::connect(std::string port)
{
    /**
     * Функция для подключения к Arduino.
     * port - порт подключения к ардуинке.
     * Возвращает True в случае успешного подключения и False в случае неудачи.
     */

    arduino_fd = -1;
 	// Открываем соединение с Arduino
 	arduino_fd = open(port.c_str(), O_RDWR | O_NOCTTY | O_NONBLOCK);
 	if (arduino_fd < 0) {
         std::cerr << "Can't open serial port." << std::endl;
 		connection = false;
 		return connection;
 	}

 	usleep(1000000); // задержка 1 секунда

 	// Задаём параметры для "общения" с Arduino
 	struct termios options;
 	tcgetattr(arduino_fd, &options);
 	// Скорость отправки/чтения данных (115200 бод)
 	cfsetispeed(&options, B115200);
 	cfsetospeed(&options, B115200);

 	options.c_cflag &= ~PARENB;
 	options.c_cflag &= ~CSTOPB;
 	options.c_cflag &= ~CSIZE;
 	options.c_cflag |= CS8;
 	options.c_cflag &= ~CRTSCTS;
 	options.c_cflag |= CREAD | CLOCAL;
 	options.c_cflag &= ~OPOST;

 	options.c_lflag = 0;

 	options.c_cc[VMIN] = 1;
 	options.c_cc[VTIME] = 0;

 	// Устаналиваем параметры для "общения" с Arduino
 	tcsetattr(arduino_fd, TCSANOW, &options);

 	tcflush(arduino_fd, TCIOFLUSH);
 	tcflush(arduino_fd, TCIFLUSH);

 	usleep(500000);

 	connection = true;

    return connection;
}


bool ArduinoCtrl::is_connected()
{
    /**
     * Функция, которая возвращает статус подключения к Arduino.
     */
	return connection;
}


void ArduinoCtrl::close_connection()
{
    /**
     * Функция для закрытия соединения с Arduino.
     */
    if (connection) {
        if (close(arduino_fd) == 0) {
            connection = true;
        } else {
            connection = false;
        }
    }
}


void ArduinoCtrl::run(int speed, int angle)
{
    /**
     * Управление движением машинки.
     * Принимает 2 аргумента:
     * speed - измеряется в см/с.
     *         Допустимые значения: -65 <= speed <= 65.
     *         Note: При |speed| < 27 машинка не едет.
     * angle - угол поворота колес. По-умолчанию angle=0
     *         Допустимые значения: -30 <= angle <= 30.
     * Робот едет прямо со скоростью 45 см/с.
     */

     // Не выполняется если соединение не установлено
     if (!connection) {
         return;
     }

     // Проверка адекватности значения скорости.
     if (abs(speed) > 65) {
        std::cerr << "Invalid speed (" << speed << "). -65 < speed < 65" << '\n';
        speed = speed < 0 ? -65 : 65;
    }

    // Проверка адекватности значения угла поворота.
    if (abs(angle) > 30) {
        std::cerr << "Invalid angle (" << angle << "). -30 < angle < 30" << '\n';
        angle = angle < 0 ? -30 : 30;
    }

    int direction = speed < 0 ? 0 : 1; // Направление движения. 1 - вперед, 0 - назад.
    speed = abs(speed); // Знак скорости - направление движения. Теперь он не нужен.
    //angle += 90; // Другой интерфейс: 60 < angle < 120.
    std::string message = "SPD " +
                          std::to_string(angle) + "," +
                          std::to_string(direction) + "," +
                          std::to_string(speed) + " ";
    send_command(message);
}


void ArduinoCtrl::stop()
{
    /**
     * Останавливает машинку.
     * Обертка для run(0);
     */

    run(0);
}


void ArduinoCtrl::send_command(std::string message)
{
    /*
     * Функция для отправки сообщения на Arduino.
     * message - констатный параметр типа char*, сообщение для отправки,
     * size - параметр типа size_t, размер отправляемого сообщения.
     */

    if (connection)
    {
        // Отправляет команду на Arduino
    	int bytes = write(arduino_fd, message.c_str(), message.length());
        // Если данные отправились не польностью, то выводим ошибку
    	if (bytes < (int)message.length()) {
            std::cerr << "Arduino sending data error." << std::endl;
        }
    	ioctl(arduino_fd, TCSBRK, 1);
    }
}

/*
int ArduinoCtrl::Read(char* chars, size_t size)
{
	return read(arduino_fd, chars, size);
}
*/
