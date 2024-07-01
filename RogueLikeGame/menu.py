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
            self.image = pygame.image.load("assets/menus/startMenu/StartMenuImage.png")
        if self.type == "Pause Menu Dungeon":
            self.image = pygame.image.load("assets/menus/PauseMenuDungeon.png")
        if self.type == "Pause Menu Lobby":
            self.image = pygame.image.load("assets/menus/PauseMenuLobby.png")

    def handleEvents(self, eventList):
        if self.type == "Start Menu":
            for event in eventList:
                # if clicking on Continue button
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if 48 < int(event.pos[0]/SCALING_FACTOR) < 371 and 196 < int(event.pos[1]/SCALING_FACTOR) < 274:
                        # CONTINUE BUTTON -> Loads the last save.
                        self.game.loadGame()
                        self.game.gameStateManager.switchGameState("Lobby")
                    if 48 < int(event.pos[0]/SCALING_FACTOR) < 371 and 300 < int(event.pos[1]/SCALING_FACTOR) < 382:
                        # NEW GAME BUTTON -> Loads new run.
                        self.game.loadNewGame()
                        self.game.gameStateManager.switchGameState("Lobby")
                    if 48 < int(event.pos[0]/SCALING_FACTOR) < 371 and 406 < int(event.pos[1]/SCALING_FACTOR) < 488:
                        # QUIT BUTTON -> Quits the game.
                        pygame.quit()

        if self.type == "Pause Menu Dungeon":
            for event in eventList:
                # if clicking Escape again brings u back to the dungeon
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game.gameStateManager.gameState = self.game.gameStateManager.previousGameState
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if 306 < int(event.pos[0]/SCALING_FACTOR) < 710 and 42 < int(event.pos[1]/SCALING_FACTOR) < 130:
                        # Resume button
                        self.game.gameStateManager.gameState = self.game.gameStateManager.previousGameState
                    if 306 < int(event.pos[0]/SCALING_FACTOR) < 710 and 178 < int(event.pos[1]/SCALING_FACTOR) < 264:
                        # Restart button
                        # reload the player.
                        self.game.player.loadPlayer()
                        self.game.gameStateManager.switchGameState(self.game.gameStateManager.previousGameState)
                    if 306 < int(event.pos[0]/SCALING_FACTOR) < 710 and 313 < int(event.pos[1]/SCALING_FACTOR) < 400:
                        # Settings button
                        pass
                    if 306 < int(event.pos[0]/SCALING_FACTOR) < 710 and 447 < int(event.pos[1]/SCALING_FACTOR) < 535:
                        # Exit button
                        # -> Don't save the player.
                        self.game.player.loadPlayer()
                        self.game.gameStateManager.switchGameState("Lobby")


        if self.type == "Pause Menu Lobby":
            for event in eventList:
                # if clicking Escape again brings u back to the lobby
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game.gameStateManager.gameState = self.game.gameStateManager.previousGameState
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if 313 < int(event.pos[0]/SCALING_FACTOR) < 714 and 89 < int(event.pos[1]/SCALING_FACTOR) < 235:
                        # Continue button
                        self.game.gameStateManager.gameState = self.game.gameStateManager.previousGameState
                    if 313 < int(event.pos[0]/SCALING_FACTOR) < 714 and 340 < int(event.pos[1]/SCALING_FACTOR) < 487:
                        # self.game.renderLoadingScreen()
                        # Save & Exit button
                        self.game.saveGame()
                        self.game.gameStateManager.switchGameState("Menu", "Start Menu")

    def updateStartMenu(self):
        mouse_pos = pygame.mouse.get_pos()
        if 48 < int(mouse_pos[0] / SCALING_FACTOR) < 371 and 196 < int(mouse_pos[1] / SCALING_FACTOR) < 274:
            self.image = pygame.image.load("assets/menus/startMenu/StartMenuImageSelectContinue.png")
        elif 48 < int(mouse_pos[0] / SCALING_FACTOR) < 371 and 300 < int(mouse_pos[1] / SCALING_FACTOR) < 382:
            self.image = pygame.image.load("assets/menus/startMenu/StartMenuImageSelectNewGame.png")
        elif 48 < int(mouse_pos[0] / SCALING_FACTOR) < 371 and 406 < int(mouse_pos[1] / SCALING_FACTOR) < 488:
            self.image = pygame.image.load("assets/menus/startMenu/StartMenuImageSelectQuit.png")
        elif 653 < int(mouse_pos[0] / SCALING_FACTOR) < 981 and 406 < int(mouse_pos[1] / SCALING_FACTOR) < 488:
            self.image = pygame.image.load("assets/menus/startMenu/StartMenuImageSelectSettings.png")
        else:
            self.image = pygame.image.load("assets/menus/startMenu/StartMenuImage.png")

    def update(self):
        if self.type == "Start Menu":
            self.updateStartMenu()


    def render(self, surf):
        surf.blit(self.image, (0, 0))