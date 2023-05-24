from dino_runner.components.obstacles.obstacle import AnimatedObstacle
from dino_runner.utils.constants import BIRD, BIRD_Y_POS

class Bird(AnimatedObstacle):
    def __init__(self):
        self.stepIndex = 0
        super().__init__(BIRD, 0, "bird")
        self.rect.y = BIRD_Y_POS

    def animation(self):
        self.image = BIRD[0] if self.stepIndex < 5 else BIRD[1]
        self.stepIndex += 1

        if self.stepIndex >= 10:
            self.stepIndex = 0