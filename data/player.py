import pygame

from data.config import screen, H, W, color_white, ship_orange, ship_blue


class Player:
    def __init__(self, name, ship):
        self.name = name
        self.ship = ship
        self.score = 0
        self.score_multiplier = 1
        self.invulnerable = False
        self.invulnerable_cooldown_count = 60

    def change_score(self, points):
        self.score += points * self.score_multiplier

    def display(self):
        if self.invulnerable:
            if self.invulnerable_cooldown_count % 5 == 0:
                self.ship.surface = ship_blue
            else:
                self.ship.surface = ship_orange

        font = pygame.font.SysFont('arial', 30)
        text = font.render(self.name + ": " + str(self.score), False, color_white)
        screen.blit(text, pygame.Rect(10, H / 1.08, W / 5, H / 5))
        self.ship.display()
