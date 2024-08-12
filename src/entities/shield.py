import pygame

from src.config import screen, shield_1


class Shield:
    def __init__(self, owner):
        self.surface = shield_1
        self.mask = pygame.mask.from_surface(self.surface)
        self.width, self.height = self.surface.get_size()
        self.owner = owner

    def display(self):
        pos_x = self.owner.pos_x - self.owner.width / 6
        pos_y = self.owner.pos_y - self.owner.height / 3

        screen.blit(self.surface, (pos_x, pos_y))
