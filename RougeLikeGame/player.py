import pygame
from constants import *


class Player(pygame.sprite.Sprite):  # Inherit from pygame.sprite.Sprite
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/white_pawn.png").convert_alpha()
        self.image.set_colorkey((100, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (500, 500)

    def update(self):
        pass

    def handleInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= 5
        if keys[pygame.K_s]:
            self.rect.y += 5
        if keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_d]:
            self.rect.x += 5

    def render(self, screen, offset = (0,0)):
        screen.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))

    def move(self, x, y):
        self.position = (x, y)
