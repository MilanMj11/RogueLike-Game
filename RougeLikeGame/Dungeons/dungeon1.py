import pygame
from constants import *
from tiles import *
from player import *
from gameStateManager import GameStateManager
from Enemies.skeletonFighter import SkeletonFighter


class Dungeon1:
    def __init__(self, game):
        self.game = game
        self.init_Dungeon_1()
        self.game.enemiesList = []
        self.game.lastSkeletonFighterSpawn = 0
        self.skeletonSpawnLocations = [[(3, 23), (2, 23), (2, 24), (3, 24)]]

    def init_Dungeon_1(self):
        self.game.background.fill((118, 59, 54))
        self.game.tilemap = TileMap(100, 100)
        self.game.tilemap.load("Dungeons/dungeon1_map.txt")

        self.game.player.position = [4 * TILESIZE, 4 * TILESIZE]

        self.game.player.loadPlayer()

        self.game.player.speed = 3

    def checkDungeon1GameEvents(self, eventList):
        self.game.player.handleEvents(eventList)
        for event in eventList:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.gameStateManager.switchGameState("Menu", "Pause Menu")

    def spawnSkeletonFighter(self):

        current_time = self.game.current_time

        if current_time - self.game.lastSkeletonFighterSpawn > 5000:
            self.game.lastSkeletonFighterSpawn = current_time
            self.game.enemiesList.append(SkeletonFighter(self.game, [5 * TILESIZE, 5 * TILESIZE]))

    def updateDungeon1(self):

        self.game.updateCamera()
        self.game.updatePlayer()

        self.game.updateProjectiles()
        self.game.xpHUD.updateXPHUD()
        self.game.healthHUD.updateHealthHUD()

        # check if player died
        if self.game.player.health <= 0:
            self.game.gameStateManager.switchGameState("Lobby")
            self.game.loadLobby()
            return

        for enemy in self.game.enemiesList:
            if enemy.health <= 0:
                self.game.enemiesList.remove(enemy)
                continue
            enemy.update()

        # spawn enemies ( up to 5 )
        if self.game.enemiesList.__len__() < 5:
            self.spawnSkeletonFighter()

    def renderDungeon1(self):
        self.game.virtual_screen.blit(self.game.background, (0, 0))
        self.game.tilemap.render(screen= self.game.virtual_screen, tile_pos=self.game.player.getTileCoords() , offset=self.game.render_camera)
        self.game.player.render(self.game.virtual_screen, offset=self.game.render_camera)
        for projectile in self.game.projectiles:
            projectile.render(self.game.virtual_screen, offset=self.game.render_camera)

        for enemy in self.game.enemiesList:
            enemy.render(self.game.virtual_screen, offset=self.game.render_camera)

        self.game.abilitiesHud.renderAbilitiesHud(self.game.virtual_screen)
