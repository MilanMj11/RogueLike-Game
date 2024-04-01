import pygame
from constants import *
from player import Player
from tiles import *
from gameStateManager import GameStateManager
from lobby import Lobby

class GameController:
    def __init__(self):
        pygame.init()
        self.virtual_screen = pygame.Surface((VIRTUALSCREEN_WIDTH, VIRTUALSCREEN_HEIGHT))
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.gameStateManager = GameStateManager("Lobby")
        self.running = True
        self.camera = [0, 0]
        self.render_camera = [0, 0]
        self.background = pygame.Surface((VIRTUALSCREEN_WIDTH, VIRTUALSCREEN_HEIGHT))
        self.background.fill((0, 0, 0))
        self.tilemap = None
        self.player = Player(self, (9 * TILESIZE, 8 * TILESIZE))
        self.projectiles = []
        self.Lobby = Lobby(self)

    def startGame(self):
        # start the game, initially is just a simple tilemap for testing
        # self.tilemap = TileMap()
        # self.tilemap.init_Lobby()
        # self.player.speed = 10
        self.Lobby.init_Lobby()

    def loadDungeon1(self):
        self.tilemap = TileMap()
        self.tilemap.init_Tilemap_Dungeon_1()
        self.player.position = [5 * TILESIZE, 5 * TILESIZE]
        self.player.speed = 5

    def updatePlayer(self):
        # update the player
        self.player.update()

    def updateProjectiles(self):
        # update each projectile present in the game
        for projectile in self.projectiles:
            projectile.update()

    def updateCamera(self):
        # camera follows the player with a smooth effect , MIGHT CHANGE VALUES LATER
        self.camera[0] += (self.player.position[0] - self.camera[0] - VIRTUALSCREEN_WIDTH / 2 + self.player.size[0] / 2) / 10
        self.camera[1] += (self.player.position[1] - self.camera[1] - VIRTUALSCREEN_HEIGHT / 2 + self.player.size[1] / 2) / 10
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

        if self.gameStateManager.gameState == "Lobby":
            self.Lobby.updateLobby()

        self.clock.tick(60)
        self.checkGameEvents()
        self.render()

    def checkGameEvents(self):

        eventList = pygame.event.get()

        if self.gameStateManager.gameState == "Lobby":
            self.Lobby.checkLobbyGameEvents(eventList)

        for event in eventList:
            if event.type == pygame.QUIT:
                self.running = False


    def renderDungeon1(self):
        # render everything needed for the dungeon 1
        self.virtual_screen.blit(self.background, (0, 0))
        self.tilemap.render(self.virtual_screen, offset=self.render_camera)
        self.player.render(self.virtual_screen, offset=self.render_camera)
        for projectile in self.projectiles:
            projectile.render(self.virtual_screen, offset=self.render_camera)

    def render(self):

        # --- Rendering the correct Scene based on the gameState ---

        if self.gameStateManager.gameState == "Dungeon 1":
            self.renderDungeon1()

        if self.gameStateManager.gameState == "Lobby":
            self.Lobby.renderLobby()

        # --- Rendering the correct Scene based on the gameState ---

        # scale the virutal screen onto the actual screen
        scaledScreen = pygame.transform.scale(self.virtual_screen, (SCREEN_WIDTH, SCREEN_HEIGHT), self.screen)
        self.screen.blit(scaledScreen, (0, 0))

        pygame.display.flip()
        pygame.display.update()
