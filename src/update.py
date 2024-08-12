import random

import pygame

from src.config import W, meteors, meteor_spawn_chance, enemies, enemy_spawn_chance, \
    max_enemies_on_screen, lasers, laser_blue, H, laser_blue_impact, ship_blue, laser_red_impact, impact_2, \
    items, player_laser_sound
from src.entities.laser import Laser
from src.util import check_collision, spawn_meteor, spawn_enemy, spawn_item


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
    def item():
        for item in items:
            item.display()

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
            player_laser_sound.play()
            ship_middle_pos = player.ship.pos_x + (player.ship.width / 2)

            #  standard cannon always fire
            laser = Laser(surface=laser_blue,
                          owner="player",
                          pos_x=ship_middle_pos,
                          pos_y=player.ship.pos_y)
            laser.pos_x -= (laser.width / 2)  # align laser position with ship cannon, uses width variable to calculate
            lasers.append(laser)

            #  extra cannons depending on power level
            if player.extra_cannons:
                for counter in range(1, player.extra_cannons + 1):
                    laser = Laser(surface=laser_blue,
                                  owner="player",
                                  pos_x=ship_middle_pos + counter * (player.ship.width / 5),
                                  pos_y=player.ship.pos_y)
                    laser.pos_x -= (laser.width / 2)  # align laser position with ship cannon, uses width variable to calculate
                    lasers.append(laser)

                    laser = Laser(surface=laser_blue,
                                  owner="player",
                                  pos_x=ship_middle_pos - counter * (player.ship.width / 5),
                                  pos_y=player.ship.pos_y)
                    laser.pos_x -= (
                                laser.width / 2)  # align laser position with ship cannon, uses width variable to calculate
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
                if laser.owner == "player" and check_collision(enemy.ship, laser):
                    impact_2.play()
                    laser.surface = laser_blue_impact
                    enemies.remove(enemy)
                    player.change_score(100)
                    laser.hit = True
                elif laser.owner == "enemy" and check_collision(player.ship, laser) and not player.invulnerable:
                    player.damaged()

                    laser.surface = laser_red_impact
                    laser.hit = True
            laser.display()

        for enemy in enemies:
            enemy.check_fire()

            if check_collision(player.ship, enemy.ship) and not player.invulnerable:
                player.damaged()
                enemies.remove(enemy)

            if enemy.laser_cooldown:
                if enemy.laser_cooldown_count == enemy.laser_cooldown_max:
                    enemy.laser_cooldown = False
                    enemy.laser_cooldown_count = 0
                else:
                    enemy.laser_cooldown_count += 1

        for meteor in meteors:
            if check_collision(player.ship, meteor) and not player.invulnerable:
                player.damaged()
                meteors.remove(meteor)
                player.change_score(20)
            for laser in lasers:
                if laser.owner == "player" and check_collision(laser, meteor):
                    try:
                        meteors.remove(meteor)
                        items.append(spawn_item(meteor))
                    except ValueError:
                        pass  # if multiple lasers hit the same meteor, this avoids multiple items spawning or crashes

                    player.change_score(50)
                    impact_2.play()
                    laser.surface = laser_blue_impact
                    laser.hit = True

        for item in items:
            if check_collision(player.ship, item):
                player.collect_item(item)
                items.remove(item)
