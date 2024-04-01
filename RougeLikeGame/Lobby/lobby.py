import pygame
from constants import *
from tiles import *
from player import *
from gameStateManager import GameStateManager

class Lobby:
    def __init__(self, game):
        self.game = game
        self.init_Lobby()

    def init_Lobby(self):
        self.game.tilemap = TileMap()
        self.game.tilemap.init_Tilemap_Lobby()
        self.game.player.position = [9 * TILESIZE, 8 * TILESIZE]
        self.game.player.speed = 12

    def checkLobbyGameEvents(self, eventList):
        for event in eventList:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if self.game.player.getTile().row == 8 and self.game.player.getTile().col == 31:
                        self.game.gameStateManager.switchGameState("Dungeon 1")
                        self.game.loadDungeon1()

    def updateLobby(self):
        self.game.updatePlayer()
        self.game.updateCamera()

    def renderLobby(self):
        self.game.virtual_screen.blit(self.game.background, (0, 0))
        self.game.tilemap.render(self.game.virtual_screen, offset=self.game.render_camera)
        self.game.player.render(self.game.virtual_screen, offset=self.game.render_camera)
