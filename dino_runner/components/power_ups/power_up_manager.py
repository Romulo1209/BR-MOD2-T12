import random
import pygame
from pygame import mixer

from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.utils.constants import POWERUP_SPAWN_MAX, POWERUP_SPAWN_MIN, POWERUP_SONG

class PowerUpManager:
    def __init__(self):
        mixer.init()
        mixer.Channel(1).set_volume(0.1)

        self.powerups = []
        self.appears = 0

    def generatePowerup(self, score):
        if len(self.powerups) == 0 and self.appears == score:
            self.appears += random.randint(POWERUP_SPAWN_MIN, POWERUP_SPAWN_MAX)
            self.powerups.append(self.powerupReturn(random.randint(0, 1)))

    def update(self, game):
        self.generatePowerup(game.score)

        for powerup in self.powerups:
            powerup.update(game.game_speed, self.powerups)

            player = game.player
            if player.dinoRect.colliderect(powerup.rect):
                mixer.Channel(2).play(POWERUP_SONG)
                powerup.startTime = pygame.time.get_ticks()
                player.shield = True
                player.hasPowerUp = True
                player.type = powerup.type
                player.powerupTimeUp = powerup.startTime + (powerup.duration * 1000)
                self.powerups.remove(powerup)

    def draw(self, screen):
        for powerup in self.powerups:
            powerup.draw(screen)

    def resetPowerups(self):
        self.powerups.clear()
        self.appears = random.randint(POWERUP_SPAWN_MIN, POWERUP_SPAWN_MAX)

    def powerupReturn(self, typeInt):
        if typeInt == 0:
            return Shield()
        elif typeInt == 1:
            return Hammer()
