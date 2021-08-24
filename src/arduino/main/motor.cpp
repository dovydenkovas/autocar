// This file is part of https://github.com/dovydenkovas/autocar project.
//
// Copyright 2020 The https://github.com/PopkovRobotics/RoboMobile contributors
// Copyright 2021 The https://github.com/dovydenkovas/autocar contributors
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

#include "motor.h"

// Конструктор класса
Motor::Motor(int pwm_motor,int dir_motor) {
  // Пин управления скоростью мотора
  this->pwm_motor = pwm_motor;
   // Пин управления направлением движения мотора
  this->dir_motor = dir_motor;
  // Направление движения модели
  this->dir = Forward;

  pinMode(pwm_motor, OUTPUT);
  pinMode(dir_motor, OUTPUT);

  // Выключаем движение мотора
  digitalWrite(pwm_motor, LOW);
  digitalWrite(dir_motor, LOW);
}

// Функция меняет направление движения модели
void Motor::direction(Direction dir) {
  if(this->dir != dir) {
    // Выключаем движение мотора
    digitalWrite(pwm_motor, LOW);
    digitalWrite(dir_motor, LOW);

    // Меняем направление движения мотора
    int tmp = dir_motor;
    dir_motor = pwm_motor;
    pwm_motor = tmp;

    this->dir = dir;
  }
}

// Функция устаналивает новую скорость движения мотора
void Motor::speed(int speed_motor) {
  analogWrite(pwm_motor, speed_motor);
}
