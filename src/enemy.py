import random

from src.config import enemies, H, W


class Enemy:
    def __init__(self, ship, difficulty):
        self.ship = ship
        self.hit = False
        self.difficulty = difficulty
        self.move_cooldown_y = False
        self.move_cooldown_x = False
        self.speed_x = 0
        self.speed_y = 0
        self.move_cooldown_y_max = 100
        self.move_cooldown_x_max = 100
        self.move_cooldown_y_count = 0
        self.move_cooldown_x_count = 0

    def display(self):
        self.move()
        if self.ship.pos_y > (H - self.ship.height):
            enemies.remove(self)

        self.ship.display()

    def move(self):
        move_x = random.randint(1, 10)
        move_y = random.randint(1, 20)
        if self.move_cooldown_x:
            if self.move_cooldown_x_count < self.move_cooldown_x_max and self.ship.pos_x > 0 and self.ship.pos_x < (W - self.ship.width):
                self.ship.pos_x += self.ship.speed * self.speed_x
            else:
                self.move_cooldown_x_count = 0
                self.move_cooldown_x = False

        if self.move_cooldown_y:
            if self.move_cooldown_y_count < self.move_cooldown_y_max:
                self.ship.pos_y += self.ship.speed * self.speed_y
            else:
                self.move_cooldown_y_count = 0
                self.move_cooldown_y = False

        if move_x == 1:
            self.move_cooldown_x = True
            move_left = random.randint(0, 1)
            if move_left:
                self.speed_x = 1
            else:
                self.speed_x = -1

        if move_y == 1:
            self.move_cooldown_y = True
            move_down = random.randint(0, 1)
            if move_down and self.ship.pos_y < H * 0.75:
                self.speed_y = 1
            else:
                if self.ship.pos_y > 0 + self.ship.height:
                    self.speed_y = -1
