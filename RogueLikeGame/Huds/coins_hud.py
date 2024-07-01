import pygame

class CoinsHUD:
    def __init__(self, game):
        self.game = game
        self.image = pygame.image.load("assets/huds/coin_hud.png").convert_alpha()

    def updateCoinsHUD(self):
        pass

    def renderCoinsHUD(self, surf):
        surf.blit(self.image, (100, 50))
        font = pygame.font.Font("assets/Pixeltype.ttf", 32)
        text = font.render(f"{self.game.player.coins}", True, (255, 255, 0))
        surf.blit(text, (120, 50))
