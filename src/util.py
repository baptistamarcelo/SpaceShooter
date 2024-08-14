import random

from src.config import brown_meteors, usable_screen_width, enemy_assets, game_state
from src.entities.enemy import Enemy
from src.entities.item import Item
from src.entities.meteor import Meteor
from src.entities.ship import Ship


def check_collision(obj_1, obj_2):
    collision_offset = (int(obj_1.pos_x - obj_2.pos_x), int(obj_1.pos_y - obj_2.pos_y))
    return obj_2.mask.overlap(obj_1.mask, collision_offset)


def roll_chance_spawn_meteor():
    if random.randint(1, game_state.meteor_spawn_chance) == 1:
        meteor_surface = brown_meteors[random.randint(0, len(brown_meteors) - 1)]
        meteor = Meteor(surface=meteor_surface, pos_x=usable_screen_width / 2, pos_y=-50)
        meteor.pos_x = random.randint(30, usable_screen_width - meteor.width)

        if game_state.meteors:
            latest_meteor = game_state.meteors[-1:][0]
            l_m_pos_x = latest_meteor.pos_x
            l_m_width = latest_meteor.width * 2
            if meteor.pos_x in range(l_m_pos_x - l_m_width, l_m_pos_x + l_m_width):
                roll_chance_spawn_meteor()  # again to reshuffle pos_x if new meteor overlaps with last meteor spawned

        game_state.meteors.append(meteor)


def roll_chance_spawn_enemy():
    if len(game_state.enemies) < game_state.max_enemies_on_screen and random.randint(1, game_state.enemy_spawn_chance) == 1:
        difficulty_roll = game_state.boss_difficulty if game_state.boss_difficulty else random.choice(["easy", "normal", "hard"])
        enemy_surface = random.choice(enemy_assets[difficulty_roll])
        enemy_ship = Ship(surface=enemy_surface)
        enemy = Enemy(ship=enemy_ship, difficulty=difficulty_roll)
        enemy.ship.pos_y = 1 - int(enemy.ship.height / 2)
        enemy.ship.pos_x = random.randint(30, usable_screen_width - enemy.ship.width)
        game_state.enemies.append(enemy)


def roll_chance_spawn_item(meteor):
    if random.randint(1, game_state.item_spawn_chance) == 1:
        pos_x = meteor.pos_x + meteor.width / 2
        game_state.items.append(Item(pos_x=pos_x, pos_y=meteor.pos_y))
