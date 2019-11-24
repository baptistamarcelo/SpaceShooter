import pygame

from src.background import Background
from src.config import W, H, laser_blue, clock, FPS, lasers, \
    bg_pos_y_1, bg_speed, \
    player_invulnerability_cooldown_max, ship_blue, meteors, \
    laser_blue_impact, enemies
from src.laser import Laser
from src.player import Player
from src.ship import Ship
from src.handler import meteor_handler, check_collision, enemy_handler

pygame.display.set_caption("Space Shooter")

player = Player("Marcelo", Ship())
background = Background(bg_pos_y_1, -H, bg_speed)

game_exit = False


while not game_exit:
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
    if keys[pygame.K_SPACE] and not player.laser_cooldown:
        laser = Laser(surface=laser_blue, pos_x=player.ship.pos_x + (player.ship.width / 2), pos_y=player.ship.pos_y)
        laser.pos_x -= (laser.width / 2)  # align laser position to match ship cannon, uses width variable to calculate
        lasers.append(laser)
        player.laser_cooldown = True

    meteor_handler()

    if player.laser_cooldown:
        if player.laser_cooldown_count == player.laser_cooldown_max:
            player.laser_cooldown = False
            player.laser_cooldown_count = 0
        else:
            player.laser_cooldown_count += 1

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

    if player.invulnerable:
        if player.invulnerable_cooldown_count == player_invulnerability_cooldown_max:
            player.invulnerable = False
            player.invulnerable_cooldown_count = 0
            player.ship.surface = ship_blue
        else:
            player.invulnerable_cooldown_count += 1

    enemy_handler()
    player.display()

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
quit()
