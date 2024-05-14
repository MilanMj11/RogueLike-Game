import json
import math
import time
import pygame

import game
from constants import *
from projectile import Projectile
from xp import *

NEIGHBOURS_OFFSET = [[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]]
NEIGHBOURS_OFFSET_4 = [[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1]]


class Player(pygame.sprite.Sprite):  # Inherit from pygame.sprite.Sprite
    def __init__(self, game, pos, size=(40, 40)):
        super().__init__()
        # Animation frames
        self.animation_frames = [
            pygame.transform.scale(pygame.image.load("assets/player/frame_1.png").convert_alpha(), size),
            pygame.transform.scale(pygame.image.load("assets/player/frame_2.png").convert_alpha(), size),
            pygame.transform.scale(pygame.image.load("assets/player/frame_3.png").convert_alpha(), size)
        ]
        # Animation variables
        self.current_frame = 0
        self.frame_delay = 350
        self.last_frame_time = 0

        self.image = self.animation_frames[self.current_frame]
        self.image.set_colorkey((100, 100, 100))
        self.size = size
        self.position = list(pos)
        self.facing = "RIGHT"
        self.game = game
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.speed = PLAYER_SPEED
        self.attackSpeed = PLAYER_ATTACK_SPEED

        self.projectileImageFile = "assets/projectile.png"
        self.initProjectileImage()
        self.last_projectile_time = 0

        self.melee_range = 70
        self.melee_damage = 15
        self.last_melee_attack_time = 0
        self.swing_animation_duration = 20
        self.swing_animation_timer = 0

        # Swing animation variables
        self.swing_current_frame = 0
        self.swing_frame_delay = 50
        self.swing_last_frame_time = 0
        self.swing_angle = -60

        self.attacked = False
        self.swinging = False
        self.attackDirection = [0, 0]

        self.projectileSpeed = 6
        self.projectileDamage = 10

        self.experience = XP()
        self.coins = 0

    def savePlayer(self):
        directory = 'Saves/'
        file = open(directory + 'save1.json', 'w')

        data = {}
        data['MAX HEALTH'] = self.max_health
        data['SPEED'] = self.speed
        data['ATTACK SPEED'] = self.attackSpeed
        data['XP'] = self.experience.to_json()
        data['PROJECTILE'] = {"SPEED": self.projectileSpeed, "DAMAGE": self.projectileDamage,
                              "IMAGE_FILE": self.projectileImageFile}
        data['MELEE'] = {"RANGE": self.melee_range, "DAMAGE": self.melee_damage}
        data['COINS'] = self.coins

        json_data = json.dumps(data, indent=4)

        file.write(json_data)

    def loadPlayer(self):
        directory = 'Saves/'
        file = open(directory + 'save1.json', 'r')
        data = json.load(file)

        self.max_health = data['MAX HEALTH']
        self.health = self.max_health
        self.speed = data['SPEED']
        self.attackSpeed = data['ATTACK SPEED']
        self.experience.xp = data['XP']['xp']
        self.experience.level = data['XP']['level']
        self.coins = data['COINS']

        self.projectileSpeed = data['PROJECTILE']['SPEED']
        self.projectileDamage = data['PROJECTILE']['DAMAGE']
        self.projectileImageFile = data['PROJECTILE']['IMAGE_FILE']

        self.melee_range = data['MELEE']['RANGE']
        self.melee_damage = data['MELEE']['DAMAGE']

    def loadNewPlayer(self):

        self.max_health = 100
        self.health = self.max_health
        self.speed = PLAYER_SPEED
        self.attackSpeed = PLAYER_ATTACK_SPEED
        self.experience.xp = 0
        self.experience.level = 1
        self.coins = 0

        self.projectileSpeed = 6
        self.projectileDamage = 10
        self.projectileImageFile = "assets/projectile.png"

        self.melee_range = 70
        self.melee_damage = 15

    def getTile(self):
        return self.game.tilemap.getTile(int((self.position[1] + self.size[1] / 2) / TILESIZE),
                                         int((self.position[0] + self.size[0] / 2) / TILESIZE))

    def getTileCoords(self):
        currentTile = self.getTile()
        return (currentTile.row, currentTile.col)

    def getRectMiddlePoint(self):
        return (self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2)

    def update_animation(self, current_time):
        # Update the animation frame
        if current_time - self.last_frame_time > self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.current_frame]
            self.last_frame_time = current_time

    def initProjectileImage(self):
        self.projectileImage = pygame.image.load(self.projectileImageFile).convert_alpha()
        self.projectileImage = pygame.transform.scale(self.projectileImage, (32, 32))
        self.projectileImage.set_colorkey((100, 100, 100))

    def getRect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def getTilesAroundClose(self):
        # get the tiles around the player
        tiles = []
        # playerTile to be the tile where the player is standing with it's center
        playerTile = self.game.tilemap.getTile(int((self.position[1] + self.size[1] / 2) / TILESIZE),
                                               int((self.position[0] + self.size[0] / 2) / TILESIZE))

        for offset in NEIGHBOURS_OFFSET:
            row = playerTile.row + offset[0]
            col = playerTile.col + offset[1]
            if row >= 0 and row < self.game.tilemap.height and col >= 0 and col < self.game.tilemap.width:
                tiles.append(self.game.tilemap.getTile(row, col))
        return tiles

    def getTilesAround(self):
        # get the tiles around the player
        tiles = []
        playerTile = self.game.tilemap.getTile(int(self.position[1] / TILESIZE), int(self.position[0] / TILESIZE))
        for offset in NEIGHBOURS_OFFSET:
            row = playerTile.row + offset[0]
            col = playerTile.col + offset[1]
            if row >= 0 and row < self.game.tilemap.height and col >= 0 and col < self.game.tilemap.width:
                tiles.append(self.game.tilemap.getTile(row, col))
        return tiles

    def getTilesAround4(self):
        tiles = []
        playerTile = self.game.tilemap.getTile(int(self.position[1] / TILESIZE), int(self.position[0] / TILESIZE))
        for offset in NEIGHBOURS_OFFSET_4:
            row = playerTile.row + offset[0]
            col = playerTile.col + offset[1]
            if row >= 0 and row < self.game.tilemap.height and col >= 0 and col < self.game.tilemap.width:
                tiles.append(self.game.tilemap.getTile(row, col))
        return tiles

    def update_AttackDirection(self, mousePos):
        self.attackDirection = mousePos

    def damageEnemiesInSwingArea(self, attackDirection):

        # get the direction of the meele attack
        playerPos = SCREEN_WIDTH / 2 + self.size[0], SCREEN_HEIGHT / 2 + self.size[1]

        direction = [attackDirection[0] - playerPos[0] + self.size[0], attackDirection[1] - playerPos[1] + self.size[1]]
        length = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
        normalized_vector = [direction[0] / length, direction[1] / length]

        attack_direction = math.atan2(normalized_vector[1], normalized_vector[0])

        # Iterate through each enemy
        for enemy in self.game.enemiesList:

            # Calculate distance between player and enemy
            distance = math.sqrt((enemy.getRectMiddlePoint()[0] - self.getRectMiddlePoint()[0]) ** 2 + (
                    enemy.getRectMiddlePoint()[1] - self.getRectMiddlePoint()[1]) ** 2) - enemy.size[0] / 2

            # Calculate angle between player and enemy
            enemy_direction = math.atan2(enemy.getRectMiddlePoint()[1] - self.getRectMiddlePoint()[1],
                                         enemy.getRectMiddlePoint()[0] - self.getRectMiddlePoint()[0])

            # Calculate the difference between the enemy's direction and the attack direction
            angle_difference = abs(math.atan2(math.sin(enemy_direction - attack_direction),
                                              math.cos(enemy_direction - attack_direction)))

            # Check if the enemy is within melee range and within the attack arc
            if distance <= self.melee_range and angle_difference <= math.pi / 3:
                # Apply damage to the enemy
                if enemy.gotAttacked == False:
                    enemy.getDamaged(self.melee_damage)

    def meeleAttack(self):
        if pygame.mouse.get_pressed()[2]:
            mousePos = pygame.mouse.get_pos()

            self.update_AttackDirection(mousePos)

            # get the direction of the meele attack
            playerPos = SCREEN_WIDTH / 2 + self.size[0], SCREEN_HEIGHT / 2 + self.size[1]

            direction = [mousePos[0] - playerPos[0] + self.size[0], mousePos[1] - playerPos[1] + self.size[1]]
            length = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
            normalized_vector = [direction[0] / length, direction[1] / length]

            self.swinging = True
            self.swing_animation_timer = self.swing_animation_duration
            self.sword_angle = 0

            return True

        return False

    def draw_sword_animation(self, mouse_pos, screen, offset=(0, 0)):
        if self.swinging:

            playerPos = SCREEN_WIDTH / 2 + self.size[0], SCREEN_HEIGHT / 2 + self.size[1]

            direction_vector = [mouse_pos[0] - playerPos[0] + self.size[0], mouse_pos[1] - playerPos[1] + self.size[1]]
            length = math.sqrt(direction_vector[0] ** 2 + direction_vector[1] ** 2)
            normalized_vector = [direction_vector[0] / length, direction_vector[1] / length]

            angle = math.atan2(normalized_vector[1], normalized_vector[0])

            swing_angle_rad = math.radians(self.swing_angle)

            rotated_vector = [math.cos(angle + swing_angle_rad), math.sin(angle + swing_angle_rad)]

            end_position = [self.position[0] + self.size[0] / 2 + rotated_vector[0] * self.melee_range,
                            self.position[1] + self.size[1] / 2 + rotated_vector[1] * self.melee_range]

            pygame.draw.line(screen, WHITE, (
                self.position[0] + self.size[0] / 2 - offset[0], self.position[1] + self.size[1] / 2 - offset[1]),
                             (end_position[0] - offset[0], end_position[1] - offset[1]), 10)

            self.swing_angle += 8

            if self.swing_angle > 60:
                self.swinging = False
                self.swing_angle = -60

    def draw_swing_area(self, mouse_pos, screen, offset=(0, 0)):
        if self.swinging:
            playerPos = SCREEN_WIDTH / 2 + self.size[0], SCREEN_HEIGHT / 2 + self.size[1]

            direction_vector = [mouse_pos[0] - playerPos[0] + self.size[0], mouse_pos[1] - playerPos[1] + self.size[1]]
            length = math.sqrt(direction_vector[0] ** 2 + direction_vector[1] ** 2)
            normalized_vector = [direction_vector[0] / length, direction_vector[1] / length]

            angle = math.atan2(normalized_vector[1], normalized_vector[0])

            for swing_angle in range(-60, 61, 2):
                # convert swing angle to radians
                swing_angle_rad = math.radians(swing_angle)
                # calculate the rotated direction vector
                rotated_vector = [math.cos(angle + swing_angle_rad), math.sin(angle + swing_angle_rad)]
                # calculate the position of the swing animation
                end_position = [self.position[0] + self.size[0] / 2 + rotated_vector[0] * self.melee_range,
                                self.position[1] + self.size[1] / 2 + rotated_vector[1] * self.melee_range]

                # draw the line:
                pygame.draw.line(screen, (255, 0, 0), (
                    self.position[0] + self.size[0] / 2 - offset[0], self.position[1] + self.size[1] / 2 - offset[1]),
                                 (end_position[0] - offset[0], end_position[1] - offset[1]), 5)

            # update the swing animation timer
            self.swing_animation_timer -= 1
            if self.swing_animation_timer <= 0:
                self.swinging = False

    def shootProjectile(self):
        if pygame.mouse.get_pressed()[0]:
            mousePos = pygame.mouse.get_pos()

            # get the direction of the projectile
            playerPos = SCREEN_WIDTH / 2 + self.size[0], SCREEN_HEIGHT / 2 + self.size[1]

            direction = [mousePos[0] - playerPos[0] + self.size[0], mousePos[1] - playerPos[1] + self.size[1]]
            length = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
            direction = [direction[0] / length, direction[1] / length]

            projectile = Projectile(self.game, self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2,
                                    direction, self.projectileSpeed, self.projectileDamage)

            projectile.setImage(self.projectileImage)
            self.game.projectiles.append(projectile)
            return True
        return False

    def movePlayer(self, movement):
        tilesAround = self.getTilesAround()

        # check collisions with walls
        self.position[0] += movement[0]
        playerRect = self.getRect()
        for tile in tilesAround:
            if tile.type == "wall":
                tileRect = tile.getRect()
                if playerRect.colliderect(tileRect):
                    # collided on the x axes
                    if movement[0] > 0.0:
                        playerRect.right = tileRect.left
                    if movement[0] < 0.0:
                        playerRect.left = tileRect.right

                    self.position[0] = playerRect.x

        self.position[1] += movement[1]
        playerRect = self.getRect()
        for tile in tilesAround:
            if tile.type == "wall":
                tileRect = tile.getRect()
                if playerRect.colliderect(tileRect):
                    # collided on the y axes
                    if movement[1] > 0.0:
                        playerRect.bottom = tileRect.top
                    if movement[1] < 0.0:
                        playerRect.top = tileRect.bottom

                    self.position[1] = playerRect.y

    def showInteractionsAvailable(self):
        interactionButton = pygame.image.load("assets/interactionButtonE.png").convert_alpha()
        interactionButton = pygame.transform.scale(interactionButton, (16, 16))


        if "Dungeon" in self.game.gameStateManager.gameState:
            tilesAround = self.getTilesAroundClose()
            for tile in tilesAround:
                if tile.decorAssetPosition in [[10, 3], [11, 3], [5, 7], [7, 9], [0, 5], [10, 2], [11, 2]]:
                    position_x = tile.col * TILESIZE + TILESIZE / 2 - interactionButton.get_width() / 2
                    position_y = tile.row * TILESIZE - 12
                    self.game.virtual_screen.blit(interactionButton, (
                        position_x - self.game.render_camera[0], position_y - self.game.render_camera[1]))

    def update(self, current_time):

        ''' For testing , print the player tile coords '''
        print(self.getTile().row, self.getTile().col)

        # I only want to shoot depending on the self.attackSpeed, every 1 / self.attackSpeed seconds

        if self.game.gameStateManager.gameState != "Lobby":

            self.game.abilitiesHud.updateAbilitiesHud(current_time)

            if current_time - self.last_projectile_time >= 1000 / self.attackSpeed:
                if self.shootProjectile():
                    self.last_projectile_time = current_time

            if current_time - self.last_melee_attack_time >= 1000 / self.attackSpeed:
                if self.meeleAttack():
                    self.last_melee_attack_time = current_time

            ''' If the player is not swinging the sword, then all the enemies will have their got attacked status reset'''
            if self.swinging == False:
                for enemy in self.game.enemiesList:
                    enemy.gotAttacked = False

            ''' If the player is swinging the sword, then I will damage all the enemies in the swing area '''
            if self.swinging == True:
                self.damageEnemiesInSwingArea(self.attackDirection)

        self.update_animation(current_time)

        MOVEMENT_DIVISION_FACTOR = 1
        movement = self.getDirectionInput()
        divided_movement = movement[0] / MOVEMENT_DIVISION_FACTOR, movement[1] / MOVEMENT_DIVISION_FACTOR

        for i in range(MOVEMENT_DIVISION_FACTOR):
            self.movePlayer(divided_movement)

    def handleEvents(self, eventList):
        for event in eventList:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    tilesAround = self.getTilesAround()
                    for tile in tilesAround:

                        # Here we check if the player is next to the chest, so he can open it
                        if tile.decorAssetPosition == [5, 7]:
                            self.coins += 100
                            tile.updateDecorAssetPosition([7, 7], self.game.tilemap.tilemap_type)
                        # Here we check if the player collects a health potion
                        if tile.decorAssetPosition == [7, 9]:
                            # Player can drink potion only if he is not at full health
                            if self.health < self.max_health:
                                self.health += int(self.max_health * 0.2)
                                if self.health > self.max_health:
                                    self.health = self.max_health
                                tile.updateDecorAssetPosition([-1, -1], self.game.tilemap.tilemap_type)

    def getDirectionInput(self):
        keys = pygame.key.get_pressed()
        movement = [0, 0]

        if keys[pygame.K_w]:
            movement[1] -= self.speed
        if keys[pygame.K_s]:
            movement[1] += self.speed
        if keys[pygame.K_a]:
            movement[0] -= self.speed
            self.facing = "LEFT"
        if keys[pygame.K_d]:
            movement[0] += self.speed
            self.facing = "RIGHT"

        if movement[0] != 0.0 and movement[1] != 0.0:
            movement[0] *= 0.70
            movement[1] *= 0.70

        return movement

    def render(self, screen, offset=(0, 0)):

        self.draw_sword_animation(self.attackDirection, self.game.virtual_screen, offset=self.game.render_camera)
        # self.draw_swing_area(self.attackDirection, self.game.virtual_screen, offset=self.game.render_camera)
        # self.draw_swing_area(self.attackDirection, self.game.virtual_screen, offset=self.game.render_camera)

        if self.facing == "LEFT":
            flippedImage = pygame.transform.flip(self.image, True, False)
            flippedImage.set_colorkey((100, 100, 100))
            screen.blit(flippedImage, (self.position[0] - offset[0], self.position[1] - offset[1]))
        else:
            screen.blit(self.image, (self.position[0] - offset[0], self.position[1] - offset[1]))

        self.showInteractionsAvailable()
