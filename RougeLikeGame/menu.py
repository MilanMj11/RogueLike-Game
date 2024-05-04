import pygame
from constants import *

SCALING_FACTOR = SCREEN_WIDTH / VIRTUALSCREEN_WIDTH
class Menu:
    def __init__(self, game, type):
        self.type = type
        self.game = game
        self.image = None
        self.loadMenu()

    def changeType(self, type):
        self.type = type
        self.loadMenu()

    def loadMenu(self):
        if self.type == "Start Menu":
            self.image = pygame.image.load("assets/menus/StartMenuExample.png")
        if self.type == "Pause Menu":
            self.image = pygame.image.load("assets/menus/PauseMenuExample.png")

    def handleEvents(self, eventList):
        if self.type == "Start Menu":
            for event in eventList:
                # if clicking on Continue button
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if 338 < int(event.pos[0]/SCALING_FACTOR) < 676 and 214 < int(event.pos[1]/SCALING_FACTOR) < 268:
                        # self.game.renderLoadingScreen()
                        self.game.gameStateManager.switchGameState("Lobby")
        if self.type == "Pause Menu":
            for event in eventList:
                # if clicking Escape again brings u back to the dungeon
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game.gameStateManager.gameState = self.game.gameStateManager.previousGameState

    def update(self):
        pass

    def render(self, surf):
        surf.blit(self.image, (0, 0))