#include "simple_arduino.hpp"

Arduino::Arduino() {}

bool Arduino::connect(std::string port) {
    controller_ = new ArduinoCtrl(port);
    if (!controller_->IsConnected()) {
           // Если соединение не установлено
        std::cerr << "Arduino isn't attached." << std::endl;
        return false;
    }
    std::cout << "Arduino is attached." << std::endl;
	stop();
	stop();
	stop();
    return true;
}

void Arduino::close() {
    controller_->DeInit();
}

void Arduino::run(int speed, int angle) {
    /* Управление движением машинки.
     * Принимает 2 аргумента:
     * speed - измеряется в см/с.
     *         Допустимые значения: -65 <= speed <= 65.
     *         Note: При |speed| < 27 машинка не едет.
     * angle - угол поворота колес. По-умолчанию angle=0
     *         Допустимые значения: -30 <= angle <= 30.
     * Робот едет прямо со скоростью 45 см/с.
     */

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
    controller_->SendCommand(message);
}

void Arduino::stop() {
    run(0);
}
