import pygame
from constants import *


class TileMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_size = TILESIZE
        self.tiles = [[None for col in range(width)] for row in range(height)]

    def init_Dungeon_1(self):
        for row in range(self.height):
            for col in range(self.width):
                self.tiles[row][col] = Tile(row, col, "floor")

        # random walls for testing
        for col in range(5, 10):
            self.setTile(5, col, "wall")
            self.setTile(6, col, "wall")
            self.setTile(7, col, "wall")
            self.setTile(8, col, "wall")
            self.setTile(9, col, "wall")
            self.setTile(10, col, "wall")

        # making the outside full of walls
        for row in range(self.height):
            self.setTile(row, 0, "wall")
            self.setTile(row, self.width - 1, "wall")
        for col in range(self.width):
            self.setTile(0, col, "wall")
            self.setTile(self.height - 1, col, "wall")


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

    def getRect(self):
        return pygame.Rect(self.col * TILESIZE, self.row * TILESIZE, self.image.get_width(), self.image.get_height())
    def initImage(self):
        image = pygame.image.load("assets/tilemap/" + self.type + ".png").convert_alpha()
        # scale the image to the tile size
        image = pygame.transform.scale(image, (TILESIZE, TILESIZE))
        self.setImage(image)

    def setImage(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.col * TILESIZE, self.row * TILESIZE)

    def render(self, screen, offset=(0, 0)):
        screen.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))
