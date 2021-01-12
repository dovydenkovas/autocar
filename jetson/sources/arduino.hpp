#pragma once
#include <string>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <iostream>
#include <termios.h>
#include <sys/ioctl.h>

struct ArduinoData {
    double distance;
    bool charge_bat;
    
    // Конструктор класса
    ArduinoData(double distance = 0.0, bool charge_bat = true) {
        this->distance = distance;
        this->charge_bat = charge_bat;
    }
};

// Класс ArduinoCtrl реализует "общение" с Arduino
class ArduinoCtrl {
private:
	// arduino_fd - параметр типа int, сокет для общения с Arduino. 
	int arduino_fd;			
	// connection - параметр типа bool, статус подключения к Arduino 
	// (true - Arduino поделючена, false - Arduino не подключена).
	bool connection;
public:
	/*
 	 * Конструктор класса, в котором подключаемся к Arduino
 	 * system - ссылка на параметр типа System, для получения порта,
 	 * к которому подключена Arduino.
 	 */
	ArduinoCtrl(std::string port);
	/* 
 	 * Функция для отправки сообщения на Arduino.
 	 * message - сообщение для отправки
 	 */
	void SendCommand(std::string message);

	int Read(char* chars, size_t size);
	/*
 	 * Функция получает информацию с Arduino и возвращает её.
 	 */
	ArduinoData Feedback();
	// Функция для закрытия соеденения с Arduino
	void DeInit();
	// Функция, которая возвращает статус подключения к Arduino.
	bool IsConnected();
};