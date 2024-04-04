import sys
import pygame
from constants import *
from tiles import TileMap, Tile

RENDER_SCALE = 2.0


class LevelEditor:
    def __init__(self):

        pygame.init()

        self.tilemapAssetsScreen = pygame.Surface((576, 528))
        self.virtual_screen = pygame.Surface((VIRTUALSCREEN_WIDTH, VIRTUALSCREEN_HEIGHT))
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.camera = [0, 0]
        self.render_camera = [0, 0]
        self.running = True
        self.tilemap = TileMap(50, 50)
        self.movement = [False, False, False, False]

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = False

        self.selectedImage = None

    def updateCamera(self):

        self.camera[0] += (self.movement[1] - self.movement[0]) * 2
        self.camera[1] += (self.movement[3] - self.movement[2]) * 2
        self.render_camera = [int(self.camera[0]), int(self.camera[1])]

    def update(self):
        if self.running == False:
            pygame.quit()
            quit()


        self.render()
        self.checkEvents()

        mouse_pos = pygame.mouse.get_pos()
        # if the mouse is on the tilemap
        if mouse_pos[0] > 10 and mouse_pos[0] < 10 + SCREEN_WIDTH * 2 // 3  and mouse_pos[1] > 130 and mouse_pos[1] < 130 + SCREEN_HEIGHT * 2 // 3:
            self.ongrid = True
            # get the tile that the mouse is on
            row = (mouse_pos[1] - 130) // TILESIZE
            col = (mouse_pos[0] - 10) // TILESIZE
            print("OK")
        else:
            self.ongrid = False

        if self.ongrid == False and self.selectedImage != None:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(self.selectedImage, mouse_pos)

        self.clock.tick(60)

    def checkEvents(self):

        eventList = pygame.event.get()

        for event in eventList:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicking = True

                if event.button == 3:
                    self.right_clicking = True

                mouse_pos = pygame.mouse.get_pos()
                # if the mouse is on the tilemapAssetsScreen
                # then we need to select the image that was clicked
                if mouse_pos[0] > 1300 and mouse_pos[0] < 1300 + 576 and mouse_pos[1] > 130 and mouse_pos[1] < 130 + 528:
                    # get the 16x16 image that was clicked
                    image_x = (mouse_pos[0] - 1300) // 48
                    image_y = (mouse_pos[1] - 130) // 48
                    self.selectedImage = self.tilemapAssetsScreen.subsurface((image_x * 48, image_y * 48, 48, 48))



    def render(self):

        self.tilemap.render(self.virtual_screen, offset=self.render_camera)

        # scale the virutal screen onto the actual screen
        scaledScreen = pygame.transform.scale(self.virtual_screen, (SCREEN_WIDTH * 2 // 3, SCREEN_HEIGHT * 2 // 3))
        self.screen.blit(scaledScreen, (10, 130))

        assetsImage = pygame.image.load("assets/tilemap/Tilemap/tilemap_packed.png").convert_alpha()
        assetsImage = pygame.transform.scale(assetsImage, (576, 528))

        self.tilemapAssetsScreen.blit(assetsImage, (0, 0))
        self.screen.blit(self.tilemapAssetsScreen, (1300, 130))

        pygame.display.flip()
        pygame.display.update()

    def run(self):
        while True:
            self.virtual_screen.fill((100, 100, 100))
            self.update()







LevelEditor().run()