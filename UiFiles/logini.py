# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logini.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(274, 159)
        Login.setStyleSheet("")
        self.label = QtWidgets.QLabel(Login)
        self.label.setGeometry(QtCore.QRect(10, 10, 251, 21))
        self.label.setStyleSheet("font-size: 15pt;\n"
"font-family: Verdana, serif;\n"
"color: black;\n"
"font-weight: bold;")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Login)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 51, 21))
        self.label_2.setStyleSheet("font-size: 10pt;\n"
"font-family: Verdana, serif;\n"
"color: black;\n"
"font-weight: bold;")
        self.label_2.setObjectName("label_2")
        self.login = QtWidgets.QLineEdit(Login)
        self.login.setGeometry(QtCore.QRect(70, 50, 191, 21))
        self.login.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font-size: 10pt;")
        self.login.setObjectName("login")
        self.password = QtWidgets.QLineEdit(Login)
        self.password.setGeometry(QtCore.QRect(70, 80, 191, 21))
        self.password.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font-size: 10pt;")
        self.password.setText("")
        self.password.setObjectName("password")
        self.label_3 = QtWidgets.QLabel(Login)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 51, 21))
        self.label_3.setStyleSheet("font-size: 10pt;\n"
"font-family: Verdana, serif;\n"
"color: black;\n"
"font-weight: bold;")
        self.label_3.setObjectName("label_3")
        self.loginbutton = QtWidgets.QPushButton(Login)
        self.loginbutton.setGeometry(QtCore.QRect(10, 120, 81, 21))
        self.loginbutton.setStyleSheet("font-family: Verdana;\n"
"font-weight: bold;\n"
"font-size: 8pt;\n"
"border-radius: 10px;\n"
"color: white;")
        self.loginbutton.setObjectName("loginbutton")
        self.createaccbutton = QtWidgets.QPushButton(Login)
        self.createaccbutton.setGeometry(QtCore.QRect(180, 120, 81, 21))
        self.createaccbutton.setStyleSheet("font-family: Verdana;\n"
"font-weight: bold;\n"
"font-size: 8pt;\n"
"border-radius: 10px;\n"
"color: white;")
        self.createaccbutton.setObjectName("createaccbutton")

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Dialog"))
        self.label.setText(_translate("Login", "Вход"))
        self.label_2.setText(_translate("Login", "Логин"))
        self.label_3.setText(_translate("Login", "Пароль"))
        self.loginbutton.setText(_translate("Login", "Войти"))
        self.createaccbutton.setText(_translate("Login", "Создать"))
