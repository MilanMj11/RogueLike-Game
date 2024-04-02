import pygame
from constants import *
from Lobby.lobbyPreset import *

class TileMap:
    def __init__(self, width = 10, height = 10):
        self.width = width
        self.height = height
        self.tile_size = TILESIZE
        self.tiles = []

    def init_Tilemap_Lobby(self):
        self.width = 33
        self.height = 18

        self.tiles = [[None for col in range(self.width)] for row in range(self.height)]

        for row in range(self.height):
            for col in range(self.width):
                self.tiles[row][col] = Tile(row, col, "floor")

        for coords in LOBBY_WALLS:
            self.setTile(coords[0], coords[1], "wall")
        for coords in LOBBY_BLANKS:
            self.setTile(coords[0], coords[1], "BLANK")

    def init_Tilemap_Dungeon_1(self):

        self.height = 10
        self.width = 10

        self.tiles = [[None for col in range(self.width)] for row in range(self.height)]

        for row in range(self.height):
            for col in range(self.width):
                self.tiles[row][col] = Tile(row, col, "floor")

        # making the outside full of walls
        for row in range(self.height):
            self.setTile(row, 0, "wall")
            self.setTile(row, self.width - 1, "wall")
        for col in range(self.width):
            self.setTile(0, col, "wall")
            self.setTile(self.height - 1, col, "wall")

        self.setTile(3, 4, "wall")
        self.setTile(3, 5, "wall")

        self.setTile(2, 7, "wall")
        self.setTile(3, 7, "wall")

        self.setTile(6, 2, "wall")
        self.setTile(6, 3, "wall")
        self.setTile(7, 2, "wall")
        self.setTile(7, 3, "wall")


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
        if self.type == "BLANK":
            image = pygame.Surface((TILESIZE, TILESIZE))
            image.fill((0, 0, 0))
            self.setImage(image)
            return
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
