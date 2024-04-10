'''
This is a level editor that allows the user to create levels for the game.
Rules of how this editor works are as follows:
1. Pressing 1 and 2 allows you to switch between placing a Wall / Floor tile
2. Pressing R will stylize the map ( This will place the correct tiles for walls and floors )
3. Clicking on the tilemap asset image on the right will select the image to place on the tilemap as decor
4. Clicking on the tilemap will place the selected image on the tilemap
5. Right clicking on the tilemap will delete the tile
6. Shift + Right click will delete the decor of the tile ( the decor being the img selected from the asset img)
7. Pressing 3 or 4 will rotate the selected image ( the decor image )

8. Moving through the tilemap will be done with the WASD keys
9. Pressing F will reduce the dimensions of the tilemap dynamically to the minimum size possible
   Considering all the placed tiles on the tilemap
'''

import sys
import pygame
from constants import *
from tiles import TileMap, Tile

RENDER_SCALE = 2.0

class LevelEditor:
    def __init__(self):

        pygame.init()

        self.tilemapAssetsScreen = pygame.Surface((576, 528))
        self.virtual_screen = pygame.Surface((1280, 720))
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.camera = [0, 0]
        self.render_camera = [0, 0]
        self.running = True
        self.tilemap = TileMap(150, 150)
        self.movement = [False, False, False, False]
        self.currentRotation = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ctrl = False
        self.ongrid = False

        self.selectedImage = None
        self.selectedTileType = None
        self.selectedImageAssetPosition = None

    def updateCamera(self):

        self.camera[1] += (self.movement[1] - self.movement[0]) * 8
        self.camera[0] += (self.movement[3] - self.movement[2]) * 8
        self.render_camera = [int(self.camera[0]), int(self.camera[1])]

    def update(self):
        if self.running == False:
            pygame.quit()
            quit()

        self.checkEvents()

        # update the camera position
        self.updateCamera()

        mouse_pos = pygame.mouse.get_pos()

        # if the mouse is on the tilemap
        if mouse_pos[0] > 10 and mouse_pos[0] < 10 + SCREEN_WIDTH * 2 // 3 and mouse_pos[1] > 130 and mouse_pos[
            1] < 130 + SCREEN_HEIGHT * 2 // 3:
            self.ongrid = True
            # get the tile that the mouse is on
            '''
            row = int((mouse_pos[1] - 130) / 64) + int (self.render_camera[1] / 64)
            col = int((mouse_pos[0] - 10) / 64) + int (self.render_camera[0] / 64)
            '''
            row = int((mouse_pos[1] - 130 + self.render_camera[1]) / TILESIZE)
            col = int((mouse_pos[0] - 10 + self.render_camera[0]) / TILESIZE)

            # 42.6 = 64 * (2 / 3)
            # TILESIZE * (SCALING FACTOR FOR RENDERING LEVEL EDITOR)

        else:
            self.ongrid = False

        if self.ongrid == False and self.selectedImage != None:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(self.selectedImage, mouse_pos)

        if self.ongrid == True and self.selectedImage != None:

            if self.clicking:
                if self.selectedTileType == "wall":
                    self.tilemap.setTile(row, col, "wall")
                    self.tilemap.setTileImage(row, col, self.selectedImage)
                if self.selectedTileType == "floor":
                    self.tilemap.setTile(row, col, "floor")
                    self.tilemap.setTileImage(row, col, self.selectedImage)
                if self.selectedTileType == "decor":
                    if self.tilemap.getTile(row, col) != None:
                        self.tilemap.setTileDecorImage(row, col, self.selectedImage)
                        self.tilemap.setTileDecorAssetPosition(row, col, self.selectedImageAssetPosition)
                        self.tilemap.getTile(row, col).rotation = self.currentRotation

                if self.selectedTileType == None and self.tilemap.getTile(row, col) != None:
                    self.tilemap.setTileImage(row, col, self.selectedImage)

        if self.ongrid == True:
            if self.tilemap.getTile(row, col) != None:

                # If I press shift and right click, then I delete the decor
                if self.shift == True and self.right_clicking == True:
                    self.tilemap.setTileDecorImage(row, col, None)
                    self.tilemap.setTileDecorAssetPosition(row, col, [-1, -1])

                # If I press right click but no shift, then I delete the tile
                if self.shift == False and self.right_clicking == True:
                    self.tilemap.delTile(row, col)

        self.clock.tick(60)

    def checkEvents(self):

        eventList = pygame.event.get()

        for event in eventList:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.selectedTileType = "wall"
                    self.selectedImage = pygame.image.load("assets/tilemap/wall.png").convert_alpha()
                    self.selectedImage = pygame.transform.scale(self.selectedImage, (TILESIZE, TILESIZE))
                if event.key == pygame.K_2:
                    self.selectedTileType = "floor"
                    self.selectedImage = pygame.image.load("assets/tilemap/floor.png").convert_alpha()
                    self.selectedImage = pygame.transform.scale(self.selectedImage, (TILESIZE, TILESIZE))
                if event.key == pygame.K_r:
                    self.tilemap.stylize_map()

                if event.key == pygame.K_3:
                    self.selectedImage = pygame.transform.rotate(self.selectedImage, 90)
                    self.currentRotation += 90

                if event.key == pygame.K_4:
                    self.selectedImage = pygame.transform.rotate(self.selectedImage, -90)
                    self.currentRotation -= 90

                if event.key == pygame.K_f:
                    self.tilemap.reduceDimensionsDinamically()

                if event.key == pygame.K_LSHIFT:
                    self.shift = True

                if event.key == pygame.K_LCTRL:
                    self.ctrl = True

                if event.key == pygame.K_w:
                    self.movement[0] = True
                if event.key == pygame.K_s:
                    if self.ctrl == False:
                        self.movement[1] = True
                if event.key == pygame.K_a:
                    self.movement[2] = True
                if event.key == pygame.K_d:
                    self.movement[3] = True

                # SAVING THE LEVEL WITH CTRL+S IN NEW TEXT FILE
                if self.ctrl == True and event.key == pygame.K_s:
                    self.tilemap.save("level1.txt")

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    self.shift = False

                if event.key == pygame.K_LCTRL:
                    self.ctrl = False

                if event.key == pygame.K_w:
                    self.movement[0] = False
                if event.key == pygame.K_s:
                    self.movement[1] = False
                if event.key == pygame.K_a:
                    self.movement[2] = False
                if event.key == pygame.K_d:
                    self.movement[3] = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicking = True

                if event.button == 3:
                    self.right_clicking = True

                mouse_pos = pygame.mouse.get_pos()

                # if the mouse is on the tilemapAssetsScreen
                # then we need to select the image that was clicked
                if mouse_pos[0] > 1300 and mouse_pos[0] < 1300 + 576 and mouse_pos[1] > 130 and mouse_pos[
                    1] < 130 + 528:
                    # get the 16x16 image that was clicked
                    image_x = (mouse_pos[0] - 1300) // 48
                    image_y = (mouse_pos[1] - 130) // 48
                    self.selectedImageAssetPosition = [image_x, image_y]
                    self.selectedImage = self.tilemapAssetsScreen.subsurface((image_x * 48, image_y * 48, 48, 48))
                    self.selectedImage = pygame.transform.scale(self.selectedImage, (TILESIZE, TILESIZE))
                    self.selectedImage.set_colorkey((0, 0, 0))
                    self.selectedTileType = "decor"

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.clicking = False

                if event.button == 3:
                    self.right_clicking = False

    def render(self):
        self.virtual_screen.fill((100, 100, 100))
        self.tilemap.render(self.virtual_screen, offset=self.render_camera)

        # highlight the chosen piece on the tilemap before applying it
        if self.ongrid == True and self.selectedImage != None:
            imageCopy = self.selectedImage.copy()
            imageCopy.set_alpha(100)
            mouse_pos = pygame.mouse.get_pos()
            row = int((mouse_pos[1] - 130 + self.render_camera[1]) / TILESIZE)
            col = int((mouse_pos[0] - 10 + self.render_camera[0]) / TILESIZE)
            # draw the image on the tilemap at the tile that the mouse is on
            self.virtual_screen.blit(imageCopy, (col * TILESIZE - self.render_camera[0], row * TILESIZE - self.render_camera[1]))

            # self.virtual_screen.blit(imageCopy, (col * 64, row * 64))

        # scale the virutal screen onto the actual screen
        scaledScreen = pygame.transform.scale(self.virtual_screen, (SCREEN_WIDTH * 2 // 3, SCREEN_HEIGHT * 2 // 3))
        self.screen.blit(scaledScreen, (10, 130))

        assetsImage = pygame.image.load("assets/tilemap/Tilemap/desert_tilemap_packed.png").convert_alpha()
        assetsImage = pygame.transform.scale(assetsImage, (576, 528))

        self.tilemapAssetsScreen.blit(assetsImage, (0, 0))
        self.screen.blit(self.tilemapAssetsScreen, (1300, 130))

        pygame.display.flip()
        pygame.display.update()
        self.screen.fill((0, 0, 0))

    def run(self):
        self.tilemap.load("level1.txt")

        while True:
            # self.virtual_screen.fill((100, 100, 100))

            self.render()
            self.update()


LevelEditor().run()
