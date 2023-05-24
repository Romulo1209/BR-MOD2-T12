import random

from dino_runner.utils.constants import SMALL_CACTUS_Y_POS, LARGE_CACTUS_Y_POS
from dino_runner.components.obstacles.obstacle import UnanimateObstacle

class SmallCactus(UnanimateObstacle):
    def __init__(self, images):
        self.type = random.randint(0, 2)
        super().__init__(images, self.type, "cactus")

        self.rect.y = SMALL_CACTUS_Y_POS

class LargeCactus(UnanimateObstacle):
    def __init__(self, images):
        self.type = random.randint(0, 2)
        super().__init__(images, self.type, "cactus")

        self.rect.y = LARGE_CACTUS_Y_POS
