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
        self.lastSkeletonFighterSpawn = [0 for _ in range(10)] # Let's say I have maximum 10 spawners
        # lastSkeletonFighterSpawn[spawnerNr] = last time a skeleton was spawned by the spawner Nr

        self.spawners = [[] for _ in range(10)] # List of Lists of Enemies
        self.spawnerTotalSpawns = [0 for _ in range(10)] # Total number of spawns by the spawner Nr

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

    def spawnSkeletonFighters(self, spawnerNr, x, y, size=4, totalSpawns = 10):
        # This function acts like a Spawner, that constantly spawns enemies
        if self.spawners[spawnerNr].__len__() >= size:
            return

        if self.spawnerTotalSpawns[spawnerNr] >= totalSpawns:
            return

        current_time = self.game.current_time

        if current_time - self.lastSkeletonFighterSpawn[spawnerNr] > 5000:
            self.lastSkeletonFighterSpawn[spawnerNr] = current_time
            self.spawners[spawnerNr].append(SkeletonFighter(self.game, [x * TILESIZE, y * TILESIZE]))
            self.spawnerTotalSpawns[spawnerNr] += 1
            self.game.enemiesList.append(self.spawners[spawnerNr][-1])

    def eliminateSkeletonFighters(self, spawnerNr):
        for skeleton in self.spawners[spawnerNr]:
            if skeleton not in self.game.enemiesList:
                self.spawners[spawnerNr].remove(skeleton)
    def spawnSkeletonFighter(self, x, y):
        # This function acts like a one time Spawner.
        self.game.enemiesList.append(SkeletonFighter(self.game, [x * TILESIZE, y * TILESIZE]))

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



        # Spawner Zone Number 0
        self.spawnSkeletonFighters(0, 25, 9, 4)
        self.eliminateSkeletonFighters(0)

        # Spawner Zone Number 1
        self.spawnSkeletonFighters(1, 4, 18, 3)
        self.eliminateSkeletonFighters(1)

        # Spawner Zone Number 2
        self.spawnSkeletonFighters(2, 39, 22, 2)
        self.eliminateSkeletonFighters(2)

        # Spawner Zone Number 3
        self.spawnSkeletonFighters(3, 21, 27, 4)
        self.eliminateSkeletonFighters(3)

        # Spawner Zone Number 4
        self.spawnSkeletonFighters(4, 4, 26, 2)
        self.eliminateSkeletonFighters(4)
        # Spawner Zone Number 5
        self.spawnSkeletonFighters(5, 4, 30, 2)
        self.eliminateSkeletonFighters(5)



    def renderDungeon1(self):
        self.game.virtual_screen.blit(self.game.background, (0, 0))
        self.game.tilemap.render(screen= self.game.virtual_screen, tile_pos=self.game.player.getTileCoords() , offset=self.game.render_camera)
        self.game.player.render(self.game.virtual_screen, offset=self.game.render_camera)
        for projectile in self.game.projectiles:
            projectile.render(self.game.virtual_screen, offset=self.game.render_camera)

        for enemy in self.game.enemiesList:
            enemy.render(self.game.virtual_screen, offset=self.game.render_camera)

        self.game.abilitiesHud.renderAbilitiesHud(self.game.virtual_screen)
