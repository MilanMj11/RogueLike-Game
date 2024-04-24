import pygame
class XP:
    def __init__(self, xp = 0, level = 1):
        self.xp = xp
        self.level = level

    def add_xp(self, xp):
        self.xp += xp
        if self.xp >= self.level * 100:
            self.level += 1
            self.xp = 0
            # print(f"Level up! You are now level {self.level}")


class XPHUD:
    def __init__(self, game, xpCls = XP()):
        self.game = game
        self.xp = xpCls
        self.font = pygame.font.Font("assets/Pixeltype.ttf", 50)
        self.text = self.font.render(f"Level: {self.xp.level}   XP: {self.xp.xp}", True, (255, 255, 255))

    def updateXPHUD(self):
        self.text = self.font.render(f"Level: {self.xp.level}   XP: {self.xp.xp}", True, (255, 255, 255))

    def renderXPHUD(self, surf):
        surf.blit(self.text, (40, surf.get_height() - surf.get_height()/16))