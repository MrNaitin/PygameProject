from pygame import *
import pygame
import pyganim
import blocks
import monsters

speed = 7
run_speed = 1.5
jump = 9
run_jump = 1
gravitation = 0.35
anim_delay = 0.2
run_anim_delay = 0.1

ANIMATION_RIGHT = ['data/mario/right1.png',
                   'data/mario/right2.png',
                   'data/mario/right3.png']
ANIMATION_LEFT = ['data/mario/left1.png',
                  'data/mario/left2.png',
                  'data/mario/left3.png']
ANIMATION_JUMP_LEFT = [('data/mario/jumpl.png', 0.1)]
ANIMATION_JUMP_RIGHT = [('data/mario/jumpr.png', 0.1)]
ANIMATION_STAY_RIGHT = [('data/mario/standr.png', 0.1)]
ANIMATION_STAY_LEFT = [('data/mario/standl.png', 0.1)]
ANIMATION_DIE = [('data/mario/death.png', 0.1)]


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.yvel = 0
        self.onGround = False
        self.diriction = "right"
        self.checker = False
        self.image = Surface((32, 32))
        self.image.fill(Color("#888888"))
        self.rect = Rect(x, y, 32, 32)
        self.image.set_colorkey(Color("#888888"))
        self.death_sound = pygame.mixer.Sound("data/music/death.wav")
        self.win_sound = pygame.mixer.Sound("data/music/stage_clear.wav")
        self.jump_sound = pygame.mixer.Sound("data/music/jump.ogg")
        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, anim_delay))
            boltAnimSuperSpeed.append((anim, run_anim_delay))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        self.boltAnimRightSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimRightSuperSpeed.play()
        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, anim_delay))
            boltAnimSuperSpeed.append((anim, run_anim_delay))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        self.boltAnimLeftSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimLeftSuperSpeed.play()

        self.boltAnimStay_left = pyganim.PygAnimation(ANIMATION_STAY_LEFT)
        self.boltAnimStay_left.play()
        self.boltAnimStay_right = pyganim.PygAnimation(ANIMATION_STAY_RIGHT)
        self.boltAnimStay_right.play()
        self.boltAnimStay_right.blit(self.image, (0, 0))

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()
        self.boltAnimDie = pyganim.PygAnimation(ANIMATION_DIE)
        self.boltAnimDie.play()
        self.winner = False

    def update(self, left, right, up, running, platforms):
        if up:
            if self.onGround:
                self.yvel = -jump
                if running and (left or right):
                    self.yvel -= run_jump
                self.image.fill(Color("#888888"))
                if self.diriction == "right" and self.checker is False:
                    self.boltAnimJumpRight.blit(self.image, (0, 0))
                    self.jump_sound.play()
                    self.checker = True
                elif self.diriction == "left" and self.checker is False:
                    self.boltAnimJumpLeft.blit(self.image, (0, 0))
                    self.jump_sound.play()
                    self.checker = True
        if left:
            self.xvel = -speed
            self.image.fill(Color("#888888"))
            self.diriction = "left"
            if running:
                self.xvel -= run_speed
                if not up:
                    if self.checker is False:
                        self.boltAnimLeftSuperSpeed.blit(self.image, (0, 0))
                    else:
                        self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                if not up:
                    if self.checker is False:
                        self.boltAnimLeft.blit(self.image, (0, 0))
                    else:
                        self.boltAnimJumpLeft.blit(self.image, (0, 0))
            if up:
                self.boltAnimJumpLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = speed
            self.image.fill(Color("#888888"))
            self.diriction = "right"
            if running:
                self.xvel += run_speed
                if not up:
                    if self.checker is False:
                        self.boltAnimRightSuperSpeed.blit(self.image, (0, 0))
                    else:
                        self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                if not up:
                    if self.checker is False:
                        self.boltAnimRight.blit(self.image, (0, 0))
                    else:
                        self.boltAnimJumpRight.blit(self.image, (0, 0))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))

        if not (left or right):
            self.xvel = 0
            if not up:
                self.image.fill(Color("#888888"))
                if self.checker is False:
                    if self.diriction == "right":
                        self.boltAnimStay_right.blit(self.image, (0, 0))
                    elif self.diriction == "left":
                        self.boltAnimStay_left.blit(self.image, (0, 0))
                else:
                    if self.diriction == "right":
                        self.boltAnimJumpRight.blit(self.image, (0, 0))
                    elif self.diriction == "left":
                        self.boltAnimJumpLeft.blit(self.image, (0, 0))
        if not self.onGround:
            self.yvel += gravitation

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and type(p) != blocks.StopBlock:
                if isinstance(p, blocks.BlockDie) or isinstance(p, monsters.Monster):
                    self.image.fill(Color("#888888"))
                    self.boltAnimDie.blit(self.image, (0, 0))
                    self.die()
                    break
                elif isinstance(p, blocks.WinBlock):
                    pygame.mixer.music.stop()
                    self.win_sound.play()
                    time.wait(5000)
                    self.winner = True
                    break
                else:
                    if xvel > 0:
                        self.rect.right = p.rect.left
                    elif xvel < 0:
                        self.rect.left = p.rect.right
                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        self.checker = False
                        self.yvel = 0
                    elif yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = 0

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY

    def die(self):
        pygame.mixer.music.stop()
        self.death_sound.play()
        time.wait(3000)
        self.diriction = "right"
        self.teleporting(self.startX, self.startY)
        pygame.mixer.music.play()
