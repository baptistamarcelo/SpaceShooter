import random
import pygame

from src.config import brown_meteors, W, meteors, enemy_ships, numbers, color_white, screen, \
    color_black, H, life_blue
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
    difficulty_choice = random.choice(["easy", "normal", "hard"])
    enemy_surface = random.choice(enemy_ships[difficulty_choice])
    enemy_ship = Ship(surface=enemy_surface)
    enemy = Enemy(ship=enemy_ship, difficulty=difficulty_choice)
    enemy.ship.pos_y = 1 - int(enemy.ship.height / 2)
    enemy.ship.pos_x = random.randint(30, W - enemy.ship.width)
    return enemy


def display_ui(player):
    font = pygame.font.SysFont(None, 40)

    name_text = font.render(player.name + ":", False, color_white)
    score_text = font.render("Score: ", False, color_white)

    screen.fill(color_white, pygame.Rect(0, H, W, H * 0.01))
    screen.fill(color_black, pygame.Rect(0, H * 1.01, W, H))

    screen.blit(score_text, pygame.Rect(W * 0.01, H * 1.03, W * 0.1, H * 0.1))
    score_position = W * 0.1

    for number in str(player.score):
        screen.blit(numbers[number], (score_position, H * 1.038))
        width, _ = numbers[number].get_size()
        score_position += width

    width, _ = name_text.get_size()
    life_position = W * 0.90
    screen.blit(name_text, pygame.Rect(life_position - (width + W * 0.01), H * 1.03, W * 0.1, H * 0.1))
    for _ in range(player.lives):
        screen.blit(life_blue, (life_position, H * 1.03))
        width, _ = life_blue.get_size()
        life_position += width
