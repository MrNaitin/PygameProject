from pygame import *
import os
import pyganim

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#000000"

 
class Platform(sprite.Sprite):
    def __init__(self, x, y, type="platform"):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        if type == "platform":
            self.image = image.load("data/blocks/platform.png")
        elif type == "brick":
            self.image = image.load("data/blocks/brick.png")
        elif type == "tl_pipe":
            self.image = image.load("data/blocks/tl_pipe.png")
        elif type == "tr_pipe":
            self.image = image.load("data/blocks/tr_pipe.png")
        elif type == "bl_pipe":
            self.image = image.load("data/blocks/bl_pipe.png")
        elif type == "br_pipe":
            self.image = image.load("data/blocks/br_pipe.png")
        elif type == "finish":
            self.image = image.load("data/blocks/finish.png")

        self.image.set_colorkey(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class StopBlock(Platform):
    def __init__(self, x, y,):
        Platform.__init__(self, x, y)
        self.image = image.load("data/blocks/stop.png")


class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("data/blocks/spike.png")

        
class WinBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("data/blocks/stop.png")
        
    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
