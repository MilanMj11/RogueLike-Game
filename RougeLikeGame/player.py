import pygame

import game
from constants import *

NEIGHBOURS_OFFSET = [[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]]


class Player(pygame.sprite.Sprite):  # Inherit from pygame.sprite.Sprite
    def __init__(self, game, pos, size=(128, 128)):
        super().__init__()
        self.image = pygame.image.load("assets/white_pawn.png").convert_alpha()
        self.image.set_colorkey((100, 100, 100))
        self.size = size
        self.position = list(pos)
        self.game = game

    def getRect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def getTilesAround(self):
        # get the tiles around the player
        tiles = []
        playerTile = self.game.tilemap.getTile(int(self.position[1] / 128), int(self.position[0] / 128))
        for offset in NEIGHBOURS_OFFSET:
            row = playerTile.row + offset[0]
            col = playerTile.col + offset[1]
            if row >= 0 and row < self.game.tilemap.height and col >= 0 and col < self.game.tilemap.width:
                tiles.append(self.game.tilemap.getTile(row, col))
        return tiles

    def update(self):

        movement = self.getDirectionInput()

        # check collisions with walls
        self.position[0] += movement[0]
        playerRect = self.getRect()
        for tile in self.getTilesAround():
            if tile.type == "wall":
                tileRect = tile.getRect()
                if playerRect.colliderect(tileRect):
                    # collided on the x axes
                    if movement[0] > 0:
                        playerRect.right = tileRect.left
                    if movement[0] < 0:
                        playerRect.left = tileRect.right

                    self.position[0] = playerRect.x

        self.position[1] += movement[1]
        playerRect = self.getRect()
        for tile in self.getTilesAround():
            if tile.type == "wall":
                tileRect = tile.getRect()
                if playerRect.colliderect(tileRect):
                    # collided on the y axes
                    if movement[1] > 0:
                        playerRect.bottom = tileRect.top
                    if movement[1] < 0:
                        playerRect.top = tileRect.bottom

                    self.position[1] = playerRect.y

    def getDirectionInput(self):
        keys = pygame.key.get_pressed()
        movement = [0, 0]

        if keys[pygame.K_w]:
            movement[1] -= 5
        if keys[pygame.K_s]:
            movement[1] += 5
        if keys[pygame.K_a]:
            movement[0] -= 5
        if keys[pygame.K_d]:
            movement[0] += 5

        return movement

    def render(self, screen, offset=(0, 0)):
        screen.blit(self.image, (self.position[0] - offset[0], self.position[1] - offset[1]))
