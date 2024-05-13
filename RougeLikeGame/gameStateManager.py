import threading

import pygame
from constants import *


class GameStateManager:
    def __init__(self, game, gameState):
        self.gameState = gameState
        self.previousGameState = None
        self.game = game

    def switchGameState(self, gameState, menuType=None):
        self.previousGameState = self.gameState
        self.gameState = gameState

        if gameState == "Menu":
            if menuType == "Start Menu":
                self.game.menu.changeType("Start Menu")
            if menuType == "Pause Menu Dungeon":
                self.game.menu.changeType("Pause Menu Dungeon")
            if menuType == "Pause Menu Lobby":
                self.game.menu.changeType("Pause Menu Lobby")

        # exit_flag = threading.Event()

        # thread1 = threading.Thread(target=self.game.renderLoadingScreen())

        self.game.renderLoadingScreen()

        if gameState == "Lobby":
            self.game.loadLobby()
        if gameState == "Dungeon 1":
            self.game.loadDungeon1()
        if gameState == "Dungeon 2":
            self.game.loadDungeon2()
        if gameState == "Dungeon 3":
            self.game.loadDungeon3()

