import pygame

from data.config import laser_blue, vel


class Laser:
    def __init__(self, surface=laser_blue, pos_x=0.0, pos_y=0.0, speed=vel*2):
        self.surface = surface
        self.mask = pygame.mask.from_surface(self.surface)

        self.width, self.height = self.surface.get_size()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed

    def __new__(cls, *args, **kwargs):
        return super(Laser, cls).__new__(cls)