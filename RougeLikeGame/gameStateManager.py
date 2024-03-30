import pygame
from constants import *


class GameStateManager:
    def __init__(self, gameState):
        self.gameState = gameState
        self.previousGameState = None

    def switchGameState(self, gameState):
        self.previousGameState = self.gameState
        self.gameState = gameState
