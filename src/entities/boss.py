import random

from src.config import usable_screen_width, laser_red, enemy_laser_sound, game_state, boss_assets, \
    usable_screen_height, boss_damaged
from src.entities.laser import Laser
from src.entities.ship import Ship


class Boss:
    def __init__(self):
        difficulty_modifier = {
            "easy": {
                "speed": 0.4,
                "laser_cooldown_max": 150,
                "enemy_spawn_chance": 40,
                "meteor_spawn_chance": 180
            }, "normal": {
                "speed": 0.6,
                "laser_cooldown_max": 100,
                "enemy_spawn_chance": 30,
                "meteor_spawn_chance": 160
            }, "hard": {
                "speed": 0.9,
                "laser_cooldown_max": 50,
                "enemy_spawn_chance": 20,
                "meteor_spawn_chance": 140
            }
        }
        self.hit = False

        self.speed_x = 0
        self.move_cooldown_x = None
        self.reset_move_cooldown()

        self.laser_cooldown = False
        self.laser_cooldown_count = 0
        self.laser_cooldown_max = None
        self.health = 10
        self.invulnerable = False
        self.invulnerable_cooldown_count = 60
        self.invulnerability_cooldown_max = 150

        self.ship = Ship(boss_assets[game_state.boss_difficulty]["ship"], pos_y=usable_screen_height * 0.01)
        self.ship.speed = game_state.default_speed * difficulty_modifier[game_state.boss_difficulty]["speed"]
        self.laser_cooldown_max = difficulty_modifier[game_state.boss_difficulty]['laser_cooldown_max']
        game_state.enemy_spawn_chance = difficulty_modifier[game_state.boss_difficulty]["enemy_spawn_chance"]
        game_state.meteor_spawn_chance = difficulty_modifier[game_state.boss_difficulty]["meteor_spawn_chance"]

    def display(self):
        if self.invulnerable:
            if self.invulnerable_cooldown_count % 5 == 0:
                self.ship.surface = boss_assets[game_state.boss_difficulty]["ship"]
            else:
                self.ship.surface = boss_damaged
        self.move()
        self.ship.display()

    def damaged(self):
        if not self.invulnerable:
            self.invulnerable = True
            self.health -= 1
            self.move()

    def reset_move_cooldown(self):
        self.move_cooldown_x = {'active': False,
                                'count': 0,
                                'max': 500}

    def move(self):
        move_x = random.randint(1, 100)
        if self.move_cooldown_x['active']:
            if self.move_cooldown_x['count'] < self.move_cooldown_x['max']:
                self.ship.pos_x += self.ship.speed * self.speed_x
                if self.ship.pos_x <= 0:
                    self.ship.pos_x = 0 + self.speed_x
                    self.reset_move_cooldown()
                if self.ship.pos_x >= (usable_screen_width - self.ship.width):
                    self.ship.pos_x = (usable_screen_width - self.ship.width) - self.speed_x
                    self.reset_move_cooldown()
            else:
                self.reset_move_cooldown()

        if move_x == 1:
            self.move_cooldown_x['active'] = True
            move_left = random.randint(0, 1)
            if move_left:
                self.speed_x = 1
            else:
                self.speed_x = -1

    def check_fire(self):
        #  the lower the number, the higher the chance, max = 7
        chance_of_firing = {
            "easy": 6,
            "normal": 4,
            "hard": 3
        }
        if random.randint(0, 8) <= chance_of_firing[game_state.boss_difficulty] and not self.laser_cooldown:
            self.shoot()

    def shoot(self):
        enemy_laser_sound.play()
        Laser(surface=laser_red,
              owner="enemy",
              pos_x=self.ship.pos_x + (self.ship.width / 2),
              pos_y=self.ship.pos_y + self.ship.height,
              speed=game_state.default_speed * -1)
        self.laser_cooldown = True
