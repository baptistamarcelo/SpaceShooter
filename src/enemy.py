import random

from src.config import enemies, H, W


class Enemy:
    def __init__(self, ship, difficulty):
        self.ship = ship
        self.hit = False
        self.difficulty = difficulty
        self.speed_x = 0
        self.speed_y = 0
        self.move_cooldown_x = None
        self.move_cooldown_y = None
        self.reset_move_cooldown()

    def display(self):
        self.move()
        if self.ship.pos_y > (H - self.ship.height):
            enemies.remove(self)

        self.ship.display()

    def reset_move_cooldown(self):
        cooldown = {'active': False,
                    'count': 0,
                    'max': 1000}
        self.move_cooldown_x = cooldown
        self.move_cooldown_y = cooldown

    def move(self):
        move_x = random.randint(1, 100)
        move_y = random.randint(1, 300)
        if self.move_cooldown_x['active']:
            if self.move_cooldown_x['count'] < self.move_cooldown_x['max']:
                self.ship.pos_x += self.ship.speed * self.speed_x
                if self.ship.pos_x <= 0:
                    self.ship.pos_x = 0 + self.speed_x
                    self.reset_move_cooldown()
                if self.ship.pos_x >= (W - self.ship.width):
                    self.ship.pos_x = (W - self.ship.width) - self.speed_x
                    self.reset_move_cooldown()
            else:
                self.reset_move_cooldown()

        if self.move_cooldown_y['active']:
            if self.move_cooldown_y['count'] < self.move_cooldown_y['max']:
                self.ship.pos_y += self.ship.speed * self.speed_y
            else:
                self.move_cooldown_y['count'] = 0
                self.move_cooldown_y['active'] = False

        if move_x == 1:
            self.move_cooldown_x['active'] = True
            move_left = random.randint(0, 1)
            if move_left:
                self.speed_x = 1
            else:
                self.speed_x = -1

        if move_y == 1:
            self.move_cooldown_y['active'] = True
            move_down = random.randint(0, 1)
            if move_down and self.ship.pos_y < H * 0.75:
                self.speed_y = 1
            else:
                if self.ship.pos_y > 0 + self.ship.height:
                    self.speed_y = -1
