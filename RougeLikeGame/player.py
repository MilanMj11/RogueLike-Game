import math
import time
import pygame

import game
from constants import *
from projectile import Projectile

NEIGHBOURS_OFFSET = [[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]]


class Player(pygame.sprite.Sprite):  # Inherit from pygame.sprite.Sprite
    def __init__(self, game, pos, size=(128, 128)):
        super().__init__()
        self.image = pygame.image.load("assets/white_pawn.png").convert_alpha()
        self.image.set_colorkey((100, 100, 100))
        self.size = size
        self.position = list(pos)
        self.game = game
        self.attackSpeed = PLAYER_ATTACK_SPEED
        self.initProjectileImage()
        self.last_call_time = 0

    def initProjectileImage(self):
        self.projectileImage = pygame.image.load("assets/projectile.png").convert_alpha()
        self.projectileImage = pygame.transform.scale(self.projectileImage, (32, 32))
        self.projectileImage.set_colorkey((100, 100, 100))

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

    def shootProjectile(self):
        if pygame.mouse.get_pressed()[0]:
            mousePos = pygame.mouse.get_pos()
            # get the direction of the projectile
            playerPos = SCREEN_WIDTH / 2 + self.size[0] / 2, SCREEN_HEIGHT / 2 + self.size[1] / 2

            direction = [mousePos[0] - playerPos[0], mousePos[1] - playerPos[1]]
            length = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
            direction = [direction[0] / length, direction[1] / length]

            projectile = Projectile(self.game, self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2,
                                    direction, 10)

            projectile.setImage(self.projectileImage)
            self.game.projectiles.append(projectile)
            return True
        return False

    def update(self):

        # I only want to shoot depending on the self.attackSpeed, every 1 / self.attackSpeed seconds

        current_time = pygame.time.get_ticks()

        if current_time - self.last_call_time >= 1000 / self.attackSpeed:
            if self.shootProjectile():
                self.last_call_time = current_time

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
            movement[1] -= PLAYER_SPEED
        if keys[pygame.K_s]:
            movement[1] += PLAYER_SPEED
        if keys[pygame.K_a]:
            movement[0] -= PLAYER_SPEED
        if keys[pygame.K_d]:
            movement[0] += PLAYER_SPEED

        return movement

    def render(self, screen, offset=(0, 0)):
        screen.blit(self.image, (self.position[0] - offset[0], self.position[1] - offset[1]))
