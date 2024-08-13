from src.config import ship_orange, ship_blue, impact_1, shield_up_sound, power_up_sound, game_state
from src.entities.shield import Shield
from src.entities.ship import Ship


class Player:
    def __init__(self, name, ship):
        self.name = name
        self.ship = ship
        self.score = 0
        self.score_multiplier = 1
        self.invulnerable = False
        self.invulnerable_cooldown_count = 60
        self.lives = 3
        self.laser_cooldown = False
        self.laser_cooldown_count = 0
        self.laser_cooldown_max = 20
        self.invulnerability_cooldown_max = 150

        self.extra_cannons = 0  # on each side of the ship
        self.max_extra_cannons = 3

        self.shield = None

    def change_score(self, points):
        self.score += points * self.score_multiplier

    def display(self):
        if self.lives <= 0:
            game_state.match = "end"
        if self.invulnerable:
            if self.invulnerable_cooldown_count % 5 == 0:
                self.ship.surface = ship_blue
            else:
                self.ship.surface = ship_orange
        self.ship.display()

        if self.shield:
            self.shield.display()

    def damaged(self):
        if self.shield is None:
            self.lives -= 1
        else:
            self.shield = None
        self.invulnerable = True
        impact_1.play()

    def restart(self):
        self = self.__init__(self.name, Ship())

    def collect_item(self, item):
        if item.type == "power_up" and self.extra_cannons < self.max_extra_cannons:
            self.extra_cannons += 1
            power_up_sound.play()
        elif item.type == "shield" and self.shield is None:
            self.shield = Shield(self.ship)  # ship is what owns the shield, not the player
            shield_up_sound.play()
