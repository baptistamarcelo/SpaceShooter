import pygame
import random

from data.config import W, H, screen, meteor_grey_big, laser_blue_impact, clock, FPS, game_exit, meteors, lasers, \
    laser_cooldown_max, laser_cooldown_count, laser_cooldown, laser_hit, meteor_spawn_chance

from data.laser import Laser
from data.meteor import Meteor
from data.ship import Ship
from data.background import Background

pygame.init()

pygame.display.set_caption("Space Shooter")

ship = Ship()
background = Background(0, -H, 4)


def check_collision(obj_1, obj_2):
    offset = (int(obj_1.pos_x - obj_2.pos_x), int(obj_1.pos_y - obj_2.pos_y))
    collision_result = obj_2.mask.overlap(obj_1.mask, offset)

    return collision_result


while not game_exit:
    pygame.time.delay(10)

    background.display()

    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
            game_exit = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and ship.pos_x > ship.speed:
        ship.pos_x -= ship.speed
    if keys[pygame.K_RIGHT] and ship.pos_x < W - ship.width - ship.speed:
        ship.pos_x += ship.speed
    if keys[pygame.K_UP] and ship.pos_y > ship.speed:
        ship.pos_y -= ship.speed
    if keys[pygame.K_DOWN] and ship.pos_y < H - ship.height - ship.speed:
        ship.pos_y += ship.speed
    if keys[pygame.K_SPACE] and not laser_cooldown:
        laser = Laser(pos_x=ship.pos_x + (ship.width / 2), pos_y=ship.pos_y)
        laser.pos_x -= (laser.width / 2)
        lasers.append(laser)
        laser_cooldown = True

    if laser_cooldown:
        if laser_cooldown_count == laser_cooldown_max:
            laser_cooldown = False
            laser_cooldown_count = 0
        else:
            laser_cooldown_count += 1

    if random.randint(1, meteor_spawn_chance) == 1:
        meteor = Meteor(pos_x=random.randint(30, W - 30))
        meteors.append(meteor)

    for meteor in meteors:
        if check_collision(meteor, ship):
            meteor.surface = meteor_grey_big
        meteor.display()

    for laser in lasers:
        if laser.pos_y > 0:
            for meteor in meteors:
                offset = (int(laser.pos_x) - int(meteor.pos_x), int(laser.pos_y) - int(meteor.pos_y))
                collision_result = meteor.mask.overlap(laser.mask, offset)
                if collision_result:
                    old_width = laser.width
                    laser.surface = laser_blue_impact
                    l_width, l_height = laser.surface.get_size()
                    screen.blit(laser.surface, (laser.pos_x - l_width / 2 + old_width / 2, laser.pos_y - l_height / 2))
                    lasers.remove(laser)
                    meteors.remove(meteor)
                    laser_hit = True

        laser.pos_y -= laser.speed
        if laser_hit:
            laser_hit = False
        else:
            screen.blit(laser.surface, (laser.pos_x, laser.pos_y))

        if laser.pos_y < 0:
            lasers.remove(laser)

    screen.blit(ship.surface, (ship.pos_x, ship.pos_y))

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
quit()
