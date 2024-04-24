import pygame

class AbilitiesHud:
    def __init__(self, game):
        self.game = game
        self.image = pygame.image.load("assets/abilities_hud.png").convert_alpha()
        self.image.set_colorkey((100, 100, 100))


    def updateAbilitiesHud(self):
        pass

    def renderAbilitiesHud(self, surf):
        surf.blit(self.image, (surf.get_width()/2 - self.image.get_width()/2, 504))