from PyQt5 import QtWidgets, uic, QtCore, QtGui, Qt
import sys
import time
import os

import messaging


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + '/resources/form.ui', self)
        self.button.clicked.connect(self.press_button)
        self.save_button.clicked.connect(self.save_settings)
        self.load_button.clicked.connect(self.load_settings)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.serve_connection)
        self.timer.start(100)
        self.n_after_log_checked = 0
        self.messager = messaging.Messager()
        self.is_running = False
        self.frame = QtGui.QPixmap(os.path.dirname(os.path.realpath(__file__)) + "/resources/background.jpg")
        self.show()

    def paintEvent(self, event):
        self.frame_widget.setPixmap(self.frame.scaledToWidth(self.frame_widget.width() ));

    def save_settings(self):
        if self.messager.is_connected:
            values = [self.input_kp.value(), self.input_ki.value(),
                      self.input_kd.value(), self.input_speed.value()
                      ]
            self.messager.send(('set', *values))

    def load_settings(self):
        # FIXME: Тут баг. Иногда крашит приложение или пакеты не долетают.
        if self.messager.is_connected:
            self.messager.send(('get',))
            time.sleep(0.4)

            kp, ki, kd, speed = self.messager.params
            self.input_kp.setValue(kp)
            self.input_ki.setValue(ki)
            self.input_kd.setValue(kd)
            self.input_speed.setValue(speed)

    def press_button(self):
        if self.messager.is_connected:
            if self.is_running:
                self.messager.send(('start',))
            else:
                self.messager.send(('stop',))
        else:
            # Попытка подключения
            self.messager.connect()
            self.button.setText("Подключаюсь...")
            #self.logs.setPlainText('')


    def closeEvent(self, event):
        if self.messager.is_connected:
            self.messager.send(('buy',))


    def serve_connection(self):
        if self.messager.is_connected:
            if self.messager.is_running:
                self.button.setText("Остановить машинку")
            else:
                self.button.setText("Запустить машинку")

            self.ip_lbl.setText(self.messager.server_addr[0])

            if self.is_show_last.isChecked():
                self.logs.setPlainText(self.logs.toPlainText() + self.messager.get_logs())
                self.logs.verticalScrollBar().setValue(self.logs.verticalScrollBar().maximum());
            else:
                pos = self.logs.verticalScrollBar().value()
                self.logs.setPlainText(self.logs.toPlainText() + self.messager.get_logs())
                self.logs.verticalScrollBar().setValue(pos)

        if self.messager.frame is not None:
            height, width, channel = self.messager.frame.shape
            bytesPerLine = 3 * width
            self.frame =  QtGui.QPixmap(QtGui.QImage(self.messager.frame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped())
            self.frame_widget.setPixmap(self.frame)

        self.status_lbl.setText(messaging.STATUS[self.messager.autocar_status])
        self.error_lbl.setText(str(self.messager.autocar_error))
        self.timer.start(100)


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
