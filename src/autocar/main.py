"""
    This file is part of https://github.com/dovydenkovas/autocar project.

    Copyright 2021 The https://github.com/dovydenkovas/autocar contributors


    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

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
logs_queue = Queue()
frames_queue = Queue()
errors_queue = Queue()

video_server = Process(target=videoserver.mainloop, args=(control_queue, frames_queue, logs_queue))
road_analyzer = Process(target=roadanalyzer.mainloop, args=(errors_queue, frames_queue, logs_queue))
video_server.start()
road_analyzer.start()
controller.mainloop(control_queue, errors_queue, logs_queue)
video_server.join()
road_analyzer.join()
