import pygame
from constants import *


class Player(pygame.sprite.Sprite):  # Inherit from pygame.sprite.Sprite
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/white_pawn.png").convert_alpha()
        self.image.set_colorkey((100, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def update(self):
        pass

    def handleInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move(self.rect.x, self.rect.y - 5)
        if keys[pygame.K_s]:
            self.move(self.rect.x, self.rect.y + 5)
        if keys[pygame.K_a]:
            self.move(self.rect.x - 5, self.rect.y)
        if keys[pygame.K_d]:
            self.move(self.rect.x + 5, self.rect.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def move(self, x, y):
        self.rect.topleft = (x, y)
