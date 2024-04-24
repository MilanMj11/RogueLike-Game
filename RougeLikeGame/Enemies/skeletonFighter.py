import random

import pygame
import math
from constants import *
from Enemies.enemy import Enemy


class SkeletonFighter(Enemy):
    def __init__(self, game, pos, health=SKELETON_FIGHTER_HEALTH, size=(40, 40)):
        super().__init__(game, pos, health, size)
        self.image = pygame.image.load("assets/skeleton_fighter/skeletonFighter_frame1.png").convert_alpha()
        self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale(self.image, size)
        # self.image.set_colorkey((100, 100, 100))
        self.health = health
        self.damage = SKELETON_FIGHTER_DAMAGE
        self.attackSpeed = SKELETON_FIGHTER_ATTACK_SPEED
        self.last_attack_time = 0
        self.speed = SKELETON_FIGHTER_SPEED
        self.last_changeDirection_time = 0
        self.randomDirection = "UP"
        self.xpValue = 50

    def seePlayer(self):
        # if the player is in the line of sight of the skeleton
        player = self.game.player
        playerRect = player.getRect()
        skeletonRect = self.getRect()
        # if there are no walls between the player and the skeleton

        # get tiles between the player and the skeleton
        dx = playerRect.x - skeletonRect.x
        dy = playerRect.y - skeletonRect.y
        angle = math.atan2(dy, dx)
        distance = math.sqrt((player.getRectMiddlePoint()[0] - self.getRectMiddlePoint()[0]) ** 2 + (
                player.getRectMiddlePoint()[1] - self.getRectMiddlePoint()[1]) ** 2)

        for i in range(int(distance)):
            x = int(self.getRectMiddlePoint()[0] + i * math.cos(angle))
            y = int(self.getRectMiddlePoint()[1] + i * math.sin(angle))
            tile = self.game.tilemap.getTile(int(y / TILESIZE), int(x / TILESIZE))
            if tile.type == "wall":
                return False

        return True

    def update(self):

        super().update()

        player = self.game.player
        playerRect = player.getRect()
        skeletonRect = self.getRect()
        distance = math.sqrt((player.getRectMiddlePoint()[0] - self.getRectMiddlePoint()[0]) ** 2 + (
                player.getRectMiddlePoint()[1] - self.getRectMiddlePoint()[1]) ** 2)

        current_time = pygame.time.get_ticks()

        if distance < 10:
            # attack the player
            if current_time - self.last_attack_time >= 1000 / self.attackSpeed:
                self.last_attack_time = current_time
                player.health -= self.damage
        else:
            # move towards the player if the skeleton sees the player

            movement = [0, 0]

            if self.seePlayer() == False:
                # then just move randomly from time to time

                if current_time - self.last_changeDirection_time >= 1000:
                    self.last_changeDirection_time = current_time
                    self.randomDirection = random.choice(NEIGHBOURS_OFFSET)

                movement[0] = self.speed * self.randomDirection[0]
                movement[1] = self.speed * self.randomDirection[1]

            else:
                dx = playerRect.x - skeletonRect.x
                dy = playerRect.y - skeletonRect.y
                angle = math.atan2(dy, dx)
                movement = [self.speed * math.cos(angle) * 1.3, self.speed * math.sin(angle) * 1.3]

            if movement[0] > 0:
                self.facing = "RIGHT"
            else:
                self.facing = "LEFT"

            # check collision with walls
            self.position[0] += movement[0]
            skeletonRect = self.getRect()
            for tile in self.getTilesAround():
                if tile.type == "wall":
                    tileRect = tile.getRect()
                    if skeletonRect.colliderect(tileRect):
                        if movement[0] > 0:
                            skeletonRect.right = tileRect.left
                        if movement[0] < 0:
                            skeletonRect.left = tileRect.right

                        self.position[0] = skeletonRect.x

            self.position[1] += movement[1]
            skeletonRect = self.getRect()
            for tile in self.getTilesAround():
                if tile.type == "wall":
                    tileRect = tile.getRect()
                    if skeletonRect.colliderect(tileRect):
                        if movement[1] > 0:
                            skeletonRect.bottom = tileRect.top
                        if movement[1] < 0:
                            skeletonRect.top = tileRect.bottom

                        self.position[1] = skeletonRect.y
