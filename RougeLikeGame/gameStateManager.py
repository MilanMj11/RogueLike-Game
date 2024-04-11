import pygame
from constants import *


class GameStateManager:
    def __init__(self, game, gameState):
        self.gameState = gameState
        self.previousGameState = None
        self.game = game

    def switchGameState(self, gameState):
        self.previousGameState = self.gameState
        self.gameState = gameState

        if gameState == "Lobby":
            self.game.loadLobby()
        if gameState == "Dungeon 1":
            self.game.loadDungeon1()
        if gameState == "Dungeon 2":
            self.game.loadDungeon2()
        if gameState == "Dungeon 3":
            self.game.loadDungeon3()
