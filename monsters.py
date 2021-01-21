from pygame import *
import pyganim
import os
from blocks import Platform

MONSTER_WIDTH = 32
MONSTER_HEIGHT = 32
MONSTER_COLOR = "#2110FF"
ANIMATION_MONSTERHORYSONTAL = ['data/monsters/gumba1.png',
                               'data/monsters/gumba2.png']


class Monster(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((32, 32))
        self.image.fill(Color(MONSTER_COLOR))
        self.rect = Rect(x, y, 32, 32)
        self.image.set_colorkey(Color(MONSTER_COLOR))
        self.startX = x
        self.startY = y
        self.xvel = 2
        self.yvel = 0
        boltAnim = []
        for anim in ANIMATION_MONSTERHORYSONTAL:
            boltAnim.append((anim, 0.3))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self, platforms):
        self.image.fill(Color(MONSTER_COLOR))
        self.boltAnim.blit(self.image, (0, 0))
        self.rect.x -= self.xvel
        self.collide(platforms)

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:  # если с чем-то или кем-то столкнулись
                self.xvel = - self.xvel
                break
