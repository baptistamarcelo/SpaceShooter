import random

import pygame

from src.config import W, meteors, meteor_spawn_chance, enemies, enemy_spawn_chance, \
    max_enemies_on_screen, lasers, laser_blue, H, laser_blue_impact, ship_blue
from src.laser import Laser
from src.util import check_collision, spawn_meteor, spawn_enemy


class Update:
    @staticmethod
    def meteor():
        if random.randint(1, meteor_spawn_chance) == 1:
            meteor = spawn_meteor()
            meteors.append(meteor)

        for meteor in meteors:
            meteor.display()

    @staticmethod
    def enemy():
        if len(enemies) < max_enemies_on_screen:
            if random.randint(1, enemy_spawn_chance) == 1:
                enemy = spawn_enemy()
                enemies.append(enemy)

        for enemy in enemies:
            enemy.display()

    @staticmethod
    def input(player):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.ship.pos_x > player.ship.speed:
            player.ship.pos_x -= player.ship.speed
        elif keys[pygame.K_RIGHT] and player.ship.pos_x < W - player.ship.width - player.ship.speed:
            player.ship.pos_x += player.ship.speed
        if keys[pygame.K_UP] and player.ship.pos_y > player.ship.speed:
            player.ship.pos_y -= player.ship.speed
        elif keys[pygame.K_DOWN] and player.ship.pos_y < H - player.ship.height - player.ship.speed:
            player.ship.pos_y += player.ship.speed
        if keys[pygame.K_SPACE] and not player.laser_cooldown:
            laser = Laser(surface=laser_blue,
                          pos_x=player.ship.pos_x + (player.ship.width / 2),
                          pos_y=player.ship.pos_y)

            laser.pos_x -= (laser.width / 2)  # align laser position with ship cannon, uses width variable to calculate
            lasers.append(laser)
            player.laser_cooldown = True

    @staticmethod
    def player(player):
        if player.laser_cooldown:
            if player.laser_cooldown_count == player.laser_cooldown_max:
                player.laser_cooldown = False
                player.laser_cooldown_count = 0
            else:
                player.laser_cooldown_count += 1

        if player.invulnerable:
            if player.invulnerable_cooldown_count == player.invulnerability_cooldown_max:
                player.invulnerable = False
                player.invulnerable_cooldown_count = 0
                player.ship.surface = ship_blue
            else:
                player.invulnerable_cooldown_count += 1

    @staticmethod
    def combat(player):
        for laser in lasers:
            for enemy in enemies:
                if check_collision(enemy.ship, laser):
                    laser.surface = laser_blue_impact
                    enemies.remove(enemy)
                    player.change_score(100)
                    laser.hit = True
            laser.display()

        for enemy in enemies:
            if check_collision(player.ship, enemy.ship) and not player.invulnerable:
                player.lives -= 1
                enemies.remove(enemy)
                player.invulnerable = True
