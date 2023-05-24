import random

from dino_runner.utils.constants import SCREEN_WIDTH

class PowerUp:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.rect.y = random.randint(125, 175)

        self.startTime = 0
        self.duration = random.randint(4, 8)

    def update(self, gameSpeed, powerups):
        self.rect.x -= gameSpeed

        if self.rect.x < -self.rect.width:
            powerups.pop()

    def draw(self, screen):
        screen.blit(self.image, self.rect)