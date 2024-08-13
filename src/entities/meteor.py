import pygame

from src.config import H, screen, default_move_speed, game_state


class Meteor:
    def __init__(self, surface, pos_x, pos_y, speed=default_move_speed / 5):
        self.surface = surface
        self.mask = pygame.mask.from_surface(self.surface)

        self.width, self.height = self.surface.get_size()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed

    def display(self):
        self.pos_y += self.speed
        screen.blit(self.surface, (self.pos_x, self.pos_y))

        if self.pos_y > H + self.height:
            game_state.meteors.remove(self)
