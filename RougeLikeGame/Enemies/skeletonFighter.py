import pygame
import math
from constants import *
from Enemies.enemy import Enemy

class SkeletonFighter(Enemy):
    def __init__(self, game, pos, size=(64, 64)):
        super().__init__(game, pos, size)
        self.image = pygame.image.load("assets/skeleton_fighter/skeletonFighter_frame1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        # self.image.set_colorkey((100, 100, 100))
        self.health = 100
        self.damage = SKELETON_FIGHTER_DAMAGE
        self.attackSpeed = SKELETON_FIGHTER_ATTACK_SPEED
        self.last_attack_time = 0

    def update(self):

        player = self.game.player
        playerRect = player.getRect()
        skeletonRect = self.getRect()
        distance = math.sqrt((player.getRectMiddlePoint()[0] - self.getRectMiddlePoint()[0]) ** 2 + (player.getRectMiddlePoint()[1] - self.getRectMiddlePoint()[1]) ** 2)

        current_time = pygame.time.get_ticks()

        if distance < 10:
            # attack the player
            if current_time - self.last_attack_time >= 1000 / self.attackSpeed:
                self.last_attack_time = current_time
                player.health -= self.damage
        else:
            # move towards the player
            dx = playerRect.x - skeletonRect.x
            dy = playerRect.y - skeletonRect.y
            angle = math.atan2(dy, dx)
            movement = [self.speed * math.cos(angle), self.speed * math.sin(angle)]
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