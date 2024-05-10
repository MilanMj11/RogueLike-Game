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
        self.game.background.fill((73, 71, 81))
        self.game.tilemap = TileMap(75, 35)
        self.game.tilemap.load("Lobby/lobby_map.txt", "lobby")
        # self.game.player.loadPlayer()

        self.game.player.position = [14 * TILESIZE, 15 * TILESIZE]
        self.game.player.speed = 8

    def checkLobbyGameEvents(self, eventList):
        for event in eventList:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if self.game.player.getTile().decorAssetPosition == [0, 5]:
                        # For testing I switch to Dungeon 1 -> I need to change to the correct Dungeon and Region
                        map = "Dungeon " + str(self.game.currentDungeon)
                        self.game.gameStateManager.switchGameState(map)
                if event.key == pygame.K_ESCAPE:
                    self.game.gameStateManager.switchGameState("Menu", "Pause Menu Lobby")

    def updateLobby(self):
        self.game.updatePlayer()
        self.game.updateCamera()

    def renderLobby(self):
        self.game.virtual_screen.blit(self.game.background, (0, 0))
        self.game.tilemap.render(screen= self.game.virtual_screen,tile_pos = self.game.player.getTileCoords(), offset=self.game.render_camera)
        self.game.player.render(self.game.virtual_screen, offset=self.game.render_camera)
