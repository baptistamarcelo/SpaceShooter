"""Game update loop.

This module contains a simple :class:`Update` class that is responsible for
processing all game logic each frame.  It is intentionally minimal and only
provides the methods required by :mod:`src.main`.
"""

import random
import pygame

from src.config import (
    usable_screen_width,
    laser_blue,
    usable_screen_height,
    laser_blue_impact,
    ship_blue,
    laser_red_impact,
    impact_2,
    player_laser_sound,
    game_state,
    boss_assets,
    impact_1,
)
from src.entities.boss import Boss
from src.entities.laser import Laser
from src.util import (
    check_collision,
    roll_chance_spawn_meteor,
    roll_chance_spawn_enemy,
    roll_chance_spawn_item,
)
from src.entities.particle import Particle


class Update:
    """Static class providing update helpers used by the main loop."""

    @staticmethod
    def meteor():
        """Handle meteor spawning and drawing."""
        roll_chance_spawn_meteor()
        # Try spawning an item from existing meteors
        roll_chance_spawn_item()
        for meteor in list(game_state.meteors):
            meteor.display()

    @staticmethod
    def enemy():
        """Handle enemy spawning and drawing."""
        roll_chance_spawn_enemy()
        for enemy in list(game_state.enemies):
            enemy.display()

    @staticmethod
    def item():
        """Draw power‑up items that have been spawned."""
        for item in list(game_state.items):
            item.display()

    @staticmethod
    def input(player):
        """Process keyboard input and player movement."""
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                game_state.set_match_state("quit")
        if keys[pygame.K_LEFT] and player.ship.pos_x > player.ship.speed:
            player.ship.pos_x -= player.ship.speed
        elif keys[pygame.K_RIGHT] and player.ship.pos_x < usable_screen_width - player.ship.width - player.ship.speed:
            player.ship.pos_x += player.ship.speed
        if keys[pygame.K_UP] and player.ship.pos_y > player.ship.speed:
            player.ship.pos_y -= player.ship.speed
        elif keys[pygame.K_DOWN] and player.ship.pos_y < usable_screen_height - player.ship.height - player.ship.speed:
            player.ship.pos_y += player.ship.speed
        if keys[pygame.K_SPACE] and not player.laser_cooldown:
            player_laser_sound.play()
            ship_middle_pos = player.ship.pos_x + (player.ship.width / 2)
            # Standard cannon always shoots
            Laser(surface=laser_blue, owner="player", pos_x=ship_middle_pos, pos_y=player.ship.pos_y)
            # Extra cannons depending on power level
            if player.extra_cannons:
                for counter in range(1, player.extra_cannons + 1):
                    Laser(surface=laser_blue, owner="player", pos_x=ship_middle_pos + counter * (player.ship.width / 5), pos_y=player.ship.pos_y)
                    Laser(surface=laser_blue, owner="player", pos_x=ship_middle_pos - counter * (player.ship.width / 5), pos_y=player.ship.pos_y)
            player.laser_cooldown = True

    @staticmethod
    def player(player):
        """Update the player's laser cooldown and invulnerability timers."""
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
        """Handle laser‑enemy interactions, scoring, and item collection."""
        # Laser‑enemy interactions
        for laser in list(game_state.lasers):
            for enemy in list(game_state.enemies):
                if laser.owner == "player" and check_collision(enemy.ship, laser):
                    laser.surface = laser_blue_impact
                    if isinstance(enemy, Boss):
                        enemy.damaged()
                        if enemy.health <= 0:
                            impact_1.play()
                            game_state.set_match_state("running")
                            game_state.boss_difficulty = None
                            game_state.enemies.remove(enemy)
                            for _ in range(15):
                                vel = (random.uniform(-2, 2), random.uniform(-2, 2))
                                game_state.particles.append(Particle(enemy.ship.pos_x, enemy.ship.pos_y, vel))
                        else:
                            impact_2.play()
                        game_state.enemies.remove(enemy)
                        for _ in range(10):
                            vel = (random.uniform(-2, 2), random.uniform(-2, 2))
                            game_state.particles.append(Particle(enemy.ship.pos_x, enemy.ship.pos_y, vel))
                    player.change_score(100)
                    laser.hit = True
                elif laser.owner == "enemy" and check_collision(player.ship, laser) and not player.invulnerable:
                    player.damaged()
                    laser.surface = laser_red_impact
                    laser.hit = True

        # Item collection
        for item in list(game_state.items):
            if check_collision(player.ship, item):
                player.collect_item(item)
                # Remove the collected item
                game_state.items.remove(item)

    @staticmethod
    def check_boss_battle():
        """Spawn a boss when the score threshold is reached."""
        if game_state.match == "running" and game_state.boss_counter_score >= game_state.score_to_spawn_boss:
            game_state.set_match_state("boss")
            # Create boss instance and add to enemy list
            boss = Boss()
            game_state.enemies.append(boss)
