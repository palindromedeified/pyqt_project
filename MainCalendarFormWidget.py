import sqlite3
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDialog
from UiFiles.MainCalendarFormUFile import Ui_Form


class MainCalendarWidget(QDialog, Ui_Form):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.flag = True

        with open('text_files/last_date.txt') as file:
            self.d, self.m, self.y = map(int, file.read().split('.'))

        self.is_done = False
        self.setupUi(self)
        self.ok_buuton.clicked.connect(self.send_close)
        self.setStyleSheet(open('stylesheet/style.css', 'r').read())
        self.show_date()
        self.main_calendarWidget.clicked.connect(self.show_date)
        self.setWindowTitle('Календарь')

    def show_date(self):  # при нажатии на дату в main_label_date будет записываться выбранная
        if self.flag:
            self.main_calendarWidget.setSelectedDate(QDate(self.y, self.m, self.d))
            self.flag = False

        date = self.main_calendarWidget.selectedDate()
        self.day, self.month, self.year = date.day(), date.month(), date.year()
        self.main_label_date.setText(f'Выбранная дата: {self.day}.{self.month}.{self.year}')

        with open('text_files/last_date.txt', 'w') as file:
            file.write(f'{self.day}.{self.month}.{self.year}')

    def send_close(self):  # при нажатии на "ок"
        self.is_done = True
        self.close()
