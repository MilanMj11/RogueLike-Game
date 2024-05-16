import pygame
import math

from constants import *

NEIGHBOURS_OFFSET = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1], [0, 0]]


class Projectile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction, velocity, damage = 10):
        super().__init__()
        self.x = x
        self.y = y
        self.velocity = velocity
        self.direction = direction
        self.game = game
        self.image = None
        self.damage = damage
        self.playerProjectile = True

    def getRect(self):
        return pygame.Rect(self.x, self.y, 5, 5)

    def setImage(self, image, size=(20, 20)):
        self.image = pygame.transform.scale(image, size)
        self.image.convert_alpha()
        self.image.set_colorkey((100, 100, 100))

    def getTilesAround(self):
        tiles = []
        projectileRect = self.getRect()
        for offset in NEIGHBOURS_OFFSET:
            row = int((projectileRect.y + offset[1]) / TILESIZE)
            col = int((projectileRect.x + offset[0]) / TILESIZE)
            if row >= 0 and row < self.game.tilemap.height and col >= 0 and col < self.game.tilemap.width:
                tiles.append(self.game.tilemap.getTile(row, col))
        return tiles

    def update(self):
        # print(self.direction)

        self.x += self.velocity * self.direction[0]
        self.y += self.velocity * self.direction[1]
        projectileRect = self.getRect()
        # get tiles around the projectile
        for tile in self.getTilesAround():
            if tile.type == "wall":
                tileRect = tile.getRect()
                if projectileRect.colliderect(tileRect):
                    self.game.projectiles.remove(self)
                    return
        # check if projectile touches an enemy
        if self.playerProjectile == True:
            for enemy in self.game.enemiesList:
                if self.getRect().colliderect(enemy.getRect()):
                    enemy.getDamaged(self.damage)
                    self.game.projectiles.remove(self)
                    return

    def render(self, screen, offset=(0, 0)):
        if self.image != None:
            screen.blit(self.image, (
            self.x - offset[0] - self.image.get_size()[0] / 2, self.y - offset[1] - self.image.get_size()[1] / 2))
