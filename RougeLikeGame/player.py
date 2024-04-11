import math
import time
import pygame

import game
from constants import *
from projectile import Projectile

NEIGHBOURS_OFFSET = [[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]]


class Player(pygame.sprite.Sprite):  # Inherit from pygame.sprite.Sprite
    def __init__(self, game, pos, size=(40, 40)):
        super().__init__()
        # Animation frames
        self.animation_frames = [
            pygame.transform.scale(pygame.image.load("assets/player/frame_1.png").convert_alpha(), size),
            pygame.transform.scale(pygame.image.load("assets/player/frame_2.png").convert_alpha(), size),
            pygame.transform.scale(pygame.image.load("assets/player/frame_3.png").convert_alpha(), size)
        ]
        # Animation variables
        self.current_frame = 0
        self.frame_delay = 350
        self.last_frame_time = 0

        self.image = self.animation_frames[self.current_frame]
        self.image.set_colorkey((100, 100, 100))
        self.size = size
        self.position = list(pos)
        self.facing = "RIGHT"
        self.game = game
        self.health = PLAYER_HEALTH
        self.speed = PLAYER_SPEED
        self.attackSpeed = PLAYER_ATTACK_SPEED
        self.initProjectileImage()
        self.last_projectile_time = 0

        self.projectileSpeed = 4
        self.projectileDamage = 10

    def getTile(self):
        return self.game.tilemap.getTile(int((self.position[1] + self.size[1] / 2) / TILESIZE),
                                         int((self.position[0] + self.size[0] / 2) / TILESIZE))

    def getTileCoords(self):
        currentTile = self.getTile()
        return (currentTile.row, currentTile.col)

    def getRectMiddlePoint(self):
        return (self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2)

    def update_animation(self, current_time):
        # Update the animation frame
        if current_time - self.last_frame_time > self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.current_frame]
            self.last_frame_time = current_time

    def initProjectileImage(self):
        self.projectileImage = pygame.image.load("assets/projectile.png").convert_alpha()
        self.projectileImage = pygame.transform.scale(self.projectileImage, (32, 32))
        self.projectileImage.set_colorkey((100, 100, 100))

    def getRect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def getTilesAround(self):
        # get the tiles around the player
        tiles = []
        playerTile = self.game.tilemap.getTile(int(self.position[1] / TILESIZE), int(self.position[0] / TILESIZE))
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
            playerPos = SCREEN_WIDTH / 2 + self.size[0], SCREEN_HEIGHT / 2 + self.size[1]

            direction = [mousePos[0] - playerPos[0] + self.size[0], mousePos[1] - playerPos[1] + self.size[1]]
            length = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
            direction = [direction[0] / length, direction[1] / length]

            projectile = Projectile(self.game, self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2,
                                    direction, self.projectileSpeed, self.projectileDamage)

            projectile.setImage(self.projectileImage)
            self.game.projectiles.append(projectile)
            return True
        return False


    def movePlayer(self, movement):
        tilesAround = self.getTilesAround()

        # check collisions with walls
        self.position[0] += movement[0]
        playerRect = self.getRect()
        for tile in tilesAround:
            if tile.type == "wall":
                tileRect = tile.getRect()
                if playerRect.colliderect(tileRect):
                    # collided on the x axes
                    if movement[0] > 0.0:
                        playerRect.right = tileRect.left
                    if movement[0] < 0.0:
                        playerRect.left = tileRect.right

                    self.position[0] = playerRect.x

        self.position[1] += movement[1]
        playerRect = self.getRect()
        for tile in tilesAround:
            if tile.type == "wall":
                tileRect = tile.getRect()
                if playerRect.colliderect(tileRect):
                    # collided on the y axes
                    if movement[1] > 0.0:
                        playerRect.bottom = tileRect.top
                    if movement[1] < 0.0:
                        playerRect.top = tileRect.bottom

                    self.position[1] = playerRect.y
    def update(self):

        ''' For testing , print the player tile coords '''
        # print(self.getTile().row, self.getTile().col)

        # I only want to shoot depending on the self.attackSpeed, every 1 / self.attackSpeed seconds

        current_time = pygame.time.get_ticks()

        if self.game.gameStateManager.gameState != "Lobby":
            if current_time - self.last_projectile_time >= 1000 / self.attackSpeed:
                if self.shootProjectile():
                    self.last_projectile_time = current_time

        self.update_animation(current_time)

        MOVEMENT_DIVISION_FACTOR = 1
        movement = self.getDirectionInput()
        divided_movement = movement[0] / MOVEMENT_DIVISION_FACTOR, movement[1] / MOVEMENT_DIVISION_FACTOR

        for i in range(MOVEMENT_DIVISION_FACTOR):
            self.movePlayer(divided_movement)



    def getDirectionInput(self):
        keys = pygame.key.get_pressed()
        movement = [0, 0]

        if keys[pygame.K_w]:
            movement[1] -= self.speed
        if keys[pygame.K_s]:
            movement[1] += self.speed
        if keys[pygame.K_a]:
            movement[0] -= self.speed
            self.facing = "LEFT"
        if keys[pygame.K_d]:
            movement[0] += self.speed
            self.facing = "RIGHT"

        if movement[0] != 0.0 and movement[1] != 0.0:
            movement[0] *= 0.70
            movement[1] *= 0.70

        return movement

    def render(self, screen, offset=(0, 0)):

        if self.facing == "LEFT":
            flippedImage = pygame.transform.flip(self.image, True, False)
            flippedImage.set_colorkey((100, 100, 100))
            screen.blit(flippedImage, (self.position[0] - offset[0], self.position[1] - offset[1]))
        else:
            screen.blit(self.image, (self.position[0] - offset[0], self.position[1] - offset[1]))
