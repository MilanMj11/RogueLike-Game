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
        self.game.background.fill((118, 59, 54))
        self.game.tilemap = TileMap(100, 100)
        self.game.tilemap.load("Lobby/lobby_map.txt")
        self.game.player.position = [14 * TILESIZE, 15 * TILESIZE]
        self.game.player.speed = 8

    def checkLobbyGameEvents(self, eventList):
        for event in eventList:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if self.game.player.getTile().decorAssetPosition == [0, 5]:
                        self.game.gameStateManager.switchGameState("Dungeon 1")

    def updateLobby(self):
        self.game.updatePlayer()
        self.game.updateCamera()

    def renderLobby(self):
        self.game.virtual_screen.blit(self.game.background, (0, 0))
        self.game.tilemap.render(screen= self.game.virtual_screen,tile_pos = self.game.player.getTileCoords(), offset=self.game.render_camera)
        self.game.player.render(self.game.virtual_screen, offset=self.game.render_camera)
