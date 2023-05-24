import pygame

from dino_runner.utils.constants import CYCLE_VELOCITY

class CycleManager:
    def __init__(self):
        self.day = True
        self.cycle = "day"
        self.r = 255
        self.g = 255
        self.b = 255

    def draw(self, screen):
        if self.r > 255 or self.g > 255 or self.b > 255:
            self.r = 255
            self.g = 255
            self.b = 255
        elif self.r < 0 or self.g < 0 or self.b < 0:
            self.r = 0
            self.g = 0
            self.b = 0

        screen.fill((self.r, self.g, self.b))
        if self.day == True and self.r != 255 and self.g != 255 and self.b != 255:
            self.r += CYCLE_VELOCITY
            self.g += CYCLE_VELOCITY
            self.b += CYCLE_VELOCITY
        elif self.day == False and self.r != 0 and self.g != 0 and self.b != 0:
            self.r -= CYCLE_VELOCITY
            self.g -= CYCLE_VELOCITY
            self.b -= CYCLE_VELOCITY

    def changeCycle(self):
        if self.day == True:
            self.day = False
            self.cycle = "night"
        elif self.day == False: 
            self.day = True
            self.cycle = "day"