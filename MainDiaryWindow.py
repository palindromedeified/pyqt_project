import sys
import sqlite3
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QIcon, QPainter, QBrush
from PyQt5.QtWidgets import (QMainWindow, QApplication,
                             QListWidgetItem,
                             QDialog, QLineEdit, QMessageBox)
import os
from UiFiles.untitled import Ui_MainWindow
from CreateTaskFormWidget import CreateTaskWidget
from InformationFormWidget import InformationWidget
from MainCalendarFormWidget import MainCalendarWidget
from UiFiles.createacc import Ui_CreateUser
from UiFiles.logini import Ui_Login


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.func_login()
        self.setupUi(self)
        self.setFixedSize(400, 570)
        self.add_task.clicked.connect(self.add_task_func)
        self.perform_button.clicked.connect(self.perform_func)

        self.taskListWidget.itemDoubleClicked.connect(self.get_info_about_task)
        self.taskListWidget_2.itemDoubleClicked.connect(self.get_info_about_task)

        self.search_line_edit.textChanged.connect(self.change_search_line_edit)
        self.search_line_edit_2.textChanged.connect(self.change_search_line_edit)

        self.important_button.clicked.connect(self.important_tasks_func)
        self.important_button.setStyleSheet('background-color: #ffaa00; border-radius: 25px')
        self.setStyleSheet(open('stylesheet/style.css', 'r').read())

        self.tabWidget.currentChanged.connect(self.on_tab_changed)

        self.search_btn.clicked.connect(self.search_func)
        self.search_btn2.clicked.connect(self.search_func)

        self.on_tab = self.tabWidget.indexOf(self.tabWidget.currentWidget())

        self.calendar_btn.clicked.connect(self.open_calendar_func)

        self.update_all()

    def func_login(self):  # функция открытия окна для авторизации
        login = Login(self)
        login.exec_()
        if login.access is True:
            self.user_id = login.id_user
        else:
            sys.exit(self.close())

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        color_bottom = QColor(250, 250, 250)
        color_shadow = QColor(230, 236, 235)
        qp.setPen(color_bottom)

        # Нижняя панель с кнопками
        qp.setBrush(QBrush(color_bottom, Qt.SolidPattern))
        qp.drawRect(QRectF(0, 510, 400, 100))

        # Тень от нижней панели
        qp.setBrush(QBrush(color_shadow, Qt.SolidPattern))
        qp.drawRect(QRectF(0, 507, 400, 3))

        qp.end()

    def add_task_func(self):  # добавляем задачу
        self.clear_all()
        if self.on_tab == 0:
            create_task = CreateTaskWidget(self, important=0, user_id=self.user_id)
        else:
            create_task = CreateTaskWidget(self, important=1, user_id=self.user_id)
        create_task.exec()

        self.update_all()

    def global_updateTask(self, obj, key=''):  # общая функция для обновления списка задач на экране
        obj.clear()
        con = sqlite3.connect("BD/data_base.db")
        cur = con.cursor()

        if obj.objectName() == 'taskListWidget':
            if key != '':
                result = cur.execute(key).fetchall()
            else:
                result = cur.execute(f"SELECT * FROM table_task_db WHERE user_id = '{self.user_id}'").fetchall()

        elif obj.objectName() == 'taskListWidget_2':
            if key != '':
                result = cur.execute(key).fetchall()
            else:
                result = cur.execute(
                    f"SELECT * FROM table_task_db WHERE Important = 1 and user_id = '{self.user_id}'").fetchall()

        for task in result:
            item = QListWidgetItem(task[1])
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            obj.addItem(item)

        obj.setStyleSheet(
            'border: 0px; font-size: 10pt; font-family: Verdana, serif; color: black; font-weight: bold;')
        con.close()

    def updateTaskList(self, key=''):  # обновляется окно на вкладке 'все задачи'
        self.global_updateTask(self.taskListWidget, key)

    def updateImportantTaskList(self, key=''):  # обновляется окно на вкладке 'важные'
        self.global_updateTask(self.taskListWidget_2, key)

    def perform_func(self):  # удаляет из базы выполненные задачи
        con = sqlite3.connect("BD/data_base.db")
        cur = con.cursor()
        obj = self.taskListWidget if self.on_tab == 0 else self.taskListWidget_2

        if self.on_tab == 0:
            key = self.search_line_edit.text()
            if key:
                key = key.split('.')
                request = f"SELECT * FROM table_task_db WHERE day = '{key[0]}' and month = '{key[1]}' and year = '{key[2]}' and user_id = '{self.user_id}'"
            else:
                request = f"SELECT * FROM table_task_db WHERE user_id = '{self.user_id}'"
            result = cur.execute(request).fetchall()
        else:
            key = self.search_line_edit_2.text()
            if key:
                key = key.split('.')
                request = f"SELECT * FROM table_task_db WHERE important = 1 and day = '{key[0]}' and month = '{key[1]}' and year = '{key[2]}' and user_id = '{self.user_id}'"
            else:
                request = f"SELECT * FROM table_task_db WHERE important = 1 and user_id = '{self.user_id}'"

            result = cur.execute(request).fetchall()

        for i in range(obj.count()):
            item = obj.item(i)
            if item.checkState() == Qt.Checked:
                if result[i][3] != '':
                    self.delete_files(result[i][3], 0)
                if result[i][4] != '':
                    self.delete_files(result[i][4], 1)

                cur.execute(f"DELETE FROM table_task_db WHERE id = '{result[i][0]}'").fetchall()

        con.commit()
        con.close()
        if key:
            self.updateTaskList(request)
            self.updateImportantTaskList(request)
        else:
            self.update_all()

    def delete_files(self, file_name, aud_pht=0):  # функция для удаления файлов
        # чтобы при нажатии на кнопку выполнить аудио и видео файлы не висели в папке просто так
        if aud_pht == 0:
            os.remove(f'audio/{file_name}')
        elif aud_pht == 1:
            os.remove(f'saved_images/{file_name}')

    def set_item_unchecked(self, obj):
        for i in range(obj.count()):
            obj.item(i).setCheckState(Qt.Unchecked)

    def important_tasks_func(self):  # ставит в базе данных 1 в столбце important
        con = sqlite3.connect("BD/data_base.db")
        cur = con.cursor()
        result = cur.execute(f"SELECT * FROM table_task_db WHERE user_id = '{self.user_id}'").fetchall()

        for i in range(self.taskListWidget.count()):
            item = self.taskListWidget.item(i)
            if item.checkState() == Qt.Checked:
                item.setCheckState(Qt.Unchecked)
                cur.execute(
                    f"UPDATE table_task_db SET Important = 1 WHERE id = '{result[i][0]}' and user_id = '{self.user_id}'").fetchall()

        con.commit()
        con.close()
        self.updateImportantTaskList()

    def get_info_about_task(self):  # выводит окно показывающее подробную информацию о задаче
        con = sqlite3.connect("BD/data_base.db")
        cur = con.cursor()
        result = cur.execute(f"SELECT * FROM table_task_db WHERE user_id = '{self.user_id}'").fetchall()

        obj = self.taskListWidget if self.on_tab == 0 else self.taskListWidget_2
        temp = obj.currentItem().text()

        for i in range(self.taskListWidget.count()):
            item = self.taskListWidget.item(i).text()
            if item == temp:
                form = InformationWidget(self, id=result[i][0])
                form.exec()

    def on_tab_changed(self):  # функция для того, чтобы узнать на какой вкладке сейчас находимся
        self.on_tab = self.tabWidget.indexOf(self.tabWidget.currentWidget())
        self.clear_all()
        self.set_item_unchecked(self.taskListWidget)
        self.set_item_unchecked(self.taskListWidget_2)
        self.update_all()

    def update_all(self):  # обновляем списки задач
        self.updateTaskList()
        self.updateImportantTaskList()

    def clear_all(self):  # удаляем все из поля ввода
        self.search_line_edit.clear()
        self.search_line_edit_2.clear()

    def search_func(self):  # функция поиска задач
        obj_text = self.search_line_edit.text() if self.on_tab == 0 else self.search_line_edit_2.text()
        if obj_text != '':
            like = f'%{obj_text}%'
            self.updateTaskList(f"SELECT * FROM table_task_db WHERE name LIKE '{like}' and user_id = '{self.user_id}'")
            self.updateImportantTaskList(
                f"SELECT * FROM table_task_db WHERE name LIKE '{like}' and Important = 1 and user_id = '{self.user_id}'")

    def change_search_line_edit(self):
        # в случае удаления очистки search_line_edit или search_line_edit_2 на экран выведутся все задачи
        obj_text = self.search_line_edit.text() if self.on_tab == 0 else self.search_line_edit_2.text()
        if obj_text == '':
            self.update_all()

    def open_calendar_func(self):  # открываем календарь из главного окна
        self.Calendar = MainCalendarWidget()
        self.Calendar.exec_()

        if self.Calendar.is_done:
            day_2, month_2, year_2 = self.Calendar.day, self.Calendar.month, self.Calendar.year
            request = f"SELECT * FROM table_task_db WHERE Day = '{day_2}' and Month = '{month_2}' and Year = '{year_2}' and user_id = '{self.user_id}'"
            request_important = f"SELECT * FROM table_task_db WHERE Day = '{day_2}' and Month = '{month_2}' and Year = '{year_2}' and Important = 1 and user_id = '{self.user_id}'"

            self.updateTaskList(request)
            self.search_line_edit.setText(f'{day_2}.{month_2}.{year_2}')
            self.updateImportantTaskList(request_important)
            self.search_line_edit_2.setText(f'{day_2}.{month_2}.{year_2}')


class Login(QDialog, Ui_Login):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.setupUi(self)
        self.setStyleSheet(open('stylesheet/style.css', 'r').read())
        self.setWindowTitle('Login')
        self.setFixedSize(272, 159)
        self.loginbutton.clicked.connect(self.login_function)
        self.password.setEchoMode(QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.go_to_create)
        self.access = False

    def login_function(self):  # проверяем есть ли в базе такой логин и пароль
        login = self.login.text()
        password = self.password.text()
        con = sqlite3.connect("BD/data_base.db")
        cur = con.cursor()
        result = cur.execute(f"SELECT * FROM users").fetchall()

        for i in result:
            if i[1] == login and i[2] == password:
                user = i
                self.access = True
        if self.access:
            self.id_user = user[0]
            self.close()
        else:
            QMessageBox.warning(
                self, 'Ошибка', 'Неправильное имя или пароль')
        con.close()

    def go_to_create(self):  # открывает окно с формой для создания логина и пароля
        create_acc = CreateAcc()
        create_acc.exec_()


class CreateAcc(QDialog, Ui_CreateUser):
    def __init__(self):
        super(CreateAcc, self).__init__()
        self.setupUi(self)
        self.setStyleSheet(open('stylesheet/style.css', 'r').read())
        self.setWindowTitle('Registration')
        self.setFixedSize(381, 156)
        self.sign_up_button.clicked.connect(self.create_acc_function)
        self.password.setEchoMode(QLineEdit.Password)
        self.confirmpass.setEchoMode(QLineEdit.Password)
        self.cancel_btn.clicked.connect(lambda x: self.close())

    def create_acc_function(self):  # создаем логин и пароль
        login_ = self.login.text()
        password = self.password.text()
        con = sqlite3.connect("BD/data_base.db")
        cur = con.cursor()
        result = cur.execute(f"SELECT * FROM users").fetchall()
        flag = True
        for i in result:
            if i[1] == login_:
                flag = False
        if self.password.text() == self.confirmpass.text() and login_ != '' and password != '' and flag:
            insert_command = f"INSERT INTO users(login, password) VALUES('{login_}', '{password}')"
            cur.execute(insert_command).fetchall()
            self.close()
        else:
            QMessageBox.warning(
                self, 'Ошибка', 'Неправильное имя или пароль')
        con.commit()
        con.close()


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(r"images/diary.png"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
