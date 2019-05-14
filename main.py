import pygame
import random

from data.config import W, H, laser_blue, laser_blue_impact, clock, FPS, meteors, lasers, \
    laser_cooldown_max, laser_cooldown_count, laser_cooldown, meteor_spawn_chance, bg_pos_y_1, bg_speed, \
    player_invulnerability_cooldown_max, ship_blue, meteor_brown_big

from data.laser import Laser
from data.meteor import Meteor
from data.ship import Ship
from data.player import Player
from data.background import Background

pygame.init()

pygame.display.set_caption("Space Shooter")

player = Player("Marcelo", Ship())
background = Background(bg_pos_y_1, -H, bg_speed)

game_exit = False


def check_collision(obj_1, obj_2):
    collision_offset = (int(obj_1.pos_x - obj_2.pos_x), int(obj_1.pos_y - obj_2.pos_y))
    return obj_2.mask.overlap(obj_1.mask, collision_offset)


while not game_exit:
    pygame.time.delay(10)

    background.display()

    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
            game_exit = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.ship.pos_x > player.ship.speed:
        player.ship.pos_x -= player.ship.speed
    elif keys[pygame.K_RIGHT] and player.ship.pos_x < W - player.ship.width - player.ship.speed:
        player.ship.pos_x += player.ship.speed
    if keys[pygame.K_UP] and player.ship.pos_y > player.ship.speed:
        player.ship.pos_y -= player.ship.speed
    elif keys[pygame.K_DOWN] and player.ship.pos_y < H - player.ship.height - player.ship.speed:
        player.ship.pos_y += player.ship.speed
    if keys[pygame.K_SPACE] and not laser_cooldown:
        laser = Laser(surface=laser_blue, pos_x=player.ship.pos_x + (player.ship.width / 2), pos_y=player.ship.pos_y)
        laser.pos_x -= (laser.width / 2)  # align laser position to match ship cannon, uses width variable to calculate
        lasers.append(laser)
        laser_cooldown = True

    if laser_cooldown:
        if laser_cooldown_count == laser_cooldown_max:
            laser_cooldown = False
            laser_cooldown_count = 0
        else:
            laser_cooldown_count += 1

    if random.randint(1, meteor_spawn_chance) == 1:
        meteor = Meteor(surface=meteor_brown_big, pos_x=W/2, pos_y=-50)
        meteor.pos_x = random.randint(30, W - meteor.width)
        meteors.append(meteor)

    for meteor in meteors:
        meteor.display()
        if meteor.alive:
            if check_collision(meteor, player.ship) and not player.invulnerable:
                player.invulnerable = True
                meteor.collide()
                player.change_score(-100)

    if player.invulnerable:
        if player.invulnerable_cooldown_count == player_invulnerability_cooldown_max:
            player.invulnerable = False
            player.invulnerable_cooldown_count = 0
            player.ship.surface = ship_blue
        else:
            player.invulnerable_cooldown_count += 1

    for laser in lasers:
        if laser.pos_y <= 0:
            lasers.remove(laser)
        else:
            for meteor in meteors:
                if meteor.alive:
                    offset = (int(laser.pos_x) - int(meteor.pos_x), int(laser.pos_y) - int(meteor.pos_y))
                    collision_result = meteor.mask.overlap(laser.mask, offset)
                    if collision_result:
                        laser.surface = laser_blue_impact
                        lasers.remove(laser)
                        meteors.remove(meteor)
                        player.change_score(100)
            laser.display()

    player.display()

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
quit()
