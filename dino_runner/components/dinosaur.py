import pygame

from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING, DEFAULT_TYPE, SHIELD_TYPE, HAMMER_TYPE, DUCKING_SHIELD, JUMPING_SHIELD, RUNNING_SHIELD, DUCKING_HAMMER, JUMPING_HAMMER, RUNNING_HAMMER, JUMP_SONG
from pygame import mixer

xPos = 80
yPos = 310
yDuckPos = 345
jumpVelocity = 8.5

DUCK_IMAGE = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE: DUCKING_HAMMER}
JUMP_IMAGE = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER}
RUN_IMAGE = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER}


class Dinosaur:
    def __init__(self):
        mixer.init()
        mixer.Channel(1).set_volume(0.3)

        self.type = DEFAULT_TYPE
        self.image = RUN_IMAGE[self.type][0]
        self.dinoRect = self.image.get_rect()
        self.dinoRect.x = xPos
        self.dinoRect.y = yPos

        self.running = True
        self.ducking = False
        self.jumping = False
        self.jumpped = False
        self.stepIndex = 0
        self.jumpVelocity = jumpVelocity
        self.hasPowerUp = False

    def run(self):
        self.image = RUN_IMAGE[self.type][self.stepIndex // 5]
        self.stepIndex += 1
        self.SetPosition(xPos, yPos)

        if self.stepIndex >= 10:
            self.stepIndex = 0

    def duck(self):
        self.image = DUCK_IMAGE[self.type][self.stepIndex // 5]
        self.SetPosition(xPos, yDuckPos)
        self.stepIndex += 1

        if self.stepIndex >= 10:
            self.stepIndex = 0
    
    def jump(self):
        self.image = JUMP_IMAGE[self.type]
        if self.jumpped == False:
            mixer.Channel(1).play(JUMP_SONG)

        if self.jumping:
            self.dinoRect.y -= self.jumpVelocity * 4
            self.jumpVelocity -= 0.8
            self.jumpped = True

        if self.jumpVelocity < -jumpVelocity:
            self.jumping = False
            self.jumpped = False
            self.dinoRect.y = yPos
            self.jumpVelocity = jumpVelocity

    def SetPosition(self, xActualPos, yActualPos):
        self.dinoRect = self.image.get_rect()
        self.dinoRect.x = xActualPos
        self.dinoRect.y = yActualPos

    def update(self, userInput):
        if userInput[pygame.K_UP] and not self.jumping:
            self.jumping = True
            self.running = False
            self.ducking = False
        elif userInput[pygame.K_DOWN] and not self.jumping:
            self.ducking = True
        elif not self.jumping:
            self.running = True
            self.ducking = False

        if self.ducking:
            self.duck()
        elif self.running:
            self.run()
        elif self.jumping:
            self.jump()

    def draw(self, screen):
        screen.blit(self.image, (self.dinoRect.x, self.dinoRect.y))