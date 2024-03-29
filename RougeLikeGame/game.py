import pygame
from constants import *
from player import Player
from tiles import *


class GameController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()
        self.running = True
        self.camera = [0, 0]
        self.render_camera = [0, 0]
        self.background = pygame.transform.scale(pygame.image.load("assets/background.jpg").convert_alpha(),
                                                 (1920, 1080))
        self.tilemap = None
        self.player = Player(self, (470, 470))

    def startGame(self):
        self.tilemap = TileMap(20, 20)
        self.tilemap.initTiles()

    def update(self):
        if self.running == False:
            pygame.quit()
            quit()

        # self.player.handleInput()
        self.player.update()

        self.camera[0] += (self.player.position[0] - self.camera[0] - 960) / 10
        self.camera[1] += (self.player.position[1] - self.camera[1] - 540) / 10

        self.render_camera = [int(self.camera[0]), int(self.camera[1])]

        self.clock.tick(60)
        self.checkGameEvents()
        self.render()

    def checkGameEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.tilemap.render(self.screen, offset=self.render_camera)
        self.player.render(self.screen, offset=self.render_camera)

        pygame.display.flip()
        pygame.display.update()
