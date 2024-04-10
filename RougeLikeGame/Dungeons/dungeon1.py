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

    def init_Dungeon_1(self):
        self.game.tilemap = TileMap(100,100)
        self.game.tilemap.load("Dungeons/dungeon1_map.txt")
        # self.game.tilemap.init_Tilemap_Dungeon_1()
        self.game.player.position = [4 * TILESIZE, 4 * TILESIZE]
        self.game.player.speed = 1.2

    def checkDungeon1GameEvents(self, eventList):
        for event in eventList:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if self.game.player.getTile().row == 1 and self.game.player.getTile().col == 1:
                        self.game.gameStateManager.switchGameState("Lobby")
                        self.game.loadLobby()

    def spawnSkeletonFighter(self):

        current_time = pygame.time.get_ticks()

        if current_time - self.game.lastSkeletonFighterSpawn > 5000:
            self.game.lastSkeletonFighterSpawn = current_time
            self.game.enemiesList.append(SkeletonFighter(self.game, [7 * TILESIZE, 7 * TILESIZE]))

    def updateDungeon1(self):

        self.game.updateCamera()
        self.game.updatePlayer()

        self.game.updateProjectiles()

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
            pass
            # self.spawnSkeletonFighter()


    def renderDungeon1(self):
        self.game.virtual_screen.blit(self.game.background, (0, 0))
        self.game.tilemap.render(self.game.virtual_screen, offset=self.game.render_camera)
        self.game.player.render(self.game.virtual_screen, offset=self.game.render_camera)
        for projectile in self.game.projectiles:
            projectile.render(self.game.virtual_screen, offset=self.game.render_camera)

        for enemy in self.game.enemiesList:
            enemy.render(self.game.virtual_screen, offset=self.game.render_camera)
