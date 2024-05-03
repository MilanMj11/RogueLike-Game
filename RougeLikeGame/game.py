from player import Player
from tiles import *
from gameStateManager import GameStateManager
from Lobby.lobby import Lobby
from Dungeons.dungeon1 import Dungeon1
from Huds.abilities_hud import AbilitiesHud
from Huds.xp_hud import XPHUD
from Huds.health_hud import HealthHUD
from Huds.coins_hud import CoinsHUD
from menu import Menu

class GameController:
    def __init__(self):
        pygame.init()
        self.virtual_screen = pygame.Surface((VIRTUALSCREEN_WIDTH, VIRTUALSCREEN_HEIGHT))
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.gameStateManager = GameStateManager(self, "Menu")
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

        self.damage_numbers = []
        self.font = pygame.font.Font("assets/Pixeltype.ttf", 20)

        self.abilitiesHud = AbilitiesHud(self)
        self.xpHUD = XPHUD(self, self.player.experience)
        self.healthHUD = HealthHUD(self)
        self.coinsHUD = CoinsHUD(self)

        self.menu = Menu(self, "Start Menu")

    def startGame(self):
        pass
        # load the lobby as the first scene
        # self.loadDungeon1()

    def loadLobby(self):
        self.Lobby = Lobby(self)
        self.Lobby.init_Lobby()

    def loadDungeon1(self):
        self.Dungeon1 = Dungeon1(self)
        self.Dungeon1.init_Dungeon_1()

    def updatePlayer(self):
        # update the player
        self.player.update()
        '''
        FOR TESTING PURPOSES ONLY, REMOVE LATER 
        '''
        self.player.savePlayer()

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
        self.current_time = pygame.time.get_ticks()
        self.checkGameEvents()
        self.render()

    def checkGameEvents(self):

        eventList = pygame.event.get()

        if self.gameStateManager.gameState == "Menu":
            self.menu.handleEvents(eventList)

        if self.gameStateManager.gameState == "Lobby":
            self.Lobby.checkLobbyGameEvents(eventList)

        if self.gameStateManager.gameState == "Dungeon 1":
            self.Dungeon1.checkDungeon1GameEvents(eventList)

        for event in eventList:
            if event.type == pygame.QUIT:
                self.running = False

    def renderDamageNumbers(self):
        for damage in self.damage_numbers[:]:
            if damage:
                if (self.current_time - damage[2]) >= 550:
                    self.damage_numbers.remove(damage)
                    continue
                text = self.font.render(str(damage[0]), True, (255, 255, 255))
                self.virtual_screen.blit(text, (damage[1][0] - self.render_camera[0], damage[1][1] - self.render_camera[1] - 20))

    def render(self):

        # --- Rendering the correct Scene based on the gameState ---

        if self.gameStateManager.gameState == "Menu":
            self.menu.render(self.virtual_screen)

        if self.gameStateManager.gameState == "Dungeon 1":
            self.Dungeon1.renderDungeon1()

        if self.gameStateManager.gameState == "Lobby":
            self.Lobby.renderLobby()

        # --- Rendering the correct Scene based on the gameState ---

        if self.gameStateManager.gameState != "Menu":
            self.renderDamageNumbers()
            self.xpHUD.renderXPHUD(self.virtual_screen)
            self.coinsHUD.renderCoinsHUD(self.virtual_screen)

            if self.gameStateManager.gameState != "Lobby":
                self.healthHUD.renderHealthHUD(self.virtual_screen)

        # scale the virutal screen onto the actual screen
        scaledScreen = pygame.transform.scale(self.virtual_screen, (SCREEN_WIDTH, SCREEN_HEIGHT), self.screen)
        self.screen.blit(scaledScreen, (0, 0))

        pygame.display.flip()
        pygame.display.update()
