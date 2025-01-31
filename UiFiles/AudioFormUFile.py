# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AudioFormUFile.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AudioForm(object):
    def setupUi(self, AudioForm):
        AudioForm.setObjectName("AudioForm")
        AudioForm.resize(281, 88)
        self.record_button = QtWidgets.QPushButton(AudioForm)
        self.record_button.setGeometry(QtCore.QRect(10, 10, 81, 23))
        self.record_button.setStyleSheet("font-family: Verdana;\n"
"font-weight: bold;\n"
"font-size: 8pt;\n"
"border-radius: 10px;\n"
"color: white;\n"
"")
        self.record_button.setObjectName("record_button")
        self.pause_button = QtWidgets.QPushButton(AudioForm)
        self.pause_button.setEnabled(False)
        self.pause_button.setGeometry(QtCore.QRect(100, 10, 81, 23))
        self.pause_button.setStyleSheet("font-family: Verdana;\n"
"font-weight: bold;\n"
"font-size: 8pt;\n"
"border-radius: 10px;\n"
"color: white;\n"
"")
        self.pause_button.setObjectName("pause_button")
        self.stop_button = QtWidgets.QPushButton(AudioForm)
        self.stop_button.setEnabled(False)
        self.stop_button.setGeometry(QtCore.QRect(190, 10, 81, 23))
        self.stop_button.setStyleSheet("font-family: Verdana;\n"
"font-weight: bold;\n"
"font-size: 8pt;\n"
"border-radius: 10px;\n"
"color: white;")
        self.stop_button.setObjectName("stop_button")
        self.result = QtWidgets.QLabel(AudioForm)
        self.result.setGeometry(QtCore.QRect(10, 40, 251, 31))
        self.result.setObjectName("result")

        self.retranslateUi(AudioForm)
        QtCore.QMetaObject.connectSlotsByName(AudioForm)

    def retranslateUi(self, AudioForm):
        _translate = QtCore.QCoreApplication.translate
        AudioForm.setWindowTitle(_translate("AudioForm", "Аудио"))
        self.record_button.setText(_translate("AudioForm", "Запись"))
        self.pause_button.setText(_translate("AudioForm", "Пауза"))
        self.stop_button.setText(_translate("AudioForm", "Стоп"))
        self.result.setText(_translate("AudioForm", "Готово"))
