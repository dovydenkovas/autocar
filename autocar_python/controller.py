""" Модуль отвечающий за управление ардуинкой.
    Получает ошибку управления по errors_queue, вычисляет управляющее
    воздействие на основе ПИД-регулятора и отправляет сигнал управления
    на ардуинку.

    Останавливает/запускает машинку при получении соответствующего сигнала
    по control_queue.

"""

import time
import datetime
import serial
import arduino


def get_time():
    return datetime.datetime.now().strftime("[%H:%M:%S]")


def mainloop(control_queue, errors_queue):
    print("Контроллер запустился")
    robot = arduino.Arduino()
    n = 100
    while not robot.isOpened():
        robot = arduino.Arduino()
        if n % 100 == 0:
            control_queue.put(f"{get_time()} Ищу ардуинку\n")
            n = 0
        n += 1
        time.sleep(0.05)

    is_running = False

    # Скорость движения
    speed = 20

    # Коэффициенты (пропорциональный, интегральный, дифференциальный):
    kp = 0.5
    ki = 0.2
    kd = 0.2

    dt = 0.005


    # Ошибка управления
    error = 0
    old_error = 0

    while True:
        # Есть ли команды управления от пользователя?
        if not control_queue.empty():
            is_running = control_queue.get()
        # Сообщает текущее состояние
        control_queue.put(f"{get_time()} I am {'runnig' if is_running else 'waiting'}\n")

        if not is_running:
            robot.run(0, 0)
        else:
            if not errors_queue.empty():
                error = errors_queue.get()

            # ПИД регулятор
            p = kp * error
            i = i + ki * error * dt
            d = kd * (error - old_error) / dt
            old_error = error

            u = p + i + d
            robot.run(speed, 90 + u)
            sleep(dt)
