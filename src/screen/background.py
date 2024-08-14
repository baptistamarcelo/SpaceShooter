import pygame

from src.config import usable_screen_width, usable_screen_height, screen, color_black


class Background:
    def __init__(self, pos_y_1, pos_x, surface):
        self.pos_x = pos_x
        self.pos_y_1 = pos_y_1
        self.surface = pygame.transform.scale(surface, (usable_screen_width, usable_screen_height))

    def display(self):
        screen.fill(color_black)
        screen.blit(self.surface, (0, self.pos_y_1))
