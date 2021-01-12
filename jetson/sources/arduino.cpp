#include "arduino.hpp"

// Функции класса ArduinoCtrl
/*
 * Конструктор класса, в котором подключаемся к Arduino
 * system - ссылка на параметр типа System, для получения порта,
 * к которому подключена Arduino.
 */
ArduinoCtrl::ArduinoCtrl(std::string port) {
	arduino_fd = -1;
	// Открываем соединение с Arduino
	arduino_fd = open(port.c_str(), O_RDWR | O_NOCTTY | O_NONBLOCK);
	if (arduino_fd < 0) {
        std::cout << "Can't open serial port." << std::endl;
		connection = false;
		return;
	}

	usleep(1000000);

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
	return;
}
/* 
 * Функция для отправки сообщения на Arduino.
 * message - констатный параметр типа char*, сообщение для отправки,
 * size - параметр типа size_t, размер отправляемого сообщения.
 */
void ArduinoCtrl::SendCommand(std::string message) {
	// Отправляет команду на Arduino
	int bytes = write(arduino_fd, message.c_str(), message.length());
    // Если данные отправились не польностью, то выводим ошибку
	if (bytes < (int)message.length()) std::cout << "Arduino sending data error." << std::endl;
	ioctl(arduino_fd, TCSBRK, 1);
	return;
}
// 
int ArduinoCtrl::Read(char* chars, size_t size) {
	return read(arduino_fd, chars, size);
}
// Функция для закрытия соеденения с Arduino
void ArduinoCtrl::DeInit() {
	// Отключаемся от Arduino, если Arduino подключена
	if (connection)
		connection = close(connection) == 0 ? true : false;
	return;
}
// Функция, которая возвращает статус подключения к Arduino.
bool ArduinoCtrl::IsConnected() {
	return connection;
}