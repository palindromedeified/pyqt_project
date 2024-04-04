import sys
import sqlite3
import datetime
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QFileDialog
from UiFiles.CreateTaskFormUFile import Ui_Form
from AudioFormWidget import AudioWidget
from CalendarFormWidget import CalendarWidget


class CreateTaskWidget(QDialog, Ui_Form):
    def __init__(self, parent=None, important=0, user_id=0):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.user_id = user_id
        self.important = important
        self.cancel.clicked.connect(self.cancel_func)
        self.audio.clicked.connect(self.audio_func)
        self.photo.clicked.connect(self.photo_func)
        self.calendar_button.clicked.connect(self.calendar_button_func)
        self.create_button.clicked.connect(self.create_button_func)
        self.description.setPlaceholderText('Описание задачи')
        self.setWindowTitle('Добавить задачу')

        self.audio_flag, self.photo_flag = True, True

        self.name_photo = ''
        self.name_audio = ''
        current_date = datetime.date.today()
        self.day, self.month, self.year = current_date.day, current_date.month, current_date.year

    def cancel_func(self):
        # функция предупреждающая в том случае если пользователь ввел в форму данные и хочет закрыть окно
        if self.name_task.text() != '' or self.description.toPlainText() != '' or self.name_audio != '' or self.name_photo != '':
            result = QMessageBox.question(self, 'Закрыть',
                                          'Вы действительно хотите закрыть? Несохраненная запись будет утеряна',
                                          buttons=QMessageBox.Yes | QMessageBox.No)
            if result == 16384:
                self.close()
        else:
            self.close()

    def audio_func(self):  # функция для записи голоса
        if self.audio_flag:
            self.Audio = AudioWidget(self, las_id_forFile=self.last_id_db())
            self.Audio.exec()
            done = self.Audio.is_done
            if done:
                self.name_audio = self.Audio.name_audio
                self.audio.setText('Удалить аудиозапись')
                self.audio_flag = False
        else:
            self.audio.setText('Добавить аудиозапись')
            self.name_audio = ''
            self.audio_flag = True

    def last_id_db(self):  # берет последний id из данных и прибавляет 1 (для уникального названия аудио и фото файлов)
        con = sqlite3.connect("BD/data_base.db")
        cur = con.cursor()
        result = cur.execute("SELECT id FROM table_task_db").fetchall()
        if result:
            return result[-1][0] + 1
        return 1

    def photo_func(self):  # функция для выбора фото посредством диалогового окна
        if self.photo_flag:
            self.fname, k = QFileDialog.getOpenFileName(self, 'выбрать картинку', '')

            if self.fname != '' and k != '':
                numb = self.last_id_db()
                self.name_photo = f'image{numb}.png'
                self.path_photo = f'saved_images/{self.name_photo}'

                self.photo.setText('Удалить фото')
                self.photo_flag = False
        else:
            self.photo.setText('Добавить изображение')
            self.name_photo = ''
            self.photo_flag = True

    def calendar_button_func(self):  # функция для выбора даты выполнения задачи
        self.Calendar = CalendarWidget(self)
        self.Calendar.exec()
        self.day, self.month, self.year = self.Calendar.date.day(), self.Calendar.date.month(), self.Calendar.date.year()

    def create_button_func(self):  # обработчик кнопки создать, записывает в базу данных задачу
        if self.name_task.text() == '':
            QMessageBox.information(self, 'Ошибка', 'Название задачи не должно быть пустым!',
                                    buttons=QMessageBox.Close, defaultButton=QMessageBox.Close)
        else:
            con = sqlite3.connect("BD/data_base.db")
            cur = con.cursor()
            self.name = self.name_task.text()
            self.desc = self.description.toPlainText()
            if self.name_photo:
                self.original = QImage(self.fname).save(self.path_photo)
            if self.name_audio:
                self.name_audio += '.wav'

            insert_command = f"INSERT INTO table_task_db(Name, Desc, Audio, Photo, Day, Month, Year, Important, user_id) VALUES('{self.name}', '{self.desc}', '{self.name_audio}','{self.name_photo}', '{self.day}', '{self.month}', '{self.year}', '{self.important}', '{self.user_id}')"
            cur.execute(insert_command).fetchall()
            con.commit()
            con.close()

            self.close()
