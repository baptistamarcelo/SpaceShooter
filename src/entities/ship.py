import pygame

from src.config import W, H, ship_blue, screen, game_state


class Ship:
    def __init__(self, surface=ship_blue, pos_x=W/2, pos_y=H/1.5, speed=game_state.default_speed):
        self.surface = surface
        self.mask = pygame.mask.from_surface(self.surface)

        self.width, self.height = self.surface.get_size()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed

    def display(self):
        screen.blit(self.surface, (self.pos_x, self.pos_y))
