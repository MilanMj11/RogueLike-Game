import pygame
from constants import *


class HealthHUD:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font("assets/Pixeltype.ttf", 50)
        self.HUD = pygame.Surface((HEALTH_HUD_WIDTH, HEALTH_HUD_HEIGHT), pygame.SRCALPHA)

        self.image = pygame.image.load("assets/healthBar.png").convert_alpha()
        self.image.set_colorkey((100, 100, 100))
        #
        self.green_bar = pygame.rect.Rect((1, 1, HEALTH_HUD_WIDTH - 2, HEALTH_HUD_HEIGHT - 2))
        self.red_bar = pygame.rect.Rect((1, 1, HEALTH_HUD_WIDTH - 2, HEALTH_HUD_HEIGHT - 2))

    def updateHealthHUD(self):
        self.green_bar.width = self.game.player.health * (HEALTH_HUD_WIDTH - 2) / self.game.player.max_health

    def renderHealthHUD(self, surf):
        # Render the green health bar and red health bar

        pygame.draw.rect(self.HUD, (187, 0, 0), self.red_bar)
        pygame.draw.rect(self.HUD, (0, 156, 15), self.green_bar)

        # Render the imageHud to the HUD
        self.HUD.blit(self.image, (0, 0))

        # Render the overlay image
        surf.blit(self.HUD, (20, surf.get_height() - surf.get_height() / 10))
