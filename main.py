import pygame

from src.entities.background import Background
from src.config import clock, FPS, bg_pos_y_1, bg_speed, music_1, bg_space
from src.update import Update
from src.entities.player import Player
from src.entities.ship import Ship
from src.util import display_ui

pygame.display.set_caption("Space Shooter")

player = Player("Marcelo", Ship())
background = Background(pos_y_1=bg_pos_y_1, speed=bg_speed, pos_x=0, surface=bg_space)
game_exit = False
update = Update()

music = music_1
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

while not game_exit:
    background.display()

    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
            game_exit = True

    update.input(player)
    update.meteor()
    update.item()
    update.player(player)
    update.combat(player)
    update.enemy()

    player.display()
    display_ui(player)

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
quit()
