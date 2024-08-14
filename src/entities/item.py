import random

import pygame

from src.config import usable_screen_height, screen, game_state, available_items


class Item:
    def __init__(self, pos_x, pos_y, speed=game_state.default_speed / 8):
        (self.type, self.surface), = random.choice(available_items).items()
        self.mask = pygame.mask.from_surface(self.surface)

        self.width, self.height = self.surface.get_size()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed
        self.pos_x = self.pos_x - self.width / 2  # align item based on the surface size

    def display(self):
        self.pos_y += self.speed
        screen.blit(self.surface, (self.pos_x, self.pos_y))

        if self.pos_y > usable_screen_height + self.height:
            game_state.items.remove(self)
