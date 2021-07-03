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

from logtools import log, command, send


is_running = False

# Скорость движения
speed = 20

# Коэффициенты (пропорциональный, интегральный, дифференциальный):
kp = 0.5
ki = 0.2
kd = 0.2


def manual_control(control_queue, logs_queue):
    global kp, ki, kd, speed, is_running
    while True:
        if not control_queue.empty():
            message = control_queue.get()
            if message['command'] == 'start':
                is_running = True
                logs_queue.put(log("Поехали!"))
            elif message['command'] == 'stop':
                is_running = False
                logs_queue.put(log("Стою!"))
            elif message['command'] == 'set':
                kp, ki, kd, speed = message['args']
                logs_queue.put(log(f'Установлены новые значения коэфициантов: {kp=}, {ki=}, {kd=}, {speed=}'))
            elif message['command'] == 'get':
                logs_queue.put(send('(app) Значения прилетели', {'command':'get', 'kp':kp, 'ki':ki, 'kd':kd, 'speed':speed}))
        time.sleep(0.02)


def mainloop(control_queue, errors_queue, logs_queue):
    global is_running, speed, kp, kd, ki
    print("Контроллер запустился")

    manual_control_thread = threading.Thread(target=manual_control, daemon=True, args=(control_queue, logs_queue))
    manual_control_thread.start()

    robot = arduino.Arduino()
    n = 20
    while not robot.isOpened():
        robot = arduino.Arduino()
        if n % 20 == 0:
            logs_queue.put(log('Ищу ардуинку'))
            n = 0
        n += 1
        time.sleep(0.05)

    dt = 0.005
    # Ошибка управления
    error = 0
    old_error = 0

    while True:
        # Есть ли команды управления от пользователя?
        if not control_queue.empty():
            is_running = control_queue.get()
        # Сообщает текущее состояние
        #logs_queue.put(log(f"I am {'runnig' if is_running else 'waiting'}"))

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
