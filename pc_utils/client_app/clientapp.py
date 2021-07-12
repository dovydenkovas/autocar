from PyQt5 import QtWidgets, uic, QtCore, QtGui, Qt
import sys
import time

import messaging


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('resources/form.ui', self)
        self.button.clicked.connect(self.press_button)
        self.save_button.clicked.connect(self.save_settings)
        self.load_button.clicked.connect(self.load_settings)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.serve_connection)
        self.timer.start(100)
        self.n_after_log_checked = 0
        self.messager = messaging.Messager()


        self.is_connected = False
        self.is_running = False
        self.frame = QtGui.QPixmap("resources/background.jpg")

        self.show()

    def paintEvent(self, event):
        self.frame_widget.setPixmap(self.frame.scaledToWidth(self.frame_widget.width() ));

    def save_settings(self):
        if self.is_connected:
            values = [self.input_kp.value(), self.input_ki.value(),
                      self.input_kd.value(), self.input_speed.value()
                      ]
            self.messager.send({'command': 'set', 'args': values})

    def load_settings(self):
        # FIXME: Тут баг. Иногда крашит приложение или пакеты не долетают.
        if self.is_connected:
            self.messager.send({'command': 'get'})
            time.sleep(0.5)
            if self.messager.message['info'] != '':
                self.input_kp.setValue(self.messager.message['info']['kp'])
                self.input_ki.setValue(self.messager.message['info']['ki'])
                self.input_kd.setValue(self.messager.message['info']['kd'])
                self.input_speed.setValue(self.messager.message['info']['speed'])

    def press_button(self):
        if self.is_connected:
            if self.is_running:
                self.is_running = self.messager.send({'command': 'start'})
                self.button.setText("Остановить машинку")
            else:
                self.is_running = not self.messager.send({'command': 'stop'})
                self.button.setText("Запустить машинку")
        else:
            self.is_connected = self.messager.connect()
            if self.is_connected:
                self.button.setText("Остановить машинку")
                self.logs.setPlainText('')
                self.messager.send({'command': 'start_video', 'ip': self.messager.local_ip})
            else:
                QtWidgets.QMessageBox.warning(self,
                                        "Что-то пошло не так",
                                        "Подключение не удалось",
                                         QtWidgets.QMessageBox.Ok)

    def closeEvent(self, event):
        if self.is_connected:
            self.messager.send({'command': 'stop_video'})


    def serve_connection(self):
        if self.is_connected:
            if self.logs.verticalScrollBar().value() == self.logs.verticalScrollBar().maximum():
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
            # self.frame = self.messager.frame
        self.frame_widget.setPixmap(self.frame)
        self.timer.start(100)


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
