""" Модуль отвечающий за управление ардуинкой.
    Получает ошибку управления по errors_queue, вычисляет управляющее
    воздействие на основе ПИД-регулятора и отправляет сигнал управления
    на ардуинку.

    Останавливает/запускает машинку при получении соответствующего сигнала
    по control_queue.

"""

import time
import serial
import arduino
import threading

from logtools import *


is_running = False

# Скорость движения
speed = 20

# Коэффициенты (пропорциональный, интегральный, дифференциальный):
kp = 0.5
ki = 0.2
kd = 0.2

# Ошибка управления
error = 0
old_error = 0

# STATUS = ["Нет соединения", "Еду", "Стою", "Ищу Ардуинку"]

def manual_control(control_queue, logs_queue):
    global kp, ki, kd, speed, is_running
    while True:
        if not control_queue.empty():
            message = control_queue.get()
            if message[0] == 'start':
                is_running = True
                logs_queue.put(log('Еду'))
            elif message[0] == 'stop':
                is_running = False
                logs_queue.put(log('Стою'))
            elif message[0] == 'set':
                kp, ki, kd, speed, *_ = message[1:]
                logs_queue.put(log(f'Установлены новые значения коэфициантов: kp={kp}, ki={ki}, kd={kd}, speed={speed}'))
            elif message[0] == 'get':
                logs_queue.put(var(kp, ki, kd, speed))
        time.sleep(0.2)


def send_stat(logs_queue):
    global is_running, error
    while True:
        logs_queue.put(arg((1 if is_running else 2), error))
        time.sleep(0.2)


def mainloop(control_queue, errors_queue, logs_queue):
    global is_running, speed, kp, kd, ki, error, old_error
    print("Контроллер запустился")

    manual_control_thread = threading.Thread(target=manual_control, daemon=True, args=(control_queue, logs_queue))
    manual_control_thread.start()

    send_stat_thread = threading.Thread(target=send_stat, daemon=True, args=(logs_queue,))
    send_stat_thread.start()

    robot = arduino.Arduino()
    logs_queue.put(arg(3, 0)) # Ищу ардуинку
    while not robot.isOpened():
        robot = arduino.Arduino()
        time.sleep(0.25)

    dt = 0.025

    i = 0

    while True:
        if not errors_queue.empty():
            error = errors_queue.get()

        if is_running:
            # ПИД регулятор
            p = kp * error
            i = i + ki * error * dt
            d = kd * (error - old_error) / dt
            old_error = error

            u = p + i + d
            robot.run(speed, 90 + u)

        else:
            robot.run(0, 90)

        time.sleep(dt)
