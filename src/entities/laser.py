import pygame

from src.config import screen, usable_screen_height, game_state


class Laser:
    def __init__(self, surface, owner, pos_x, pos_y, speed=game_state.default_speed * 2):
        self.surface = surface
        self.mask = pygame.mask.from_surface(self.surface)
        self.owner = owner

        self.width, self.height = self.surface.get_size()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed
        self.hit = False
        self.pos_x -= (self.width / 2)  # align laser position with ship cannon, uses width variable to calculate
        game_state.lasers.append(self)

    def display(self):
        old_width = self.width
        l_width, l_height = self.surface.get_size()
        screen.blit(self.surface, (self.pos_x - l_width / 2 + old_width / 2, self.pos_y - l_height / 2))
        self.pos_y -= self.speed
        if self.pos_y <= 0 or self.hit or self.pos_y >= usable_screen_height:
            game_state.lasers.remove(self)
