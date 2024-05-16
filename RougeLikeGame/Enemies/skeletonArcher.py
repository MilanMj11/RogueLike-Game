import random

import pygame
import math
from constants import *
from Enemies.enemy import Enemy
from projectile import Projectile

class SkeletonArcher(Enemy):
    def __init__(self, game, pos, health=SKELETON_ARCHER_HEALTH, size=(40, 40)):
        super().__init__(game, pos, health, size)
        self.image = pygame.image.load("assets/skeleton_archer/skeletonArcher_frame1.png").convert_alpha()
        self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale(self.image, size)
        # self.image.set_colorkey((100, 100, 100))
        self.health = health
        self.damage = SKELETON_ARCHER_DAMAGE
        self.attackSpeed = SKELETON_ARCHER_ATTACK_SPEED
        self.arrowSpeed = SKELETON_ARCHER_ARROW_SPEED
        self.shootingRange = SKELETON_ARCHER_SHOOTING_RANGE
        self.last_attack_time = 0
        self.speed = SKELETON_ARCHER_SPEED
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

    def move(self, movement):
        tilesAround = self.getTilesAround()

        # check collision with walls
        self.position[0] += movement[0]
        skeletonRect = self.getRect()
        for tile in tilesAround:
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
        for tile in tilesAround:
            if tile.type == "wall":
                tileRect = tile.getRect()
                if skeletonRect.colliderect(tileRect):
                    if movement[1] > 0:
                        skeletonRect.bottom = tileRect.top
                    if movement[1] < 0:
                        skeletonRect.top = tileRect.bottom

                    self.position[1] = skeletonRect.y

    def shootArrow(self):
        playerPos = self.game.player.getRectMiddlePoint()

        dx = playerPos[0] - self.getRectMiddlePoint()[0]
        dy = playerPos[1] - self.getRectMiddlePoint()[1]
        magnitude = math.sqrt(dx ** 2 + dy ** 2)
        direction = [dx / magnitude, dy / magnitude]


        arrow = Projectile(self.game, self.getRectMiddlePoint()[0], self.getRectMiddlePoint()[1], direction,
                           self.arrowSpeed, self.damage)
        arrow.setImage(pygame.image.load("assets/skeleton_archer/arrow.png"))
        arrow.playerProjectile = False

        # Rotate the arrow image
        angle = math.atan2(dx, dy)
        arrow.image = pygame.transform.rotate(arrow.image, math.degrees(angle - math.pi / 2))

        self.game.projectiles.append(arrow)

    def update(self):

        super().update()

        player = self.game.player
        playerRect = player.getRect()
        skeletonRect = self.getRect()
        distance = math.sqrt((player.getRectMiddlePoint()[0] - self.getRectMiddlePoint()[0]) ** 2 + (
                player.getRectMiddlePoint()[1] - self.getRectMiddlePoint()[1]) ** 2)

        current_time = self.game.current_time

        if distance <= self.shootingRange:
            # attack the player with projectile
            if current_time - self.last_attack_time >= 1000 / self.attackSpeed:
                self.last_attack_time = current_time
                self.shootArrow()

        if distance > self.shootingRange:
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

            self.move(movement)
