import pygame

from src.config import W, H, screen, color_black


class Background:
    def __init__(self, pos_y_1, speed, pos_x, surface):
        self.pos_x = pos_x
        self.pos_y_1 = pos_y_1
        self.speed = speed
        self.surface = pygame.transform.scale(surface, (W, H))

    def display(self):
        screen.fill(color_black)
        screen.blit(self.surface, (0, self.pos_y_1))
