from PyQt5 import QtWidgets, uic, QtCore, QtGui
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

        self.is_connected = False
        self.is_running = False
        self.frame = QtGui.QPixmap("resources/background.jpg")
        self.show()

    def press_button(self):
        if self.is_connected:
            if self.is_running:
                self.is_running = messaging.send("start")
                self.button.setText("Остановить машинку")
            else:
                self.is_running = not messaging.send("end")
                self.button.setText("Запустить машинку")
        else:
            self.is_connected = messaging.connect()
            if self.is_connected:
                self.button.setText("Остановить машинку")
            else:
                QtWidgets.QMessageBox.information(self,
                                        "Что-то пошло не так",
                                        "Подключение не удалось",
                                         QtWidgets.QMessageBox.Ok)



    def serve_connection(self):
        if self.is_connected:
            # frame = messaging.get_frame()
            self.logs.setText(self.logs.text() + messaging.get_logs())


        self.frame_widget.setPixmap(self.frame)
        self.timer.start(100)


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
