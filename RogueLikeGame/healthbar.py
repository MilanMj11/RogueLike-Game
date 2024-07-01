import pygame


class HealthBar:
    def __init__(self, health, maxHealth, position, entitySize=(40, 40)):
        self.health = health
        self.maxHealth = maxHealth
        self.position = position
        self.entitySize = entitySize

    def update(self, health):
        self.health = health

    def render(self, screen, offset=(0, 0)):
        # draw the healthbar above the enemy with the same length as the entity

        health_bar_x = self.position[0] - offset[0]
        health_bar_y = self.position[1] - offset[1] - 10
        health_bar_width = self.entitySize[0]
        health_bar_height = 4

        # draw the health bar background
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

        # calculate the width of the health bar based on the entity's health
        health_bar_current_width = int(health_bar_width * (self.health / self.maxHealth))

        # draw the health bar with the current health
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, health_bar_current_width, health_bar_height))


