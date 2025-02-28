import pygame
import math
from constants import *
from healthbar import HealthBar


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, pos, health, size=(40, 40)):
        super().__init__()
        self.game = game
        self.position = list(pos)
        self.size = size
        self.speed = ENEMY_SPEED
        self.attackSpeed = ENEMY_ATTACK_SPEED
        self.health = health
        self.healthBar = HealthBar(self.health, self.health, self.position)

        self.image = None
        self.facing = "LEFT"
        self.gotAttacked = False

        self.damageDisplayTimer = 0
        self.xpValue = None

    def getKilled(self):
        self.game.enemiesList.remove(self)
        self.game.player.experience.add_xp(self.xpValue)
        self.game.player.coins += 10

    def getDamaged(self, damage):
        self.health -= damage
        self.gotAttacked = True
        position_copy = self.position.copy()
        time_copy = self.game.current_time
        self.game.damage_numbers.append((damage, position_copy, time_copy))
        if self.health <= 0:
            self.getKilled()

    def getTilesAround(self):
        # get the tiles around the enemy
        tiles = []
        enemyTile = self.game.tilemap.getTile(int(self.position[1] / TILESIZE), int(self.position[0] / TILESIZE))
        for offset in NEIGHBOURS_OFFSET:
            row = enemyTile.row + offset[0]
            col = enemyTile.col + offset[1]
            if row >= 0 and row < self.game.tilemap.height and col >= 0 and col < self.game.tilemap.width:
                tiles.append(self.game.tilemap.getTile(row, col))
        return tiles

    def getRectMiddlePoint(self):
        return (self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2)

    def getTile(self):
        return self.game.tilemap.getTile(int((self.position[1] + self.size[1] / 2) / TILESIZE),
                                         int((self.position[0] + self.size[0] / 2) / TILESIZE))

    def getRect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def update(self):
        self.healthBar.update(self.health)

    def render(self, screen, offset=(0, 0)):

        self.healthBar.render(screen, offset)

        if self.image != None:
            if self.facing == "RIGHT":
                flippedImage = pygame.transform.flip(self.image, True, False)
                screen.blit(flippedImage, (self.position[0] - offset[0], self.position[1] - offset[1]))
            else:
                screen.blit(self.image, (self.position[0] - offset[0], self.position[1] - offset[1]))
