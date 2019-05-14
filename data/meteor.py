import pygame

from data.config import H, screen, default_move_speed, meteors, tiny_meteors


class Meteor:
    def __init__(self, surface, pos_x, pos_y, speed=default_move_speed / 2):
        self.surface = surface
        self.mask = pygame.mask.from_surface(self.surface)

        self.width, self.height = self.surface.get_size()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed
        self.alive = True

    def display(self):
        self.pos_y += self.speed
        if self.alive:
            screen.blit(self.surface, (self.pos_x, self.pos_y))
        else:
            screen.blit(tiny_meteors[0], (self.pos_x, self.pos_y))
            screen.blit(tiny_meteors[1], (self.pos_x + 45, self.pos_y + 30))
            screen.blit(tiny_meteors[2], (self.pos_x + 25, self.pos_y + 50))

        if self.pos_y > H + self.height:
            meteors.remove(self)

    def collide(self):
        self.alive = False

