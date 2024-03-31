import pygame
from constants import *


class TileMap:
    def __init__(self, width = 10, height = 10):
        self.width = width
        self.height = height
        self.tile_size = TILESIZE
        self.tiles = []

    def init_Lobby(self):
        self.width = 33
        self.height = 18

        self.tiles = [[None for col in range(self.width)] for row in range(self.height)]

        for row in range(self.height):
            for col in range(self.width):
                self.tiles[row][col] = Tile(row, col, "floor")

        # Personal Room
        for j in range(5,10):
            self.setTile(0,j,"wall")
        for i in range(1,6):
            self.setTile(i,4,"wall")
            self.setTile(i,10,"wall")
        self.setTile(6,5,"wall")
        self.setTile(6,6,"wall")
        self.setTile(6,8,"wall")
        self.setTile(6,9,"wall")

        # Hallway
        for j in range(10,17):
            self.setTile(6,j,"wall")
        for j in range(9,25):
            if j == 15 or j == 16 or j == 17:
                continue
            self.setTile(10,j,"wall")
        self.setTile(10,5,"wall")
        for i in range(7,10):
            self.setTile(i,4,"wall")
        for j in range(22,25):
            self.setTile(6,j,"wall")

        # Gable Room
        for j in range(1,5):
            self.setTile(11,j,"wall")
        for i in range(12,17):
            self.setTile(i,0,"wall")
        for j in range(1,24):
            self.setTile(17,j,"wall")
        for j in range(10,14):
            self.setTile(11,j,"wall")
        for i in range(12,17):
            self.setTile(i,12,"wall")

        # Black Smith
        for i in range(12,17):
            self.setTile(i,13,"wall")
        for i in range(11,17):
            self.setTile(i,24,"wall")

        # Shop
        for i in range(1,7):
            self.setTile(i,13,"wall")
        for i in range(1,7):
            self.setTile(i,24,"wall")
        for j in range(14,24):
            self.setTile(0,j,"wall")

        # Dungeon Entrance
        self.setTile(5,25,"wall")
        for j in range(26,29):
            self.setTile(4,j,"wall")
        self.setTile(5,29,"wall")
        self.setTile(11,25,"wall")
        for j in range(26,29):
            self.setTile(12,j,"wall")
        self.setTile(11,29,"wall")
        self.setTile(6,30,"wall")
        self.setTile(6,31,"wall")
        self.setTile(10,30,"wall")
        self.setTile(10,31,"wall")
        for i in range(7,10):
            self.setTile(i,32,"wall")

        # making the outside full of BLANK
        for i in range(11):
            for j in range(4):
                self.setTile(i,j,"BLANK")
        self.setTile(6,4,"BLANK")
        self.setTile(10,4,"BLANK")
        self.setTile(11,0,"BLANK")
        self.setTile(17,0,"BLANK")
        self.setTile(0,4,"BLANK")
        for j in range(10,14):
            self.setTile(0,j,"BLANK")
        for i in range(1,6):
            self.setTile(i,11,"BLANK")
            self.setTile(i,12,"BLANK")

        for i in range(4):
            for j in range(25,33):
                self.setTile(i,j,"BLANK")
                self.setTile(17-i,j,"BLANK")
        self.setTile(0,24,"BLANK")
        self.setTile(4,25,"BLANK")
        for j in range(29,33):
            self.setTile(4,j,"BLANK")
        for j in range(30,33):
            self.setTile(5,j,"BLANK")
        self.setTile(6,32,"BLANK")

        for j in range(25,33):
            self.setTile(13,j,"BLANK")
        self.setTile(17,24,"BLANK")
        self.setTile(12,25,"BLANK")
        for j in range(29,33):
            self.setTile(12,j,"BLANK")
        for j in range(30,33):
            self.setTile(11,j,"BLANK")
        self.setTile(10,32,"BLANK")


    def init_Dungeon_1(self):

        self.height = 20
        self.width = 20

        self.tiles = [[None for col in range(self.width)] for row in range(self.height)]

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
