import sys
import sqlite3
import datetime
from PyQt5.QtGui import QImage, QMouseEvent
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QFileDialog
from UiFiles.CalendarFormUFile import Ui_CalendarForm
from AudioFormWidget import AudioWidget


class CalendarWidget(QDialog, Ui_CalendarForm):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.flag = True

        self.setupUi(self)
        self.OK.clicked.connect(self.send_close)
        self.setStyleSheet(open('stylesheet/style.css', 'r').read())
        self.show_date()
        self.calendarWidget.clicked.connect(self.show_date)

    def show_date(self): # при нажатии на дату в date_label будет записываться выбранная
        self.date = self.calendarWidget.selectedDate()
        self.day, self.month, self.year = self.date.day(), self.date.month(), self.date.year()
        self.date_label.setText(f'Выбранная дата: {self.day}.{self.month}.{self.year}')

    def send_close(self):  # при нажатии на "ок"
        self.date = self.calendarWidget.selectedDate()
        self.day, self.month, self.year = self.date.day(), self.date.month(), self.date.year()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalendarWidget()
    window.show()
    sys.exit(app.exec_())
