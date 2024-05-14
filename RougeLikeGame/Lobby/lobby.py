import pygame
from constants import *
from tiles import *
from player import *
from gameStateManager import GameStateManager


class Lobby:
    def __init__(self, game):
        self.game = game
        self.decoratorImage = pygame.image.load("assets/huds/lobbyDecorators.png").convert_alpha()
        # Gamba Room
        self.decoratorGamba = self.decoratorImage.subsurface((16, 16, 19 * 16, 8 * 16))
        self.decoratorGamba = pygame.transform.scale(self.decoratorGamba, (19 * TILESIZE, 8 * TILESIZE))
        self.decoratorGamba2 = self.decoratorImage.subsurface((0, 0, 19 * 16, 1 * 16))
        self.decoratorGamba2 = pygame.transform.scale(self.decoratorGamba2, (19 * TILESIZE, 1 * TILESIZE))

        # Personal Room
        self.decoratorPersonalRoom = self.decoratorImage.subsurface((16, 208, 11 * 16, 5 * 16))
        self.decoratorPersonalRoom = pygame.transform.scale(self.decoratorPersonalRoom, (11 * TILESIZE, 5 * TILESIZE))

        # Abilities Room
        self.decoratorAbilitiesRoom = self.decoratorImage.subsurface((16, 544, 18 * 16, 8 * 16))
        self.decoratorAbilitiesRoom = pygame.transform.scale(self.decoratorAbilitiesRoom, (18 * TILESIZE, 8 * TILESIZE))
        self.decoratorAbilitiesRoom2 = self.decoratorImage.subsurface((0, 527, 18 * 16, 1 * 16))
        self.decoratorAbilitiesRoom2 = pygame.transform.scale(self.decoratorAbilitiesRoom2, (18 * TILESIZE, 1 * TILESIZE))

        # Smith Room
        self.decoratorSmithRoom = self.decoratorImage.subsurface((16, 368, 17 * 16, 7 * 16))
        self.decoratorSmithRoom = pygame.transform.scale(self.decoratorSmithRoom, (17 * TILESIZE, 7 * TILESIZE))

        # Dungeon Entrance Room
        self.decoratorDungeonEntrance = self.decoratorImage.subsurface((16, 720, 17 * 16, 17 * 16))
        self.decoratorDungeonEntrance = pygame.transform.scale(self.decoratorDungeonEntrance, (17 * TILESIZE, 17 * TILESIZE))

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

    def renderDecorators(self):
        # Gamba Room
        self.game.virtual_screen.blit(self.decoratorGamba, (
        2 * TILESIZE - self.game.render_camera[0], 21 * TILESIZE - self.game.render_camera[1]))
        self.game.virtual_screen.blit(self.decoratorGamba2, (
        1 * TILESIZE - self.game.render_camera[0], 20 * TILESIZE - self.game.render_camera[1]))
        # ----------------------------------------------------------------------------------------
        # Personal Room
        self.game.virtual_screen.blit(self.decoratorPersonalRoom, (
        9 * TILESIZE - self.game.render_camera[0], 4 * TILESIZE - self.game.render_camera[1]))
        # ----------------------------------------------------------------------------------------
        # Abilities Room
        self.game.virtual_screen.blit(self.decoratorAbilitiesRoom, (
        25 * TILESIZE - self.game.render_camera[0], 21 * TILESIZE - self.game.render_camera[1]))
        self.game.virtual_screen.blit(self.decoratorAbilitiesRoom2, (
        24 * TILESIZE - self.game.render_camera[0], 20 * TILESIZE - self.game.render_camera[1]))
        # ----------------------------------------------------------------------------------------
        # Smith Room
        self.game.virtual_screen.blit(self.decoratorSmithRoom, (
        26 * TILESIZE - self.game.render_camera[0], 3 * TILESIZE - self.game.render_camera[1]))
        # ----------------------------------------------------------------------------------------
        # Dungeon Entrance Room
        self.game.virtual_screen.blit(self.decoratorDungeonEntrance, (
        47 * TILESIZE - self.game.render_camera[0], 7 * TILESIZE - self.game.render_camera[1]))



    def renderLobby(self):
        self.game.virtual_screen.blit(self.game.background, (0, 0))
        self.game.tilemap.render(screen=self.game.virtual_screen, tile_pos=self.game.player.getTileCoords(),
                                 offset=self.game.render_camera)
        # blit the decorators on the map
        self.renderDecorators()
        self.game.player.render(self.game.virtual_screen, offset=self.game.render_camera)
