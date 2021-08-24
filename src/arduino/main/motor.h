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

#pragma once
#include <Arduino.h>

// Перечесление, в котором хранится возможные направления
// движения модели
enum Direction {
  Forward = 0,            // Движение модели вперёд
  Backward,               // Движение модели назад
};

class Motor {
private:
  // Пин управления скоростью мотора
  int pwm_motor,
  // Пин управления направлением движения мотора
    dir_motor;

  // Направление движения модели
  Direction dir;
public:
  // Конструктор класса
  Motor(int pwm_motor,int dir_motor);

  // Функция меняет направление движения модели
  void direction(Direction dir);

  // Функция устаналивает новую скорость движения мотора
  void speed(int speed_motor);
};
