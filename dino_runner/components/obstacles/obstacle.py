from dino_runner.utils.constants import SCREEN_WIDTH

class UnanimateObstacle:
    def __init__(self, images, type, obstacleType):
        self.image = images[type]
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.obstacleType = obstacleType

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed

        if(self.rect.x < -self.rect.width):
            obstacles.pop()

class AnimatedObstacle:
    def __init__(self, images, type, obstacleType):
        self.image = images[type]
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.obstacleType = obstacleType

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, game_speed, obstacles):
        self.animation()
        self.rect.x -= game_speed

        if(self.rect.x < -self.rect.width):
            obstacles.pop()