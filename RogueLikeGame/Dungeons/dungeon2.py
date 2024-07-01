import pygame
from constants import *
from tiles import *
from player import *
from gameStateManager import GameStateManager
from Enemies.skeletonFighter import SkeletonFighter
from Enemies.skeletonArcher import SkeletonArcher

class Dungeon2:
    def __init__(self, game):
        self.game = game
        self.game.enemiesList = []
        self.lastSkeletonFighterSpawn = [0 for _ in range(20)]  # Let's say I have maximum 10 spawners
        self.lastSkeletonArcherSpawn = [0 for _ in range(20)]
        # lastSkeletonFighterSpawn[spawnerNr] = last time a skeleton was spawned by the spawner Nr

        self.spawners = [[] for _ in range(20)]  # List of Lists of Enemies
        self.spawnerTotalSpawns = [0 for _ in range(20)]  # Total number of spawns by the spawner Nr
        self.init_Dungeon_2()

    def init_Dungeon_2(self):
        self.game.background.fill((118, 59, 54))
        self.game.tilemap = TileMap(60, 60)
        self.game.tilemap.load("Dungeons/dungeon2_map.txt")

        # self.game.player.loadPlayer()

        self.game.player.position = [4 * TILESIZE, 4 * TILESIZE]
        self.game.player.speed = 3

    def checkDungeon2GameEvents(self, eventList):
        self.game.player.handleEvents(eventList)
        for event in eventList:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.gameStateManager.switchGameState("Menu", "Pause Menu Dungeon")
                if event.key == pygame.K_e:
                    # Here we check if the player is next to the door, so he can exit the dungeon
                    for tile in self.game.player.getTilesAround4():
                        if tile.decorAssetPosition == [10, 3] or tile.decorAssetPosition == [11, 3]:
                            # Advance the game to the next dungeon as this one is completed
                            self.game.progressToNextDungeonAndSave()
                            # Might want to switch to the next dungeon -> for now Lobby makes it.
                            self.game.gameStateManager.switchGameState("Dungeon 3")
                            break
                        if tile.decorAssetPosition == [10, 2] or tile.decorAssetPosition == [11, 2]:
                            # Return to Lobby and save the progression of player through the dungeon
                            self.game.player.savePlayer()
                            self.game.gameStateManager.switchGameState("Lobby")
                            break

    def spawnSkeletonFighters(self, spawnerNr, x, y, size=4, totalSpawns=10):
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

    def spawnSkeletonArcher(self, spawnerNr, x, y, size=4, totalSpawns=10):
        # This function acts like a Spawner, that constantly spawns enemies
        if self.spawners[spawnerNr].__len__() >= size:
            return

        if self.spawnerTotalSpawns[spawnerNr] >= totalSpawns:
            return

        current_time = self.game.current_time

        if current_time - self.lastSkeletonArcherSpawn[spawnerNr] > 5000:
            self.lastSkeletonArcherSpawn[spawnerNr] = current_time
            self.spawners[spawnerNr].append(SkeletonArcher(self.game, [x * TILESIZE, y * TILESIZE]))
            self.spawnerTotalSpawns[spawnerNr] += 1
            self.game.enemiesList.append(self.spawners[spawnerNr][-1])

    def eliminateSkeletonArchers(self, spawnerNr):
        for skeleton in self.spawners[spawnerNr]:
            if skeleton not in self.game.enemiesList:
                self.spawners[spawnerNr].remove(skeleton)

    def updateSpawnLocations(self):
        # Spawner Zone Number 0
        self.spawnSkeletonArcher(0, 5, 19, 1)
        self.eliminateSkeletonArchers(0)

        # Spawner Zone Number 1
        self.spawnSkeletonArcher(1, 13, 19, 1)
        self.eliminateSkeletonArchers(1)

        # Spawner Zone Number 2
        self.spawnSkeletonFighters(2, 5, 28, 1)
        self.eliminateSkeletonFighters(2)

        # Spawner Zone Number 3
        self.spawnSkeletonFighters(3, 26, 17, 1)
        self.eliminateSkeletonFighters(3)

        # Spawner Zone Number 4
        self.spawnSkeletonArcher(4, 19, 4, 1)
        self.eliminateSkeletonArchers(4)

        # Spawner Zone Number 5
        self.spawnSkeletonArcher(5, 24, 4, 1)
        self.eliminateSkeletonArchers(5)

        # Spawner Zone Number 6
        self.spawnSkeletonFighters(6, 22, 8, 1)
        self.eliminateSkeletonFighters(6)

        # Spawner Zone Number 7
        self.spawnSkeletonFighters(7, 35, 15, 1)
        self.eliminateSkeletonFighters(7)

        # Spawner Zone Number 8
        self.spawnSkeletonFighters(8, 46, 6, 1)
        self.eliminateSkeletonFighters(8)

        # Spawner Zone Number 9
        self.spawnSkeletonArcher(9, 46, 21, 1)
        self.eliminateSkeletonArchers(9)

        # Spawner Zone Number 10
        self.spawnSkeletonFighters(10, 44, 28, 1)
        self.eliminateSkeletonFighters(10)

        # Spawner Zone Number 11
        self.spawnSkeletonFighters(11, 22, 25, 1)
        self.eliminateSkeletonFighters(11)

        # Spawner Zone Number 12
        self.spawnSkeletonArcher(12, 14, 38, 1)
        self.eliminateSkeletonArchers(12)

        # Spawner Zone Number 13
        self.spawnSkeletonArcher(13, 18, 33, 1)
        self.eliminateSkeletonArchers(13)

        # Spawner Zone Number 14
        self.spawnSkeletonFighters(14, 10, 33, 1)
        self.eliminateSkeletonFighters(14)

        # Spawner Zone Number 15
        self.spawnSkeletonFighters(15, 14, 33, 1)
        self.eliminateSkeletonFighters(15)

    def updateDungeon2(self):

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

        self.updateSpawnLocations()


    def renderDungeon2(self):
        self.game.virtual_screen.blit(self.game.background, (0, 0))
        self.game.tilemap.render(screen=self.game.virtual_screen, tile_pos=self.game.player.getTileCoords(),
                                 offset=self.game.render_camera)
        self.game.player.render(self.game.virtual_screen, offset=self.game.render_camera)
        for projectile in self.game.projectiles:
            projectile.render(self.game.virtual_screen, offset=self.game.render_camera)

        for enemy in self.game.enemiesList:
            enemy.render(self.game.virtual_screen, offset=self.game.render_camera)

        self.game.abilitiesHud.renderAbilitiesHud(self.game.virtual_screen)
