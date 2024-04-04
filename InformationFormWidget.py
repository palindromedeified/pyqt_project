import sqlite3
from PyQt5 import uic
from PyQt5.QtCore import QRectF, Qt, QRect, QUrl
from PyQt5.QtGui import QImage, QPixmap, QMouseEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyle, QDialog, QLabel, QDesktopWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from UiFiles.InformationFormUFile import Ui_Form


class InformationWidget(QDialog, Ui_Form):
    def __init__(self, parent=None, id=None):
        QDialog.__init__(self, parent)

        self.setupUi(self)
        con = sqlite3.connect("BD/data_base.db")
        cur = con.cursor()
        db_id, name, desc, audio, self.photo, day, month, year, important, id_user = \
            cur.execute(f"SELECT * FROM table_task_db WHERE id = '{id}'").fetchall()[0]

        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

        if audio != '':
            self.openFile_audio('audio/' + audio)
        if self.photo != '':
            self.openFile_photo('saved_images/' + self.photo)
        else:
            self.photo_label.setText('image.png')

        self.playBtn.clicked.connect(self.play_audio)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.setStyleSheet("border-radius: 10px; background-color: #7dabf6;")
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # Name
        self.name_label.setText(' ' + name)
        # Desc
        self.DescPlainText.setPlainText(desc)
        self.DescPlainText.setEnabled(False)
        # Date
        self.date_label.setText(f' {day}.{month}.{year}')

        self.setWindowTitle('Информация о задаче')

    def openFile_audio(self, file):  # открываем файл аудио
        self.mediaPlayer.setMedia(QMediaContent(QUrl(file)))

    def play_audio(self):  # воспроизводит аудио запись и останавливает ее по нажатию кнопки
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediastate_changed(self, state):  # меняет иконку кнопки в зависимости от ее состояния
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def openFile_photo(self, file):  # открываем файл фото
        self.fname = file

        self.img = QImage(self.fname)
        self.x, self.y = self.img.width(), self.img.height()
        self.img_resized = self.img.scaled(271, 221)
        self.imagePixmap = QPixmap(self.img_resized)
        self.photo_label.setPixmap(self.imagePixmap)

    def mouseDoubleClickEvent(self,
                              a0):  # обработчик двойного клика по фото чтобы оно развернулось в своем первоначальном размере
        if 210 <= a0.x() <= 481 and 10 <= a0.y() <= 231 and self.photo != '':
            img = ShowImage(self, w=self.x, h=self.y, file=self.fname)  # открываем окно для данного фото
            img.exec()


class ShowImage(QDialog):
    def __init__(self, parent=None, w=None, h=None, file=None):
        QDialog.__init__(self, parent)
        self.setFixedSize(w, h)
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, w, h)

        screen = QDesktopWidget().screenGeometry()
        self.move((screen.width() - w) / 2,
                  (screen.height() - h) / 2)

        self.img = QImage(file)
        self.imagePixmap = QPixmap(self.img)
        self.label.setPixmap(self.imagePixmap)
