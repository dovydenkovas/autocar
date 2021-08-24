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

// Значение отклонения от угла поворота 90,
// при котором будут включены поворотники
#define DEVIATION             14
// Продолжительность свечения/выключенности поворотников
// в миллисекундах. (По полсекунды вкл/выкл).
#define TURN_SIGNAL_FREQ      500

class Indicators {
private:
  // Пин, к которому подключён левый поворотникs
  int left_indicator,
  // Пин, к которому подключён правый поворотник
    right_indicator,
  // Пин, к которому подключены светодиоды стоп сигнала
    stop_indicator,
  // Пин, к которому подключены светодиоды передних фар
    head_ligh,
  // Пин, к которому подключены светодиоды габаритов
    rear_ligh;

  // Время, которое включен правый поворотник в миллисекундах
  unsigned long right_time_indicator,
  // Время, которое включен левый поворотник в миллисекундах
    left_time_indicator;

  // Флаг, определяющий включен ли правый поворотник
  bool turn_right_light,
  // Флаг, определяющий включен ли левый поворотник
      turn_left_light;

public:
  // Конструктор класса
  Indicators(int left_indicator, int right_indicator,
      int head_ligh, int rear_ligh, int stop_indicator);

  // Функция включает/выключает фары и фонари-габариты
  void start_indicators(bool on = true);

  // Функция выключает всю световую индекацию
  void lights_off();

  // Функция управляет светофовй индекацией модели,
  // в зависимости от угла поворота передних колёс и скорости модели
  void upd_indicators(int corner, int speed);

};
