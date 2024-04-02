import pygame
import math
from constants import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, pos, size=(64, 64)):
        super().__init__()
        self.game = game
        self.position = list(pos)
        self.size = size
        self.speed = ENEMY_SPEED
        self.attackSpeed = ENEMY_ATTACK_SPEED

        self.image = None

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
        pass

    def render(self, screen, offset=(0, 0)):
        if self.image != None:
            screen.blit(self.image, (self.position[0] - offset[0], self.position[1] - offset[1]))