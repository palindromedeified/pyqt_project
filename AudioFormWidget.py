from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog
from PyQt5.QtMultimedia import QAudioRecorder, QAudioEncoderSettings, QMultimedia, QMediaRecorder
from UiFiles.AudioFormUFile import Ui_AudioForm
from PyQt5 import uic
import os
import sys


class AudioWidget(QDialog, Ui_AudioForm):
    def __init__(self, parent=None, las_id_forFile=1):
        QDialog.__init__(self, parent)

        self.name_audio = f'record{las_id_forFile}'
        self.path = fr'audio/{self.name_audio}'
        self.setupUi(self)
        self.is_done = False
        self.setWindowTitle("Запись звука")
        self.recorder = QAudioRecorder()
        self.recorder.setVolume(500)

        file = QUrl.fromLocalFile(os.path.abspath(self.path))
        self.recorder.setOutputLocation(file)
        self.recorder.setAudioInput(self.recorder.defaultAudioInput())

        self.recorder.statusChanged.connect(self.initRecorder)
        self.recorder.durationChanged.connect(self.showDuration)

        self.record_button.clicked.connect(self.recorder.record)
        self.pause_button.clicked.connect(self.recorder.pause)
        self.stop_button.clicked.connect(self.recorder.stop)

    def initRecorder(self, status):
        if status == QMediaRecorder.RecordingStatus:
            self.record_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            self.result.setText("Запись")

        elif status == QMediaRecorder.PausedStatus:
            self.record_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.result.setText("Пауза")

        elif status == QMediaRecorder.FinalizingStatus:
            self.record_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.result.setText("Готово")
            self.is_done = True
            self.close()

    def showDuration(self, duration):
        self.result.setText(f"Записано {duration // 1000} секунд")
