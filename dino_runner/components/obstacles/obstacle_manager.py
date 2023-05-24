import pygame
import random
from pygame import mixer

from dino_runner.components.obstacles.cactus import SmallCactus, LargeCactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, POWERUP_DESTROY, DEATH_SONG

class ObstacleManager:
    def __init__(self):
        mixer.init()
        mixer.Channel(1).set_volume(0.3)

        self.obstacles = []
    
    def update(self, game):
        if len(self.obstacles) == 0:
            self.obstacles.append(self.obstacleReturn(random.randint(0, 2)))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)

            if game.player.dinoRect.colliderect(obstacle.rect):
                if not game.player.hasPowerUp:
                    self.killPlayer(game)
                    break
                else:
                    if self.powerupCheckImmunity(game.player.type, obstacle.obstacleType) == True:
                        self.obstacles.remove(obstacle)
                    else:
                        self.killPlayer(game)
    
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def resetObstacles(self):
        self.obstacles.clear()

    def killPlayer(self, game):
        pygame.time.delay(500)
        mixer.Channel(2).play(DEATH_SONG)
        game.playing = False
        game.deathCount += 1

    def powerupCheckImmunity(self, powerupType, obstacleType):
        if obstacleType in POWERUP_DESTROY[powerupType]:
            return True
        else:
            return False

    def obstacleReturn(self, typeInt):
        if typeInt == 0:
            return SmallCactus(SMALL_CACTUS)
        elif typeInt == 1:
            return LargeCactus(LARGE_CACTUS)
        elif typeInt == 2:
            return Bird()
