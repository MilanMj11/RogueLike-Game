from player import Player
from tiles import *
from gameStateManager import GameStateManager
from Lobby.lobby import Lobby
from Dungeons.dungeon1 import Dungeon1


class GameController:
    def __init__(self):
        pygame.init()
        self.virtual_screen = pygame.Surface((VIRTUALSCREEN_WIDTH, VIRTUALSCREEN_HEIGHT))
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.gameStateManager = GameStateManager(self, "Dungeon 1")
        self.running = True
        self.camera = [0, 0]
        self.render_camera = [0, 0]

        self.background = pygame.Surface((VIRTUALSCREEN_WIDTH, VIRTUALSCREEN_HEIGHT))
        self.background.fill((0, 0, 0))

        self.tilemap = None
        self.player = Player(self, (9 * TILESIZE, 8 * TILESIZE))
        self.projectiles = []
        # Scenes
        self.Lobby = None
        self.Dungeon1 = None

    def startGame(self):
        # load the lobby as the first scene
        self.loadDungeon1()

    def loadLobby(self):
        self.Lobby = Lobby(self)
        self.Lobby.init_Lobby()
        self.player.health = PLAYER_HEALTH

    def loadDungeon1(self):
        self.Dungeon1 = Dungeon1(self)
        self.Dungeon1.init_Dungeon_1()
        self.player.health = PLAYER_HEALTH

    def updatePlayer(self):
        # update the player
        self.player.update()

    def updateProjectiles(self):
        # update each projectile present in the game
        for projectile in self.projectiles:
            projectile.update()

    def updateCamera(self):

        current_fps = self.clock.get_fps()
        if current_fps < 1:
            current_fps = FPS

        # camera follows the player with a smooth effect , MIGHT CHANGE VALUES LATER
        self.camera[0] += (self.player.position[0] - self.camera[0] - VIRTUALSCREEN_WIDTH / 2 + self.player.size[
            0] / 2) / CAMERA_FOLLOW_RATE / current_fps * FPS
        self.camera[1] += (self.player.position[1] - self.camera[1] - VIRTUALSCREEN_HEIGHT / 2 + self.player.size[
            1] / 2) / CAMERA_FOLLOW_RATE / current_fps * FPS
        self.render_camera = [(self.camera[0]), (self.camera[1])]

    def update(self):

        if self.running == False:
            pygame.quit()
            quit()

        if self.gameStateManager.gameState == "Dungeon 1":
            self.Dungeon1.updateDungeon1()

        if self.gameStateManager.gameState == "Lobby":
            self.Lobby.updateLobby()

        self.clock.tick(FPS)
        self.checkGameEvents()
        self.render()

    def checkGameEvents(self):

        eventList = pygame.event.get()

        if self.gameStateManager.gameState == "Lobby":
            self.Lobby.checkLobbyGameEvents(eventList)

        if self.gameStateManager.gameState == "Dungeon 1":
            self.Dungeon1.checkDungeon1GameEvents(eventList)

        for event in eventList:
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):

        # --- Rendering the correct Scene based on the gameState ---

        if self.gameStateManager.gameState == "Dungeon 1":
            self.Dungeon1.renderDungeon1()

        if self.gameStateManager.gameState == "Lobby":
            self.Lobby.renderLobby()

        # --- Rendering the correct Scene based on the gameState ---

        # scale the virutal screen onto the actual screen
        scaledScreen = pygame.transform.scale(self.virtual_screen, (SCREEN_WIDTH, SCREEN_HEIGHT), self.screen)
        self.screen.blit(scaledScreen, (0, 0))

        pygame.display.flip()
        pygame.display.update()
