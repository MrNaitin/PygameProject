from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.Qt import QImage
from PyQt5.QtGui import QPixmap
from player import *
from blocks import *
from monsters import *
import pygame
import sys


WIN_WIDTH = 800
WIN_HEIGHT = 570
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#000000"


class Ui_main(object):

    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(1280, 720)
        main_window.setMinimumSize(QtCore.QSize(960, 540))
        main_window.setMaximumSize(QtCore.QSize(1920, 1080))
        font = QtGui.QFont()
        font.setFamily("Poor Richard")
        font.setPointSize(26)
        main_window.setFont(font)
        main_window.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        main_window.setStyleSheet("background-color: rgb(158, 158, 158);")
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.Start_button = QtWidgets.QPushButton(self.centralwidget)
        self.Start_button.setGeometry(QtCore.QRect(510, 290, 180, 50))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(19)
        self.Start_button.setFont(font)
        self.Start_button.setStyleSheet("background-color: rgb(90, 90, 90);")
        self.Start_button.setObjectName("Start_button")
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(420, 80, 350, 174))
        self.title_label.setTextFormat(QtCore.Qt.RichText)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(19)
        self.Quit_button = QtWidgets.QPushButton(self.centralwidget)
        self.Quit_button.setGeometry(QtCore.QRect(510, 360, 180, 50))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(19)
        self.Quit_button.setFont(font)
        self.Quit_button.setStyleSheet("background-color: rgb(90, 90, 90);")
        self.Quit_button.setObjectName("Quit_button")
        main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Main menu"))
        self.Start_button.setText(_translate("main_window", "Начать играть"))
        self.title_label.setText(_translate("main_window", ""))
        self.Quit_button.setText(_translate("main_window", "Выход"))


class Main_Window(Ui_main, QMainWindow):

    def __init__(self):
        super(Main_Window, self).__init__()
        self.setupUi(self)
        self.title_label.setPixmap(QPixmap(QImage("data/Title/titlescreen.png")))
        self.Quit_button.clicked.connect(self.quit)
        self.Start_button.clicked.connect(self.start)

    def quit(self):
        self.close()

    def start(self):
        self.close()
        main()


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)
    l = max(-(camera.width - WIN_WIDTH), l)
    t = max(-(camera.height - WIN_HEIGHT), t)
    t = min(0, t)

    return Rect(l, t, w, h)


def loadLevel():
    global playerX, playerY

    levelFile = open('data/levels/level.txt')
    line = levelFile.readline()
    while line[0] != "]":
        line = levelFile.readline()
        if line[0] != "]":
            endLine = line.find("|")
            level.append(line[0: endLine])


def main():
    global entities, screen, camera
    loadLevel()
    pygame.init()
    pygame.mixer.music.load('data/music/main_theme_sped_up.ogg')
    pygame.mixer.music.play()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Super Mario road")
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(Color(BACKGROUND_COLOR))

    left = right = False
    up = False
    running = False

    hero = Player(1, 352)
    entities.add(hero)

    timer = pygame.time.Clock()
    x = y = -32
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            elif col == "b":
                pf = Platform(x, y, "brick")
                entities.add(pf)
                platforms.append(pf)
            elif col == "t":
                pf = Platform(x, y, "tl_pipe")
                entities.add(pf)
                platforms.append(pf)
            elif col == "T":
                pf = Platform(x, y, "tr_pipe")
                entities.add(pf)
                platforms.append(pf)
            elif col == "u":
                pf = Platform(x, y, "bl_pipe")
                entities.add(pf)
                platforms.append(pf)
            elif col == "U":
                pf = Platform(x, y, "br_pipe")
                entities.add(pf)
                platforms.append(pf)
            elif col == "p":
                pf = Platform(x, y, "finish")
                entities.add(pf)
                platforms.append(pf)
            elif col == "s":
                pf = StopBlock(x, y)
                entities.add(pf)
                platforms.append(pf)
            elif col == "*":
                bd = BlockDie(x, y)
                entities.add(bd)
                platforms.append(bd)
            elif col == "w":
                pr = WinBlock(x, y)
                entities.add(pr)
                platforms.append(pr)
                animatedEntities.add(pr)
            elif col == "g":
                mn = Monster(x, y)
                entities.add(mn)
                platforms.append(mn)
                monsters.add(mn)
            x += 32
        y += 32
        x = -32

    total_level_width = len(level[0]) * 32
    total_level_height = len(level) * 32

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while not hero.winner:
        timer.tick(40)
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit("QUIT")
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                running = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_LSHIFT:
                running = False

        screen.blit(bg, (0, 0))

        animatedEntities.update()
        monsters.update(platforms)
        camera.update(hero)
        hero.update(left, right, up, running, platforms)
        check()
        pygame.display.update()
    print("You win!!!")


def check():
    for e in entities:
        screen.blit(e.image, camera.apply(e))


level = []
entities = pygame.sprite.Group()
animatedEntities = pygame.sprite.Group()
monsters = pygame.sprite.Group()
platforms = []
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_Window()
    ex.show()
    sys.exit(app.exec())
