#ifndef ARDUINO_HPP
#define ARDUINO_HPP

#include <fcntl.h>
#include <iostream>
#include <string>
#include <sys/ioctl.h>
#include <termios.h>
#include <unistd.h>
//#include <string.h>
//#include <stdio.h>


// Класс ArduinoCtrl реализует "общение" с Arduino
class ArduinoCtrl {
public:
    /**
     * Конструктор класса без подключения к Arduino.
     */
    ArduinoCtrl();

   /**
    * Конструктор класса, в котором подключаемся к Arduino
    * port - порт подключения к ардуинке.
    * к которому подключена Arduino.
    */
   ArduinoCtrl(std::string port);

   /**
    * Функция для подключения к Arduino.
    * port - порт подключения к ардуинке.
    * Возвращает True в случае успешного подключения и False в случае неудачи.
    */
   bool connect(std::string port="/dev/ttyUSB0");

   /**
    * Функция, которая возвращает статус подключения к Arduino.
    */
   bool is_connected();

   /**
    * Функция для закрытия соединения с Arduino.
    */
   void close_connection();

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
   void run(int speed, int angle=0);

   /**
    * Останавливает машинку.
    * По сути тоже самое, что run(0,0);
    */
   void stop();

   /**
    * Функция для отправки сообщения на Arduino.
    * message - сообщение для отправки
    */
   void send_command(std::string message);

   /**
    * Функция получает информацию с Arduino и возвращает её.
    */

private:
   // arduino_fd - параметр типа int, сокет для общения с Arduino.
   int arduino_fd;
   // connection - параметр типа bool, статус подключения к Arduino
   // (true - Arduino поделючена, false - Arduino не подключена).
   bool connection;
};

#endif // ARDUINO_HPP
