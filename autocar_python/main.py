""" Главный модуль.
    Создает отдельные процессы: controller, road_analyzer, video_server
    и очереди между ними:
        control_queue - между video_server и controller
        frames_queue - между video_server и road_analyzer
        errors_queue - между controller и road_analyzer

    Модуль является процессом controller, после запуска остальных процессов
    вызывается метод mainloop() из модуля controller.

"""

from multiprocessing import Process, Queue
import controller
import roadanalyzer
import videoserver


control_queue = Queue()
frames_queue = Queue()
errors_queue = Queue()

video_server = Process(target=videoserver.mainloop, args=(control_queue, frames_queue))
road_analyzer = Process(target=roadanalyzer.mainloop, args=(errors_queue, frames_queue))
video_server.start()
road_analyzer.start()
controller.mainloop(control_queue, errors_queue)
video_server.join()
road_analyzer.join()
