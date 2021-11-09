from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QPushButton, QListWidget, QHBoxLayout, \
    QVBoxLayout, QSlider, QListWidgetItem, QMenu, QMessageBox, QLineEdit
from PyQt5.QtGui import QPixmap, QIcon, QFont, QCursor
from PyQt5.QtCore import Qt, QSize, QUrl, QSettings, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from collections import defaultdict
import os
import time
from abs_path import abs_path

list_items = []
user_playlists = defaultdict(list)

style = '''
QPushButton {
	background-color: #8e949c;
	border: 1px solid black;
	border-radius: 4px;
}

QPushButton:hover {
	color: #fff;
}

QPushButton:pressed {
	color: #b895878c9116;
    background-color: #ccc;
}
'''


app = QApplication([])
player = QWidget()
player.setGeometry(300, 250, 1000, 500)
player.setWindowTitle('AudioPlayer')
player.setStyleSheet('background-color: #40424f')

playlist_win = QWidget(player, Qt.Window)
playlist_win.setGeometry(450, 300, 700, 400)
playlist_win.setFixedSize(700, 400)
playlist_win.setStyleSheet('background-color: #40424f')

media = QMediaPlayer()

settings = QSettings('AudioPlayer', 'Personality')

timer = QTimer()
timer.start(1000)

font = QFont('Arial', 16, QFont.Cursive)
font_info = QFont('Arial', 15, QFont.Cursive)
lb_info = QLabel()
lb_info.setStyleSheet('color: #ccc')
lb_info.setFont(font_info)
lb_music = QLabel()
lb_volume = QLabel()
pixmap = QPixmap(abs_path('images/med.png'))
pixmap = pixmap.scaled(35, 35)
lb_volume.setPixmap(pixmap)
lb_music_time = QLabel('00:00')
lb_music_time.setStyleSheet('color: #ccc')
lb_length_music = QLabel('00:00')
lb_length_music.setStyleSheet('color: #ccc')
lb_info_tip = QLabel('Нажмите два раза что-бы добавить композицию')
lb_info_tip.setStyleSheet('color: #ccc')
btn_create = QPushButton('Создать плейлист')
btn_create.setStyleSheet(style)
btn_save_playlist = QPushButton('Сохранить плейлист')
btn_save_playlist.setStyleSheet(style)
btn_dir = QPushButton('Добавить музыку')
btn_dir.setStyleSheet(style)
btn_save = QPushButton('Сохранить файлы')
btn_save.setStyleSheet(style)
files = QListWidget()
files.setStyleSheet('background-color: #8e949c; border: 1px solid black; border-radius: 10px;')
files.installEventFilter(player)
list_playlist = QListWidget()
list_playlist.setStyleSheet('background-color: #8e949c; border: 1px solid black; border-radius: 10px;')
list_playlist.installEventFilter(player)
items = QListWidget()
items.setStyleSheet('background-color: #8e949c; border: 1px solid black; border-radius: 10px;')
name_playlist = QLineEdit()
name_playlist.setPlaceholderText('Введи имя плейлиста')
slider = QSlider(Qt.Horizontal)
slider.setMinimum(0)
slider.setMaximum(10000)
slider.setValue(0)
slider.setSingleStep(1)
volume_slider = QSlider(Qt.Vertical)
volume_slider.setMinimum(0)
volume_slider.setMaximum(100)
volume_slider.setValue(75)
volume_slider.setSingleStep(1)
btn_previous = QPushButton()
btn_previous.setStyleSheet(style)
btn_previous.setIcon(QIcon(abs_path('images/left.png')))
btn_previous.setIconSize(QSize(45, 45))
btn_previous.setFixedSize(75, 45)
btn_pause = QPushButton()
btn_pause.setStyleSheet('border-radius: 23px')
btn_pause.setIcon(QIcon(abs_path('images/pause.png')))
btn_pause.setIconSize(QSize(45, 45))
btn_pause.setFixedSize(45, 45)
btn_unpause = QPushButton()
btn_unpause.setStyleSheet('border-radius: 23px')
btn_unpause.setIcon(QIcon(abs_path('images/play-button.png')))
btn_unpause.setIconSize(QSize(45, 45))
btn_unpause.setFixedSize(45, 45)
btn_next = QPushButton()
btn_next.setStyleSheet(style)
btn_next.setIcon(QIcon(abs_path('images/right.png')))
btn_next.setIconSize(QSize(45, 45))
btn_next.setFixedSize(75, 45)
btn_uncycle = QPushButton()
btn_uncycle.setStyleSheet(style)
btn_uncycle.setIcon(QIcon(abs_path('images/cycle.png')))
btn_uncycle.setIconSize(QSize(25, 25))
btn_cycle = QPushButton()
btn_cycle.setStyleSheet(style)
btn_cycle.setIcon(QIcon(abs_path('images/cycle1.png')))
btn_cycle.setIconSize(QSize(25, 25))
btn_back = QPushButton('Назад')
btn_next_step = QPushButton('Дальше')
btn_create_list = QPushButton('Создать Плейлист')

row = QHBoxLayout()
col_playlist = QVBoxLayout()
set_horizontal = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col_playlist.addWidget(btn_create)
col_playlist.addWidget(btn_save_playlist)
col_playlist.addWidget(list_playlist)
col1.addWidget(btn_dir)
col1.addWidget(btn_save)
col1.addWidget(files)
col2.addWidget(lb_info)
col2.addWidget(lb_music, 95, alignment=(Qt.AlignVCenter | Qt.AlignHCenter))
volume_tool = QVBoxLayout()
volume_tool.addWidget(lb_volume, alignment=Qt.AlignRight)
volume_tool.addWidget(volume_slider, alignment=Qt.AlignRight)
time_tool = QHBoxLayout()
time_tool.addWidget(lb_music_time)
time_tool.addWidget(lb_length_music, alignment=Qt.AlignRight)
slider_tool = QVBoxLayout()
slider_tool.addWidget(slider)
row_tools = QHBoxLayout()
row_tools.addWidget(btn_previous)
row_tools.addWidget(btn_pause)
btn_pause.hide()
row_tools.addWidget(btn_unpause)
row_tools.addWidget(btn_next)
cycle_tool = QHBoxLayout()
cycle_tool.addWidget(btn_uncycle, alignment=Qt.AlignRight)
cycle_tool.addWidget(btn_cycle, alignment=Qt.AlignRight)
btn_cycle.hide()
slider_tool.addLayout(cycle_tool)
slider_tool.addLayout(row_tools)
set_horizontal.addLayout(col_playlist)
set_horizontal.addLayout(col1)
col2.addLayout(volume_tool)
col2.addLayout(time_tool)
col2.addLayout(slider_tool)

row.addLayout(set_horizontal, 50)
row.addLayout(col2, 80)
player.setLayout(row)

workdir = None


def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


def filter(filenames, extension):
    result = []
    for filename in filenames:
        for i in extension:
            if filename.endswith(i):
                result.append(filename)
    return result


def showFilenamesList():
    files.clear()
    list_items.clear()
    saveSetting()
    extensions = ['.mp3']
    repeat = []
    chooseWorkdir()
    # noinspection PyTypeChecker
    if len(workdir) > 0:
        filenames = filter(os.listdir(workdir), extensions)
        for value in range(files.count()):
            repeat.append(files.item(value).text())
        for filename in filenames:
            if filename not in repeat:
                item = QListWidgetItem(filename)
                files.addItem(item)
                list_items.append(filename)


def createPlaylistWin():
    playlist_win.setWindowModality(Qt.WindowModal)

    name_playlist.clear()
    name_playlist.show()
    btn_back.show()
    btn_next_step.show()

    lb_info_tip.setFont(font)
    name_playlist.setFixedSize(400, 50)
    name_playlist.setFont(font)
    name_playlist.setStyleSheet('color: #fff')
    items.setFixedSize(650, 270)
    btn_back.setFixedSize(200, 35)
    btn_back.setStyleSheet(style)
    btn_next_step.setFixedSize(200, 35)
    btn_next_step.setStyleSheet(style)
    btn_create_list.setFixedSize(200, 35)
    btn_create_list.setStyleSheet(style)

    col = QVBoxLayout()
    layout_v = QVBoxLayout()
    layout_h = QHBoxLayout()

    layout_v.addWidget(lb_info_tip)
    lb_info_tip.hide()
    layout_v.addWidget(name_playlist, alignment=Qt.AlignCenter)
    layout_v.addWidget(items, alignment=Qt.AlignCenter)
    items.hide()
    layout_h.addWidget(btn_back, alignment=Qt.AlignBottom)
    layout_h.addWidget(btn_create_list, alignment=Qt.AlignBottom)
    btn_create_list.hide()
    layout_h.addWidget(btn_next_step, alignment=Qt.AlignBottom)
    col.addLayout(layout_v)
    col.addLayout(layout_h)
    playlist_win.setLayout(col)

    btn_back.clicked.connect(hideWindow)

    playlist_win.show()

user_text = None


def nextStep():
    global user_text
    repeat = []
    user_text = name_playlist.text()
    if len(user_text) > 0:
        name_playlist.hide()
        btn_next_step.hide()
        btn_back.hide()
        lb_info_tip.show()
        items.show()
        btn_create_list.show()

        for value in range(items.count()):
            repeat.append(items.item(value).text())
        for filename in range(files.count()):
            if files.item(filename).text() not in repeat:
                item = QListWidgetItem(files.item(filename).text())
                items.addItem(item)


def addItemToPlaylist():
    item = items.selectedItems()[0]
    if item.text() not in user_playlists[user_text]:
        user_playlists[user_text].append(item.text())
        icon = QIcon(abs_path('images/check.png'))
        item.setIcon(icon)
        items.setIconSize(QSize(20, 20))


def createPlaylist():
    if len(user_playlists[user_text]) > 0:
        item = QListWidgetItem(user_text)
        list_playlist.addItem(item)

        items.clear()
        playlist_win.hide()


def hideWindow():
    items.clear()
    playlist_win.hide()


class AudioProcessor:
    def __init__(self, filename):
        self.filename = filename

        # noinspection PyTypeChecker
        self.path = os.path.join(workdir, self.filename)

    def playFile(self):
        btn_unpause.hide()
        btn_pause.show()
        btn_cycle.hide()
        btn_uncycle.show()
        if len(self.path) < 50:
            lb_info.setText(f'                        name: {self.filename}\n                        path: {self.path}')
        else:
            lb_info.setText(f'                        name: {self.filename}')
        media.setMedia(QMediaContent(QUrl.fromLocalFile(self.path)))
        pixmap = QPixmap(abs_path('images/headphones.png'))
        pixmap = pixmap.scaled(125, 125, Qt.KeepAspectRatio)
        lb_music.setPixmap(pixmap)

        media.play()

    @staticmethod
    def pause():
        btn_pause.hide()
        btn_unpause.show()
        media.pause()

    @staticmethod
    def unpause():
        btn_unpause.hide()
        btn_pause.show()
        media.play()

    def previousOrNext(self):
        btn_unpause.hide()
        btn_pause.show()
        btn_cycle.hide()
        btn_uncycle.show()
        lb_info.setText(f'                        name: {self.filename}\n                        path: {self.path}')
        media.setMedia(QMediaContent(QUrl.fromLocalFile(self.path)))
        media.play()

    def cycle(self):
        btn_uncycle.hide()
        btn_cycle.show()
        media.stop()
        playlist = QMediaPlaylist(media)
        playlist.addMedia(QMediaContent(QUrl.fromLocalFile(self.path)))
        playlist.setPlaybackMode(QMediaPlaylist.Loop)
        media.setPlaylist(playlist)
        media.play()

    def destroyCycle(self):
        btn_cycle.hide()
        btn_uncycle.show()
        media.stop()
        media.setMedia(QMediaContent(QUrl.fromLocalFile(self.path)))
        media.play()


def showChosenAudio():
    filename = files.selectedItems()[0].text()
    workaudio = AudioProcessor(filename)
    workaudio.playFile()


def showPause():
    filename = files.selectedItems()[0].text()
    workaudio = AudioProcessor(filename)
    workaudio.pause()


def showUnpause():
    try:
        filename = files.selectedItems()[0].text()
        workaudio = AudioProcessor(filename)
        workaudio.unpause()
    except IndexError:
        pass


def showPrevious():
    try:
        index = files.currentRow()
        new_index = index - 1
        filename = files.item(new_index).text()
        files.setCurrentItem(files.item(new_index))
        workaudio = AudioProcessor(filename)
        workaudio.previousOrNext()
    except AttributeError:
        pass


def showNext():
    try:
        index = files.currentRow()
        new_index = index + 1
        filename = files.item(new_index).text()
        files.setCurrentItem(files.item(new_index))
        workaudio = AudioProcessor(filename)
        workaudio.previousOrNext()
    except AttributeError:
        pass


def positionChanged(position):
    slider.setValue(position)


def durationChanged(duration):
    slider.setRange(0, duration)
    minutes = duration // 1000 // 60
    seconds = duration // 1000 % 60
    lb_length_music.setText(f'{minutes:>1}:{seconds:0>2}')


def sliderMoved(pos):
    media.setPosition(pos)


def volumeMoved(vol):
    media.setVolume(vol)


def changeValue(value):
    if value == 0:
        pixmap = QPixmap(abs_path('images/mute.png'))
        pixmap = pixmap.scaled(35, 35)
        lb_volume.setPixmap(pixmap)
    elif 0 < value <= 30:
        pixmap = QPixmap(abs_path('images/min.png'))
        pixmap = pixmap.scaled(35, 35)
        lb_volume.setPixmap(pixmap)
    elif 30 < value < 70:
        pixmap = QPixmap(abs_path('images/med.png'))
        pixmap = pixmap.scaled(35, 35)
        lb_volume.setPixmap(pixmap)
    else:
        pixmap = QPixmap(abs_path('images/max.png'))
        pixmap = pixmap.scaled(35, 35)
        lb_volume.setPixmap(pixmap)


def timeMode():
    try:
        lb_music_time.setText(time.strftime('%M:%S', time.localtime(media.position() / 1000)))
    except KeyboardInterrupt:
        pass


def eventFilter():
    menu = QMenu()
    menu.addAction('Delete')
    menu.setStyleSheet('background-color: #8e949c; border: 1px solid black; border-radius: 4px')
    if menu.exec_(QCursor.pos()):
        item = files.selectedItems()[0]
        files.takeItem(files.row(item))
        list_items.remove(item.text())

        media.stop()
        media.setMedia(QMediaContent(None))
        slider.setValue(0)
        lb_music_time.setText('00:00')
        lb_length_music.setText('00:00')
        lb_info.setText(None)
        btn_pause.hide()
        btn_unpause.show()

        saveSetting()


def showCycle():
    try:
        filename = files.selectedItems()[0].text()
        workaudio = AudioProcessor(filename)
        workaudio.cycle()
    except IndexError:
        pass


def showUnCycle():
    try:
        filename = files.selectedItems()[0].text()
        workaudio = AudioProcessor(filename)
        workaudio.destroyCycle()
    except IndexError:
        pass


def showPlaylist():
    media.stop()
    btn_unpause.hide()
    btn_pause.show()
    btn_cycle.hide()
    btn_uncycle.show()
    pixmap = QPixmap(abs_path('images/headphones.png'))
    pixmap = pixmap.scaled(125, 125, Qt.KeepAspectRatio)
    lb_music.setPixmap(pixmap)
    playlist = QMediaPlaylist(media)
    for file in user_playlists[list_playlist.selectedItems()[0].text()]:
        path = os.path.join(workdir, file)
        print(path)
        playlist.addMedia(QMediaContent(QUrl.fromLocalFile(path)))
    lb_info.setText(f'                         Playlist-name: {list_playlist.selectedItems()[0].text()}')
    media.setPlaylist(playlist)
    media.play()


def action():
    if len(files) > 0:
        saveSetting()

        info_window = QMessageBox()
        info_window.setIcon(QMessageBox.Information)
        info_window.setStyleSheet('background-color: #40424f; color: #ccc;')
        info_window.setText(f'Ваши файлы:\n\n{list_items}\n\nуспешено сохранены!')
        info_window.exec_()


def saveSetting():
    settings.setValue('ListData', list_items)
    settings.setValue('workdir', workdir)


def loadSetting():
    global workdir
    if settings.contains('ListData'):
        for i in settings.value('ListData'):
            item = QListWidgetItem(i)
            files.addItem(item)
            list_items.append(i)
    if settings.contains('workdir'):
        workdir = settings.value('workdir')


btn_dir.clicked.connect(showFilenamesList)
btn_create.clicked.connect(createPlaylistWin)
files.itemClicked.connect(showChosenAudio)
btn_pause.clicked.connect(showPause)
btn_unpause.clicked.connect(showUnpause)
btn_previous.clicked.connect(showPrevious)
btn_next.clicked.connect(showNext)
media.positionChanged.connect(positionChanged)
media.durationChanged.connect(durationChanged)
slider.valueChanged.connect(sliderMoved)
volume_slider.valueChanged.connect(volumeMoved)
volume_slider.valueChanged.connect(changeValue)
timer.timeout.connect(timeMode)
btn_save.clicked.connect(action)
files.itemDoubleClicked.connect(eventFilter)
btn_cycle.clicked.connect(showUnCycle)
btn_uncycle.clicked.connect(showCycle)
btn_next_step.clicked.connect(nextStep)
items.itemDoubleClicked.connect(addItemToPlaylist)
btn_create_list.clicked.connect(createPlaylist)
list_playlist.itemClicked.connect(showPlaylist)


loadSetting()
player.show()
app.exec_()
