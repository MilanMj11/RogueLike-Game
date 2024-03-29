import pygame
from constants import *


class TileMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_size = 128
        self.tiles = [[None for col in range(width)] for row in range(height)]

    def initTiles(self):
        for row in range(self.height):
            for col in range(self.width):
                self.tiles[row][col] = Tile(row, col, "floor")

    def setTile(self, row, col, type):
        self.tiles[row][col] = Tile(row, col, type)

    def getTile(self, row, col):
        return self.tiles[row][col]

    def render(self, screen, offset=(0, 0)):
        for row in range(self.height):
            for col in range(self.width):
                tile = self.getTile(row, col)
                if tile != None:
                    tile.render(screen, offset)


class Tile(pygame.sprite.Sprite):
    def __init__(self, row, col, type):
        super().__init__()
        self.type = type
        self.row = row
        self.col = col
        self.initImage()

    def initImage(self):
        image = pygame.image.load("assets/tilemap/" + self.type + ".png").convert_alpha()
        self.setImage(image)

    def setImage(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.col * 128, self.row * 128)

    def render(self, screen, offset=(0, 0)):
        screen.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))
