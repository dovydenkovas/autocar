/**
 * Пример использования библиотеки для подключения к Arduino "arduino.hpp"
 * Программа выполняет:
 *   1. Подключение к ардуинке.
 *   2. Отправляет ардуинке команду движения вперед со скоростью 50 см/с
 *   3. Через 4 секунды останавливает движение
 */
#include <iostream>
#include <stdlib.h>
#include "arduino.hpp"

int main() {
    ArduinoCtrl robot;
    // Пробуем подключиться к ардуине.
    // Если подключение успешно - функция возвращает true
    // и выполняется тело условия.
    if (robot.connect()) {
        // Функция run принимает 2 аргумента:
        // speed - измеряется в см/с.
        //         Допустимые значения: -65 <= speed <= 65.
        //         Note: При |speed| < 27 машинка не едет.
        // angle - угол поворота колес. По-умолчанию angle=0
        //         Допустимые значения: -30 <= angle <= 30.
        //         angle < 0 - поворот направо.
        //         angle > 0 - поворот налево.
        // Робот едет прямо со скоростью 50 см/с.
        robot.run(50);
		// Ждем 4 секунды
       	sleep(4);
        // робот останавливается
        robot.stop();
        // подключение закрывается
        robot.close_connection();
    }
    return 0;
}