""" Модуль отвечающий за управление ардуинкой.
    Получает ошибку управления по errors_queue, вычисляет управляющее
    воздействие на основе ПИД-регулятора и отправляет сигнал управления
    на ардуинку.

    Останавливает/запускает машинку при получении соответствующего сигнала
    по control_queue.

"""

import time
import datetime

def get_time():
    return datetime.datetime.now().strftime("[%H:%M:%S]")

def mainloop(control_queue, errors_queue):
    print("Контроллер запустился")

    while True:
        control_queue.put(f"{get_time()} Hello\n")
        time.sleep(4)
