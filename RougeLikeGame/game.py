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
        self.player = Player()
        self.camera = [0, 0]
        self.render_camera = [0, 0]
        self.background = pygame.transform.scale(pygame.image.load("assets/background.jpg").convert_alpha(), (1920, 1080))
        self.tilemap = None

    def startGame(self):
        self.tilemap = TileMap(20, 20)
        self.tilemap.initTiles()

    def update(self):
        self.player.handleInput()
        if self.running == False:
            pygame.quit()
            quit()

        self.camera[0] += (self.player.rect.centerx - self.screen.get_width() / 2 - self.camera[0]) / 20
        self.camera[1] += (self.player.rect.centery - self.screen.get_height() / 2 - self.camera[1]) / 20
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
        self.tilemap.render(self.screen, offset = self.render_camera)
        self.player.render(self.screen, offset = self.render_camera)

        pygame.display.flip()
        pygame.display.update()