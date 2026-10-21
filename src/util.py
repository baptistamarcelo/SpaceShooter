"""Utility functions used across the game.

The original project had a small helper module that provided collision
checking and random spawn logic for meteors, enemies, and items.  During the
previous patch the file was accidentally deleted, breaking imports in
``src/update.py``.  This patch recreates the module with the expected
behaviour.

All functions are intentionally lightweight and operate directly on the
``game_state`` singleton defined in :mod:`src.config`.
"""

import random
from src.config import (
    brown_meteors,
    usable_screen_width,
    enemy_assets,
    game_state,
)
from src.entities.enemy import Enemy
from src.entities.item import Item
from src.entities.meteor import Meteor
from src.entities.ship import Ship

__all__ = [
    "check_collision",
    "roll_chance_spawn_meteor",
    "roll_chance_spawn_enemy",
    "roll_chance_spawn_item",
]


def check_collision(obj_1, obj_2):
    """Return True if ``obj_1`` collides with ``obj_2``.

    The function relies on the ``mask`` attributes of the objects which are
    assumed to be :class:`pygame.mask.Mask` instances.  It returns the mask
    overlap result, which is truthy when a collision occurs.
    """

    collision_offset = (int(obj_1.pos_x - obj_2.pos_x), int(obj_1.pos_y - obj_2.pos_y))
    return obj_2.mask.overlap(obj_1.mask, collision_offset)


def roll_chance_spawn_meteor():
    """Randomly spawn a meteor.

    The original implementation used ``game_state.item_spawn_chance`` which
    does not exist.  The corrected version uses ``game_state.meteor_spawn_chance``
    and applies the ``item_spawn_multiplier`` to allow difficulty based
    scaling.  A meteor surface is chosen from :data:`brown_meteors`.
    """

    spawn_chance = max(1, int(game_state.meteor_spawn_chance * game_state.item_spawn_multiplier))
    if random.randint(1, spawn_chance) == 1:
        meteor_surface = random.choice(brown_meteors)
        meteor = Meteor(surface=meteor_surface, pos_x=usable_screen_width / 2, pos_y=-50)
        meteor.pos_x = random.randint(30, usable_screen_width - meteor.width)

        # Avoid overlapping with the last spawned meteor
        if game_state.meteors:
            latest_meteor = game_state.meteors[-1]
            l_m_pos_x = latest_meteor.pos_x
            l_m_width = latest_meteor.width * 2
            if meteor.pos_x in range(l_m_pos_x - l_m_width, l_m_pos_x + l_m_width):
                # Reschedule recursively
                roll_chance_spawn_meteor()
                return
        game_state.meteors.append(meteor)


def roll_chance_spawn_enemy():
    """Randomly spawn an enemy if the screen is not full.

    The difficulty and spawn rates are influenced by the current game state
    via :data:`game_state.enemy_spawn_chance`.
    """

    if (
        len(game_state.enemies) < game_state.max_enemies_on_screen
        and random.randint(1, game_state.enemy_spawn_chance) == 1
    ):
        difficulty_roll = (
            game_state.boss_difficulty
            if game_state.boss_difficulty
            else random.choice(["easy", "normal", "hard"])
        )
        enemy_surface = random.choice(enemy_assets[difficulty_roll])
        enemy_ship = Ship(surface=enemy_surface)
        enemy = Enemy(ship=enemy_ship, difficulty=difficulty_roll)
        enemy.ship.pos_y = 1 - int(enemy.ship.height / 2)
        enemy.ship.pos_x = random.randint(30, usable_screen_width - enemy.ship.width)
        game_state.enemies.append(enemy)


def roll_chance_spawn_item():
    """Randomly spawn a power‑up item at a meteor's location.

    Items are spawned only when a meteor is present, mirroring the original
    behaviour where items fell from meteors.  The spawn probability is
    controlled by ``game_state.item_spawn_multiplier``.
    """

    if not game_state.meteors:
        return
    if random.randint(1, int(100 / game_state.item_spawn_multiplier)) == 1:
        meteor = random.choice(game_state.meteors)
        pos_x = meteor.pos_x + meteor.width / 2
        game_state.items.append(Item(pos_x=pos_x, pos_y=meteor.pos_y))
