import random

import pygame
from constants import *

DirectionOFFSET4 = [[0, -1], [0, 1], [-1, 0], [1, 0]]


class TileMap:
    def __init__(self, width=10, height=10, tilemap_type="desert"):
        self.width = width
        self.height = height
        self.tile_size = TILESIZE
        self.tiles = [[None for col in range(self.width)] for row in range(self.height)]
        self.last_randomSet_tile_ind = 0
        self.tilemap_type = tilemap_type

    def returnInformation(self):
        return (self.width, self.height, self.tile_size)

    def save(self, filename):
        # save the tilemap to a file

        # create a file with the filename and write the tilemap to it
        with open(filename, "w") as file:
            file.write(str(self.returnInformation()))
            file.write("\n")
            for row in range(self.height):
                for col in range(self.width):
                    tile = self.getTile(row, col)
                    if tile != None:
                        file.write(str(tile.returnInformation()))
                        file.write("\n")

    def load(self, filename, tilemap_type="desert"):
        # if the file is empty do nothing:
        with open(filename, "r") as file:
            if file.readline() == "":
                return

        # load the tilemap from the file and set the tilemap to the loaded tilemap

        # open the file with the filename and read the tilemap from it
        with open(filename, "r") as file:
            # reading the tilemap information
            tilemap_info = file.readline().strip()
            tilemap_info = tilemap_info[1:-1].split(", ")
            self.width = int(tilemap_info[0])
            self.height = int(tilemap_info[1])
            self.tile_size = int(tilemap_info[2])

            # read the tiles from the file

            # while I'm reading lines:

            while True:

                tile_info = file.readline().strip()
                if not tile_info:
                    break
                tile_info = tile_info[1:-1].split(", ")

                tile_row = int(tile_info[0])
                tile_col = int(tile_info[1])

                # get rid of ' ' ' ' from the string
                tile_type = tile_info[2].strip('"').strip("'")

                tile_assetPosition_x = int(tile_info[3][1:])
                tile_assetPosition_y = int(tile_info[4][:-1])
                tile_assetPosition = [tile_assetPosition_x, tile_assetPosition_y]
                tile_rotation = int(tile_info[5])

                tile_decorAssetPosition = [int(tile_info[6][1:]), int(tile_info[7][:-1])]

                self.loadTile(tile_row, tile_col, tile_type, tile_assetPosition, tile_rotation, tile_decorAssetPosition,
                              tilemap_type)

        # self.stylize_map()

    def loadTile(self, row, col, type, assetPosition, rotation, decorAssetPosition, tilemap_type="desert"):
        self.setTile(row, col, str(type))

        self.getTile(row, col).rotation = rotation

        # get Tile Image from the tilemap_packed.png with the assetPosition

        if assetPosition != [-1, -1]:
            self.getTile(row, col).assetPosition = assetPosition

            tilemapAssetImage = pygame.image.load(
                "assets/tilemap/Tilemap/" + tilemap_type + "_tilemap_packed.png").convert_alpha()
            tile_surface = tilemapAssetImage.subsurface(
                pygame.Rect(assetPosition[0] * 16, assetPosition[1] * 16, 16, 16))
            image = pygame.transform.scale(tile_surface, (TILESIZE, TILESIZE))
            image = pygame.transform.rotate(image, rotation)
            self.setTileImage(row, col, image)

        # get Decor Image from the tilemap_packed.png with the decorAssetPosition

        if decorAssetPosition != [-1, -1]:
            self.getTile(row, col).decorAssetPosition = decorAssetPosition

            decorImage = pygame.image.load(
                "assets/tilemap/Tilemap/" + tilemap_type + "_tilemap_packed.png").convert_alpha()
            decor_surface = decorImage.subsurface(
                pygame.Rect(decorAssetPosition[0] * 16, decorAssetPosition[1] * 16, 16, 16))
            decorImage = pygame.transform.scale(decor_surface, (TILESIZE, TILESIZE))
            self.setTileDecorImage(row, col, decorImage)

        # self.setCorrectAssetPosition(row, col)

    def interior(self, row, col):
        return row >= 0 and row < self.height and col >= 0 and col < self.width

    def getType(self, row, col):
        if self.interior(row, col) and self.tiles[row][col] != None:
            return self.tiles[row][col].type
        return None

    def setCorrectAssetPosition(self, row, col):
        tile = self.getTile(row, col)

        if tile == None:
            return

        if tile != None:
            if tile.type == "floor":

                tile.assetPosition = [0, 4]

                if self.tiles[row - 1][col] != None and self.tiles[row - 1][col].type == "wall":
                    tile.assetPosition = [2, 4]

                if self.tiles[row][col - 1] != None and self.tiles[row][col - 1].type == "wall":
                    if tile.assetPosition == [2, 4]:
                        tile.assetPosition = [4, 4]
                        tile.rotation = 90
                    else:
                        tile.assetPosition = [2, 4]
                        tile.rotation = 90

                # if tile is surrounded by floors
                if self.tiles[row - 1][col] != None and self.tiles[row - 1][col].type == "floor" and \
                        self.tiles[row + 1][col] != None and self.tiles[row + 1][col].type == "floor" and \
                        self.tiles[row][col - 1] != None and self.tiles[row][col - 1].type == "floor" and \
                        self.tiles[row][col + 1] != None and self.tiles[row][col + 1].type == "floor":
                    self.last_randomSet_tile_ind += 1
                    if self.last_randomSet_tile_ind % 10 == 0:
                        tile.assetPosition = [1, 4]


            elif tile.type == "wall":

                tile.assetPosition = [4, 3]

                neighbors = 0

                # if wall is surrounded by walls
                for offset in NEIGHBOURS_OFFSET:
                    row_offset = row + offset[0]
                    col_offset = col + offset[1]
                    if self.interior(row_offset, col_offset) == False:
                        neighbors += 1
                    if self.interior(row_offset, col_offset):
                        if self.getTile(row_offset, col_offset) != None and self.getTile(row_offset,
                                                                                         col_offset).type == "wall":
                            neighbors += 1

                if self.getType(row, col + 1) == "floor":
                    # Left wall
                    tile.assetPosition = [1, 1]

                if self.getType(row, col - 1) == "floor":
                    # Right wall
                    tile.assetPosition = [3, 1]

                if self.getType(row + 1, col) == "floor":
                    # Top wall
                    tile.assetPosition = [4, 3]
                    if self.getType(row, col - 1) == "floor":
                        tile.assetPosition = [9, 4]
                    if self.getType(row, col + 1) == "floor":
                        tile.assetPosition = [11, 4]

                if self.getType(row - 1, col) == "floor":
                    # Bottom wall
                    tile.assetPosition = [2, 2]
                    if self.getType(row, col - 1) == "floor":
                        tile.assetPosition = [4, 0]
                    if self.getType(row, col + 1) == "floor":
                        tile.assetPosition = [5, 0]

                if self.getType(row - 1, col) == "wall":
                    if self.getType(row + 1, col) == "wall":
                        if self.getType(row + 2, col) == "floor":
                            if tile.assetPosition == [3, 1]:
                                tile.assetPosition = [4, 1]
                            if tile.assetPosition == [1, 1]:
                                tile.assetPosition = [5, 1]
                            if tile.assetPosition == [4, 3]:
                                tile.assetPosition = [2, 0]

                        # tile.assetPosition = [2, 0]

                if tile.assetPosition == [4, 3]:
                    if self.getType(row + 1, col) == "wall":
                        if self.getType(row + 2, col) == "floor":
                            tile.assetPosition = [2, 0]
                    if neighbors == 8:
                        if self.getType(row + 1, col + 1) == "floor":
                            tile.assetPosition = [1, 1]

                        if self.getType(row + 1, col - 1) == "floor":
                            tile.assetPosition = [3, 1]

                        if self.getType(row - 1, col + 1) == "floor":
                            tile.assetPosition = [1, 2]

                        if self.getType(row - 1, col - 1) == "floor":
                            tile.assetPosition = [3, 2]

                    if self.getType(row, col + 1) == "wall":
                        if self.getType(row + 1, col + 1) == "wall":
                            if self.getType(row + 2, col + 1) == "floor":
                                if self.getType(row + 2, col) != "floor":
                                    tile.assetPosition = [1, 0]

                    if self.getType(row, col - 1) == "wall":
                        if self.getType(row + 1, col - 1) == "wall":
                            if self.getType(row + 2, col - 1) == "floor":
                                if self.getType(row + 2, col) != "floor":
                                    tile.assetPosition = [3, 0]

                if tile.assetPosition != [4, 3]:
                    tile.initImage()
                    return

                if neighbors == 9:
                    tile.assetPosition = [0, 0]
                    tile.initImage()
                    return

        if tile != None:
            tile.initImage()

    def stylize_map(self):
        for row in range(self.height):
            for col in range(self.width):
                self.setCorrectAssetPosition(row, col)

    def fillNonesWithWalls(self):
        for row in range(self.height):
            for col in range(self.width):
                if self.tiles[row][col] == None:
                    self.setTile(row, col, "wall")

    def reduceDimensions(self, new_width, new_height):
        self.width = new_width
        self.height = new_height

    def reduceDimensionsDinamically(self):
        # find the most right and most bottom tile
        most_right = 0
        most_bottom = 0
        for row in range(self.height):
            for col in range(self.width):
                if self.tiles[row][col] != None:
                    most_right = max(most_right, col)
                    most_bottom = max(most_bottom, row)

        self.reduceDimensions(most_right + 1, most_bottom + 1)
        self.fillNonesWithWalls()

    def fillTileWithFloor(self):
        for row in range(self.height):
            for col in range(self.width):
                self.setTile(row, col, "floor")

    def setTileImage(self, row, col, image):
        self.tiles[row][col].setImage(image)

    def setTileDecorImage(self, row, col, image):
        self.tiles[row][col].decorImage = image

    def setTileDecorAssetPosition(self, row, col, assetPosition):
        self.tiles[row][col].decorAssetPosition = assetPosition

    def setTileAssetPosition(self, row, col, assetPosition):
        self.getTile(row, col).assetPosition = assetPosition

    def setTile(self, row, col, type):
        self.tiles[row][col] = Tile(row, col, type)

    def delTile(self, row, col):
        self.tiles[row][col] = None

    def getTile(self, row, col):
        return self.tiles[row][col]

    def renderAll(self, screen, offset=(0, 0)):
        for row in range(self.height):
            for col in range(self.width):
                tile = self.getTile(row, col)
                if tile != None:
                    tile.render(screen, offset)

    # optimized render
    def render(self, tile_pos, screen, offset=(0, 0)):
        # I want to render only the tiles that should be visible instead of all the tiles
        # I will render the tiles that are in the screen and the tiles that are around the screen
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        tile_size = TILESIZE
        tilesX = screen_width // tile_size
        tilesY = screen_height // tile_size

        tilesUp = tilesY // 2 + 2
        tilesDown = tilesY // 2 + 2
        tilesLeft = tilesX // 2 + 2
        tilesRight = tilesX // 2 + 2

        mostLeftTile = max(0, tile_pos[1] - tilesLeft)
        mostRightTile = min(tile_pos[1] + tilesRight, self.width)
        mostUpTile = max(0, tile_pos[0] - tilesUp)
        mostDownTile = min(tile_pos[0] + tilesDown, self.height)

        for row in range(mostUpTile, mostDownTile):
            for col in range(mostLeftTile, mostRightTile):
                tile = self.getTile(row, col)
                if tile != None:
                    tile.render(screen, offset)


class Tile(pygame.sprite.Sprite):
    def __init__(self, row, col, type):
        super().__init__()
        self.type = type
        self.row = row
        self.col = col
        self.assetPosition = [-1, -1]
        self.rotation = 0
        self.initImage()
        self.decorImage = None
        self.decorAssetPosition = [-1, -1]

    def updateDecorAssetPosition(self, assetPosition, tilemap_type="desert"):
        self.decorAssetPosition = assetPosition
        self.updateDecorImage(tilemap_type)

    def updateDecorImage(self, tilemap_type="desert"):
        if self.decorAssetPosition == [-1, -1]:
            self.decorImage = None

        if self.decorAssetPosition != [-1, -1]:
            decorImage = pygame.image.load(
                "assets/tilemap/Tilemap/" + tilemap_type + "_tilemap_packed.png").convert_alpha()
            decor_surface = decorImage.subsurface(
                pygame.Rect(self.decorAssetPosition[0] * 16, self.decorAssetPosition[1] * 16, 16, 16))
            decorImage = pygame.transform.scale(decor_surface, (TILESIZE, TILESIZE))
            self.decorImage = decorImage

    def returnInformation(self):
        if self != None:
            return (self.row, self.col, self.type, self.assetPosition, self.rotation, self.decorAssetPosition)

    def getRect(self):
        return pygame.Rect(self.col * TILESIZE, self.row * TILESIZE, TILESIZE, TILESIZE)

    def initImage(self, tilemap_type="desert"):
        if self.type == "BLANK":
            image = pygame.Surface((TILESIZE, TILESIZE))
            image.fill((0, 0, 0))
            self.setImage(image)
            return

        if self.assetPosition != [-1, -1]:
            tile_surface = (pygame.image.load(
                "assets/tilemap/Tilemap/" + tilemap_type + "_tilemap_packed.png").convert_alpha()).subsurface(
                pygame.Rect(self.assetPosition[0] * 16, self.assetPosition[1] * 16, 16, 16))
            image = pygame.transform.scale(tile_surface, (TILESIZE, TILESIZE))  # .transform.scale((TILESIZE, TILESIZE))
            image = pygame.transform.rotate(image, self.rotation)
            # scale the image to the tile size
            # image = pygame.transform.scale(image, (TILESIZE, TILESIZE))
            self.setImage(image)

    def setImage(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.col * TILESIZE, self.row * TILESIZE)

    def render(self, screen, offset=(0, 0)):
        if self.image != None:
            screen.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))
            if self.decorImage != None:
                screen.blit(self.decorImage, (self.rect.x - offset[0], self.rect.y - offset[1]))
