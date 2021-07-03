from PyQt5 import QtWidgets, uic, QtCore, QtGui, Qt
import sys

import messaging


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('resources/form.ui', self)
        self.button.clicked.connect(self.press_button)
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


    def press_button(self):
        if self.is_connected:
            if self.is_running:
                self.is_running = self.messager .send("start")
                self.button.setText("Остановить машинку")
            else:
                self.is_running = not self.messager .send("end")
                self.button.setText("Запустить машинку")
        else:
            self.is_connected = self.messager.connect()
            if self.is_connected:
                self.button.setText("Остановить машинку")
                self.logs.setPlainText('')
            else:
                QtWidgets.QMessageBox.warning(self,
                                        "Что-то пошло не так",
                                        "Подключение не удалось",
                                         QtWidgets.QMessageBox.Ok)


    def serve_connection(self):
        if self.is_connected:
            self.logs.setPlainText(self.logs.toPlainText() + self.messager .get_logs())

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
