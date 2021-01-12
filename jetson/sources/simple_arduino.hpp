#ifndef SIMPLE_ARDUINO
#define SIMPLE_ARDUINO
#include <string>
#include <cmath>
#include "arduino.hpp"

class Arduino {
public:
    Arduino();

    bool connect(std::string port="/dev/ttyUSB0");
    void close();

    void run(int speed, int angle=0);
    void stop();

private:
    ArduinoCtrl *controller_;
};

#endif
