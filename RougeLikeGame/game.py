import pygame
from constants import *
from player import Player
from tiles import *
from gameStateManager import GameStateManager


class GameController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.gameStateManager = GameStateManager("Dungeon 1")
        self.running = True
        self.camera = [0, 0]
        self.render_camera = [0, 0]
        self.background = pygame.transform.scale(pygame.image.load("assets/background.jpg").convert_alpha(),
                                                 (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.tilemap = None
        self.player = Player(self, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.projectiles = []

    def startGame(self):
        # start the game, initially is just a simple tilemap for testing
        self.tilemap = TileMap(20, 20)
        self.tilemap.initTiles()

    def updatePlayer(self):
        # update the player
        self.player.update()

    def updateProjectiles(self):
        # update each projectile present in the game
        for projectile in self.projectiles:
            projectile.update()

    def updateCamera(self):
        # camera follows the player with a smooth effect , MIGHT CHANGE VALUES LATER
        self.camera[0] += (self.player.position[0] - self.camera[0] - 960) / 10
        self.camera[1] += (self.player.position[1] - self.camera[1] - 540) / 10
        self.render_camera = [int(self.camera[0]), int(self.camera[1])]

    def updateDungeon1(self):
        # update everything needed for the dungeon 1
        self.updatePlayer()
        self.updateProjectiles()
        self.updateCamera()


    def update(self):
        if self.running == False:
            pygame.quit()
            quit()

        if self.gameStateManager.gameState == "Dungeon 1":
            self.updateDungeon1()

        self.clock.tick(60)
        self.checkGameEvents()
        self.render()

    def checkGameEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def renderDungeon1(self):
        # render everything needed for the dungeon 1
        self.screen.blit(self.background, (0, 0))
        self.tilemap.render(self.screen, offset=self.render_camera)
        self.player.render(self.screen, offset=self.render_camera)
        for projectile in self.projectiles:
            projectile.render(self.screen, offset=self.render_camera)

    def render(self):

        if self.gameStateManager.gameState == "Dungeon 1":
            self.renderDungeon1()

        pygame.display.flip()
        pygame.display.update()
