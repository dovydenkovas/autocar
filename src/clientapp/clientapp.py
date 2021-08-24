"""
    Главный файл клиентского приложения.
    Реализует графический интерфейс в классе Ui.
"""

import os
import sys
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication

import messaging


class Ui(QMainWindow):
    """ Класс окна """
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + '/resources/form.ui', self)
        self.button.clicked.connect(self.press_button)
        self.save_button.clicked.connect(self.save_settings)
        self.load_button.clicked.connect(self.load_settings)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.serve_connection)
        self.timer.start(150)

        self.n_after_log_checked = 0
        self.messager = messaging.Messager()
        self.frame = QPixmap(os.path.dirname(os.path.realpath(__file__)) +
                            "/resources/background.jpg")
        self.waiting_settings = False
        self.show()

    def paintEvent(self, event):
        """ Масштабирует изображение. """
        self.frame_widget.setPixmap(self.frame.scaledToWidth(self.frame_widget.width()))

    def save_settings(self):
        """ Сохраняет значения коэффициентов на машинку. """
        if self.messager.is_connected:
            values = [self.input_kp.value(), self.input_ki.value(),
                      self.input_kd.value(), self.input_speed.value()
                      ]
            self.messager.send(('set', *values))

    def load_settings(self):
        """ Загружает значения коэффициентов с машинки. """
        if self.messager.is_connected:
            self.messager.send(('get',))
            self.waiting_settings = True


    def press_button(self):
        """ Обрабатывает нажатие большой синей кнопки. """
        if self.messager.is_connected:
            if self.messager.is_running:
                self.messager.send(('stop',))
            else:
                self.messager.send(('start',))
        else:
            # Попытка подключения
            self.messager.open()
            self.button.setText("Подключаюсь...")


    def closeEvent(self, event):
        """ Завершает соединение с машинкой. """
        self.messager.close()


    def serve_connection(self):
        """ Обрабатывает информацию с машинки. """
        if self.messager.is_connected:
            if self.messager.is_running:
                self.button.setText("Остановить машинку")
            else:
                self.button.setText("Запустить машинку")

            self.ip_lbl.setText(self.messager.server_addr[0])

            if self.is_show_last.isChecked():
                self.logs.setPlainText(self.logs.toPlainText() + self.messager.get_logs())
                self.logs.verticalScrollBar().setValue(self.logs.verticalScrollBar().maximum())
            else:
                pos = self.logs.verticalScrollBar().value()
                self.logs.setPlainText(self.logs.toPlainText() + self.messager.get_logs())
                self.logs.verticalScrollBar().setValue(pos)

        if self.messager.frame is not None:
            height, width, _ = self.messager.frame.shape
            bytes_per_line = 3 * width
            self.frame =  QPixmap(QImage(self.messager.frame.data,
                                        width, height, bytes_per_line,
                                        QImage.Format_RGB888).rgbSwapped())
            self.frame_widget.setPixmap(self.frame)

        if self.waiting_settings:
            kp, ki, kd, speed = self.messager.params
            self.input_kp.setValue(kp)
            self.input_ki.setValue(ki)
            self.input_kd.setValue(kd)
            self.input_speed.setValue(speed)
            self.waiting_settings = False

        self.status_lbl.setText(messaging.STATUS[self.messager.autocar_status])
        self.error_lbl.setText(str(self.messager.autocar_error))


app = QApplication(sys.argv)
window = Ui()
app.exec_()
