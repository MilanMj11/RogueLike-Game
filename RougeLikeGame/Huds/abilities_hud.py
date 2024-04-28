import pygame
from constants import *
class AbilitiesHud:
    def __init__(self, game):
        self.game = game

        self.HUD_SURF = pygame.Surface((ABILITIES_HUD_WIDTH, ABILITIES_HUD_HEIGHT), pygame.SRCALPHA)
        self.timer_surface = pygame.Surface((ABILITIES_HUD_WIDTH, ABILITIES_HUD_HEIGHT), pygame.SRCALPHA)

        self.image = pygame.image.load("assets/huds/abilities_hud.png").convert_alpha()
        self.image.set_colorkey((100, 100, 100))

        self.abilitiesImages = [pygame.image.load("assets/abilities/fireBallAbilityImage.png").convert_alpha(),
                                pygame.image.load("assets/abilities/swordAbilityImage.png").convert_alpha(),
                                pygame.image.load("assets/abilities/unknownAbilityImage.png").convert_alpha(),
                                pygame.image.load("assets/abilities/unknownAbilityImage.png").convert_alpha()]

        self.abilitiesTimerSquares = [[32,0],[32,0],[32,0],[32,0]]

        self.scaleAbilitiesImages()

    def scaleAbilitiesImages(self):
        for i in range(self.abilitiesImages.__len__()):
            scaled_image = pygame.transform.scale(self.abilitiesImages[i], (32, 32))
            self.abilitiesImages[i] = scaled_image

    def updateAbilitiesHud(self, current_time):
        # Ability 1 = projectile ->
        if current_time - self.game.player.last_projectile_time >= 1000 / self.game.player.attackSpeed:
            self.abilitiesTimerSquares[0][1] = 0
        else:
            self.abilitiesTimerSquares[0][1] = 32 - (32 * (current_time - self.game.player.last_projectile_time) / (1000 / self.game.player.attackSpeed))

        # Ability 2 = melee attack ->
        if current_time - self.game.player.last_melee_attack_time >= 1000 / self.game.player.attackSpeed:
            self.abilitiesTimerSquares[1][1] = 0
        else:
            self.abilitiesTimerSquares[1][1] = 32 - (32 * (current_time - self.game.player.last_melee_attack_time) / (1000 / self.game.player.attackSpeed))



    def renderAbilitiesHud(self, surf):

        self.HUD_SURF.blit(self.image, (0, 0))

        # I have 4 abilities , 2 which are leftclick and rightclick , the others 2 are "swappable" for later
        for i in range(self.abilitiesImages.__len__()):
            self.HUD_SURF.blit(self.abilitiesImages[i], (10 * (i + 1) + i * 32, 10))


        # Here I want to draw the timer squares over the abilities with transparency
        self.timer_surface.fill((0, 0, 0, 0))

        # Drawing the timer squares over the abilities with transparency
        for i in range(self.abilitiesTimerSquares.__len__()):
            pygame.draw.rect(self.timer_surface, (255, 255, 255, 128),
                             (10 * (i + 1) + i * 32, 10, 32, self.abilitiesTimerSquares[i][1]))

        self.HUD_SURF.blit(self.timer_surface, (0, 0))

        '''
        # Drawing the timer squares over the abilities with transparency
        for i in range(self.abilitiesTimerSquares.__len__()):
            pygame.draw.rect(self.HUD_SURF, (255, 255, 255, 128), (10 * (i + 1) + i * 32, 10, 32, self.abilitiesTimerSquares[i][1]))
        '''

        surf.blit(self.HUD_SURF, (surf.get_width()/2 - self.image.get_width()/2, 504))