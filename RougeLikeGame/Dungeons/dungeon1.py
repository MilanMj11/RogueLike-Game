import pygame
from constants import *
from tiles import *
from player import *
from gameStateManager import GameStateManager


class Dungeon1:
    def __init__(self, game):
        self.game = game
        self.init_Dungeon_1()

    def init_Dungeon_1(self):
        self.game.tilemap = TileMap()
        self.game.tilemap.init_Tilemap_Dungeon_1()
        self.game.player.position = [5 * TILESIZE, 5 * TILESIZE]
        self.game.player.speed = 6

    def checkDungeon1GameEvents(self, eventList):
        for event in eventList:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if self.game.player.getTile().row == 1 and self.game.player.getTile().col == 1:
                        self.game.gameStateManager.switchGameState("Lobby")
                        self.game.loadLobby()

    def updateDungeon1(self):
        self.game.updatePlayer()
        self.game.updateProjectiles()
        self.game.updateCamera()

    def renderDungeon1(self):
        self.game.virtual_screen.blit(self.game.background, (0, 0))
        self.game.tilemap.render(self.game.virtual_screen, offset=self.game.render_camera)
        self.game.player.render(self.game.virtual_screen, offset=self.game.render_camera)
        for projectile in self.game.projectiles:
            projectile.render(self.game.virtual_screen, offset=self.game.render_camera)
