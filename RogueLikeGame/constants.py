import threading

import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
# 2560 x 1440
# 1920 x 1080
# 1440 x 810
VIRTUALSCREEN_WIDTH = 1024
VIRTUALSCREEN_HEIGHT = 576
# 960 x 540
# 1024 x 576

ABILITIES_HUD_WIDTH = 178
ABILITIES_HUD_HEIGHT = 52

HEALTH_HUD_WIDTH = 182
HEALTH_HUD_HEIGHT = 36

NEIGHBOURS_OFFSET = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1], [0, 0]]

TILESIZE = 64

PLAYER_HEALTH = 100
PLAYER_SPEED = 2
# attacks per second
PLAYER_ATTACK_SPEED = 1

FPS = 90

CAMERA_FOLLOW_RATE = 13

ENEMY_SPEED = 2
ENEMY_ATTACK_SPEED = 1

SKELETON_FIGHTER_DAMAGE = 10
SKELETON_FIGHTER_ATTACK_SPEED = 1
SKELETON_FIGHTER_HEALTH = 30
SKELETON_FIGHTER_SPEED = 1

SKELETON_ARCHER_DAMAGE = 10
SKELETON_ARCHER_ATTACK_SPEED = 0.7
SKELETON_ARCHER_HEALTH = 25
SKELETON_ARCHER_SPEED = 0.8
SKELETON_ARCHER_ARROW_SPEED = 3
SKELETON_ARCHER_SHOOTING_RANGE = 250