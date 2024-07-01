from xp import XP
import pygame

class XPHUD:
    def __init__(self, game, xpCls=XP()):
        self.game = game
        self.xp = xpCls

        self.xpHUD = pygame.Surface((200, 50), pygame.SRCALPHA)

        self.Levelfont = pygame.font.Font("assets/Pixeltype.ttf", 32)
        self.XPfont = pygame.font.Font("assets/Pixeltype.ttf", 26)
        self.Level_text = self.Levelfont.render(f"Lv: {self.xp.level}", True, (255, 255, 255))
        self.XP_text = self.XPfont.render(f"XP: {self.xp.xp}", True, (255, 255, 255))
        self.image = pygame.image.load("assets/huds/xp_hud.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 1.7, self.image.get_height() * 1.7))
        # (180,49,231)
        self.BarSize = [205, 26]
        self.xp_bar = pygame.rect.Rect((80, 20, self.BarSize[0], self.BarSize[1]))
        self.background_bar = pygame.rect.Rect((80, 20, self.BarSize[0], self.BarSize[1]))

    def updateXPHUD(self):
        self.Level_text = self.Levelfont.render(f"Lv: {self.xp.level}", True, (255, 255, 255))
        self.XP_text = self.XPfont.render(f"XP: {self.xp.xp}", True, (255, 255, 255))
        if self.xp.level >= 100:
            self.Levelfont = pygame.font.Font("assets/Pixeltype.ttf", 26)

        self.xp_bar.width = self.xp.xp * 205 / (self.xp.level * 100)
        self.background_bar.width = 205

    def renderXPHUD(self, surf):
        pygame.draw.rect(surf, (68, 13, 90), self.background_bar)
        pygame.draw.rect(surf, (58, 203, 255), self.xp_bar)

        surf.blit(self.image, (-15, -5))
        surf.blit(self.Level_text, (30, 42))
        surf.blit(self.XP_text, (162, 26))
