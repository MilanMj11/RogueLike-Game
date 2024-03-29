import pygame
from constants import *
from player import Player

class GameController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()

    def startGame(self):
        print("Game Started")

    def update(self):
        self.player.handleInput()
        if self.running == False:
            pygame.quit()
            quit()

        self.clock.tick(60)
        self.checkGameEvents()
        self.render()

    def checkGameEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        self.screen.fill(LIGHT_GRAY)
        self.player.draw(self.screen)

        pygame.display.flip()
        pygame.display.update()