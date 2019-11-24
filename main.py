import pygame

from src.background import Background
from src.config import H, clock, FPS, lasers, \
    bg_pos_y_1, bg_speed, \
    player_invulnerability_cooldown_max, ship_blue, laser_blue_impact, enemies
from src.handler import meteor_handler, check_collision, enemy_handler, input_handler
from src.player import Player
from src.ship import Ship

pygame.display.set_caption("Space Shooter")

player = Player("Marcelo", Ship())
background = Background(bg_pos_y_1, -H, bg_speed)
game_exit = False


while not game_exit:
    background.display()

    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
            game_exit = True

    input_handler(player)
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
