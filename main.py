import pygame

from src.background import Background
from src.config import H, clock, FPS, bg_pos_y_1, bg_speed, music_1, bg_space
from src.update import Update
from src.player import Player
from src.ship import Ship

pygame.display.set_caption("Space Shooter")

player = Player("Marcelo", Ship())
background = Background(pos_y_1=bg_pos_y_1, pos_y_2=-H, speed=bg_speed, pos_x=0, surface=bg_space)
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
    update.player(player)
    update.combat(player)
    update.enemy()

    player.display()

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
quit()
