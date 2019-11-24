import pygame

from src.background import Background
from src.config import H, clock, FPS, bg_pos_y_1, bg_speed
from src.handler import meteor_handler, enemy_handler, input_handler, combat_handler, player_handler
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
    player_handler(player)
    combat_handler(player)
    enemy_handler()
    player.display()

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
quit()
