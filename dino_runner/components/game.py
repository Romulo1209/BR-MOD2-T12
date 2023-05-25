import pygame
from pygame import mixer

from dino_runner.utils.constants import BG, CLOUD, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE, DEFAULT_TYPE, CYCLE_SCORE, CYCLE_COLORS, MUSIC_SONG
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.components.cycleManager import CycleManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)

        mixer.init()
        mixer.Channel(0).set_volume(0.05)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.executing = False
        self.game_speed = 20

        self.x_pos_cloud = 1200
        self.y_pos_cloud = 150
        self.x_pos_bg = 0
        self.y_pos_bg = 380

        self.powerupManager = PowerUpManager()
        self.obstacleManager = ObstacleManager()
        self.cycleManager = CycleManager()
        self.deathCount = 0
        self.score = 0
        self.bestScore = 0

        self.textColorR = CYCLE_COLORS[self.cycleManager.cycle][0]
        self.textColorG = CYCLE_COLORS[self.cycleManager.cycle][1]
        self.textColorB = CYCLE_COLORS[self.cycleManager.cycle][2]

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.resetGame()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def execute(self):
        self.executing = True
        mixer.Channel(0).play(MUSIC_SONG)
        while self.executing:
            if not self.playing:
                self.showMenu()
        pygame.display.quit()
        pygame.quit()
    
    def resetGame(self):
        self.player = Dinosaur()
        self.obstacleManager.resetObstacles()
        self.powerupManager.resetPowerups()
        self.game_speed = 20
        self.score = 0

        if self.cycleManager.day == False:
            self.cycleManager.changeCycle()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.executing = False

    def update(self):
        userInput = pygame.key.get_pressed()
        self.player.update(userInput)
        self.obstacleManager.update(self)
        self.powerupManager.update(self)
        self.updateScore()
        self.updateFontColors()

    def updateFontColors(self):
        self.textColorR = CYCLE_COLORS[self.cycleManager.cycle][0]
        self.textColorG = CYCLE_COLORS[self.cycleManager.cycle][1]
        self.textColorB = CYCLE_COLORS[self.cycleManager.cycle][2]

    def updateScore(self):
        self.score += 1
        if self.bestScore < self.score:
            self.bestScore = self.score
            
        if(self.score % CYCLE_SCORE == 0):
            self.cycleManager.changeCycle()

        if self.score % 100 == 0:
            self.game_speed += 0.5

    def draw(self):
        self.clock.tick(FPS)
        self.cycleManager.draw(self.screen)
        self.drawParalax()
        self.player.draw(self.screen)
        self.obstacleManager.draw(self.screen)
        self.drawScore()
        self.drawPowerupTime()
        self.powerupManager.draw(self.screen)
        pygame.display.flip()

    def drawScore(self):
        font = pygame.font.Font(FONT_STYLE, 22)
        scoreText = font.render(f"Score: {self.score}", True, (self.textColorR, self.textColorG, self.textColorB))
        scoreTextRect = scoreText.get_rect()
        scoreTextRect.center = (970, 50)
        self.screen.blit(scoreText, scoreTextRect)

    def drawParalax(self):
        backgroundWidth = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (backgroundWidth + self.x_pos_bg, self.y_pos_bg))

        self.screen.blit(CLOUD, (self.x_pos_cloud, self.y_pos_cloud))
        self.screen.blit(CLOUD, (self.x_pos_cloud + SCREEN_WIDTH * 2, self.y_pos_cloud + 70))

        if self.x_pos_bg <= -backgroundWidth:
            self.screen.blit(BG, (backgroundWidth + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        
        if self.x_pos_cloud <= -backgroundWidth:
            self.x_pos_cloud = 1200
        
        self.x_pos_cloud -= self.game_speed / 4
        self.x_pos_bg -= self.game_speed

    def drawPowerupTime(self):
        if self.player.hasPowerUp:
            timeToShow = round((self.player.powerupTimeUp - pygame.time.get_ticks())/1000, 2)
            if timeToShow >= 0:
                font = pygame.font.Font(FONT_STYLE, 22)
                text = font.render(f"Active Power Up: {timeToShow}s", True, (self.textColorR, self.textColorG, self.textColorB))
                text_rect = text.get_rect()
                text_rect.x = 425
                text_rect.y = 50
                self.screen.blit(text, text_rect)
            else:
                self.player.hasPowerUp = False
                self.player.type = DEFAULT_TYPE

    def showMenu(self):
        self.screen.fill((255,255,255))
        halfScreenHeight = SCREEN_HEIGHT / 2
        halfScreenWidth = SCREEN_WIDTH / 2

        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render("Press UP button to start game", True, (0,0,0))
        bestScore = font.render(f"Best score: {self.bestScore}", True, (0,0,0))
        text_Rect = text.get_rect()
        text_Rect.center = (halfScreenWidth, halfScreenHeight)
        bestText_Rect = bestScore.get_rect()
        bestText_Rect.center = (halfScreenWidth,  + 50)

        self.screen.blit(text, text_Rect)
        self.screen.blit(bestScore, bestText_Rect)

        pygame.display.update()

        self.HandleEventsOnMenu()
        self.drawParalax()

    def HandleEventsOnMenu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.executing = False
            elif event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_UP] and self.deathCount == 0:
                    self.run()
                elif pygame.key.get_pressed()[pygame.K_UP]:
                    self.run()