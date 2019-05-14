import pygame

from data.config import W, H, screen, meteor_brown_big, default_move_speed, meteors


class Meteor:
    def __init__(self, surface=meteor_brown_big, pos_x=W/2, pos_y=-50, speed=default_move_speed / 2):
        self.surface = surface
        self.mask = pygame.mask.from_surface(self.surface)

        self.width, self.height = self.surface.get_size()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed

    def __new__(cls, *args, **kwargs):
        return super(Meteor, cls).__new__(cls)

    def display(self):
        self.pos_y += self.speed
        screen.blit(self.surface, (self.pos_x, self.pos_y))

        if self.pos_y > H + self.height:
            meteors.remove(self)
