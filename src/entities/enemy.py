import random

from src.config import H, W, laser_red, default_move_speed, enemy_laser_sound, game_state
from src.entities.laser import Laser


class Enemy:
    def __init__(self, ship, difficulty):
        self.ship = ship
        self.hit = False
        self.difficulty = difficulty
        difficulty_modifier = {"easy":   {"speed": 0.2, "laser_cooldown_max": 200},
                               "normal": {"speed": 0.4, "laser_cooldown_max": 150},
                               "hard":   {"speed": 0.8, "laser_cooldown_max": 100}
                               }

        self.speed_x = 0
        self.speed_y = 0
        self.move_cooldown_x = None
        self.move_cooldown_y = None
        self.reset_move_cooldown()
        self.laser_cooldown = False
        self.laser_cooldown_count = 0

        self.ship.speed = default_move_speed * difficulty_modifier[self.difficulty]['speed']
        self.laser_cooldown_max = difficulty_modifier[self.difficulty]['laser_cooldown_max']

    def display(self):
        self.move()
        if self.ship.pos_y > (H - self.ship.height):
            game_state.enemies.remove(self)

        self.ship.display()

    def reset_move_cooldown(self):
        cooldown = {'active': False,
                    'count': 0,
                    'max': 500}
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

    def check_fire(self):
        chance_of_firing = {
            "easy": 1,
            "normal": 2,
            "hard": 3
        }
        if random.randint(0, 7) <= chance_of_firing[self.difficulty] and not self.laser_cooldown:
            self.shoot()

    def shoot(self):
        enemy_laser_sound.play()
        Laser(surface=laser_red,
              owner="enemy",
              pos_x=self.ship.pos_x + (self.ship.width / 2),
              pos_y=self.ship.pos_y + self.ship.height,
              speed=default_move_speed * -1)
        self.laser_cooldown = True
