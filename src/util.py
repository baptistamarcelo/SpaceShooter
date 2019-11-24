import random

from src.config import brown_meteors, W, meteors, enemy_ships, default_move_speed
from src.enemy import Enemy
from src.meteor import Meteor
from src.ship import Ship


def check_collision(obj_1, obj_2):
    collision_offset = (int(obj_1.pos_x - obj_2.pos_x), int(obj_1.pos_y - obj_2.pos_y))
    return obj_2.mask.overlap(obj_1.mask, collision_offset)


def spawn_meteor():
    meteor_surface = brown_meteors[random.randint(0, len(brown_meteors) - 1)]
    meteor = Meteor(surface=meteor_surface, pos_x=W / 2, pos_y=-50)
    meteor.pos_x = random.randint(30, W - meteor.width)

    if meteors:
        latest_meteor = meteors[-1:][0]
        l_m_pos_x = latest_meteor.pos_x
        l_m_width = latest_meteor.width * 2
        if meteor.pos_x in range(l_m_pos_x - l_m_width, l_m_pos_x + l_m_width):
            meteor = spawn_meteor()

    return meteor


def spawn_enemy():
    enemy_surface = enemy_ships[random.randint(0, len(enemy_ships) - 1)]
    enemy_ship = Ship(surface=enemy_surface)
    enemy = Enemy(ship=enemy_ship, difficulty=random.choice(["easy", "medium", "hard"]))
    enemy.ship.pos_y = 1 - enemy.ship.height
    enemy.ship.pos_x = random.randint(30, W - enemy.ship.width)
    enemy.ship.speed = default_move_speed * 0.3
    return enemy
