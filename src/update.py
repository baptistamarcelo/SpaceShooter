import pygame

from src.config import W, laser_blue, H, laser_blue_impact, ship_blue, laser_red_impact, impact_2, \
    player_laser_sound, game_state
from src.entities.laser import Laser
from src.util import check_collision, roll_chance_spawn_meteor, roll_chance_spawn_enemy, roll_chance_spawn_item


class Update:
    @staticmethod
    def meteor():
        roll_chance_spawn_meteor()

        for meteor in game_state.meteors:
            meteor.display()

    @staticmethod
    def enemy():
        roll_chance_spawn_enemy()

        for enemy in game_state.enemies:
            enemy.display()

    @staticmethod
    def item():
        for item in game_state.items:
            item.display()

    @staticmethod
    def input(player):
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                game_state.match = "quit"
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

            #  standard cannon always shoots
            Laser(surface=laser_blue,
                  owner="player",
                  pos_x=ship_middle_pos,
                  pos_y=player.ship.pos_y)

            #  extra cannons depending on power level
            if player.extra_cannons:
                for counter in range(1, player.extra_cannons + 1):
                    Laser(surface=laser_blue,
                          owner="player",
                          pos_x=ship_middle_pos + counter * (player.ship.width / 5),
                          pos_y=player.ship.pos_y)

                    Laser(surface=laser_blue,
                          owner="player",
                          pos_x=ship_middle_pos - counter * (player.ship.width / 5),
                          pos_y=player.ship.pos_y)

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
        for laser in game_state.lasers:
            for enemy in game_state.enemies:
                if laser.owner == "player" and check_collision(enemy.ship, laser):
                    impact_2.play()
                    laser.surface = laser_blue_impact
                    game_state.enemies.remove(enemy)
                    player.change_score(100)
                    laser.hit = True
                elif laser.owner == "enemy" and check_collision(player.ship, laser) and not player.invulnerable:
                    player.damaged()

                    laser.surface = laser_red_impact
                    laser.hit = True
            laser.display()

        for enemy in game_state.enemies:
            enemy.check_fire()

            if check_collision(player.ship, enemy.ship) and not player.invulnerable:
                player.damaged()
                game_state.enemies.remove(enemy)

            if enemy.laser_cooldown:
                if enemy.laser_cooldown_count == enemy.laser_cooldown_max:
                    enemy.laser_cooldown = False
                    enemy.laser_cooldown_count = 0
                else:
                    enemy.laser_cooldown_count += 1

        for meteor in game_state.meteors:
            if check_collision(player.ship, meteor) and not player.invulnerable:
                player.damaged()
                game_state.meteors.remove(meteor)
                player.change_score(20)
            for laser in game_state.lasers:
                if laser.owner == "player" and check_collision(laser, meteor):
                    try:
                        game_state.meteors.remove(meteor)
                        roll_chance_spawn_item(meteor)
                    except ValueError:
                        pass  # ignores to handle the race condition if multiple lasers hit the same meteor

                    player.change_score(50)
                    impact_2.play()
                    laser.surface = laser_blue_impact
                    laser.hit = True

        for item in game_state.items:
            if check_collision(player.ship, item):
                player.collect_item(item)
                game_state.items.remove(item)
