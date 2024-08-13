import pygame

from src.config import color_white, screen, W, H, color_black, game_state, font
from src.util import play_music


def display():
    menu_text = font.render("Space Shooter", False, color_white)

    guide_text_1 = font.render("Arrow keys to move", False, color_white)
    guide_text_2 = font.render("Space to shoot", False, color_white)
    guide_text_3 = font.render("Enter to begin", False, color_white)
    guide_text_4 = font.render("ESC to quit", False, color_white)

    guide_text_5 = font.render("You start with 3 lives", False, color_white)
    guide_text_6 = font.render("Shields absorb damage", False, color_white)
    guide_text_7 = font.render("Cannon upgrades are permanent", False, color_white)
    guide_text_8 = font.render("Bosses will appear depending on your score", False, color_white)

    separation_space = W * 0.1
    right_text_width = W - separation_space / 2 - guide_text_8.get_width()  # the lengthiest of the texts

    screen.fill(color_black, pygame.Rect(0, H * 0.1, W, H * 0.7))
    screen.blit(menu_text, pygame.Rect(W / 2 - menu_text.get_width() / 2, H * 0.2, 0, 0))

    screen.blit(guide_text_1, pygame.Rect(separation_space, H * 0.4, 2, 0))
    screen.blit(guide_text_2, pygame.Rect(separation_space, H * 0.5, 2, 0))
    screen.blit(guide_text_3, pygame.Rect(separation_space, H * 0.6, 2, 0))
    screen.blit(guide_text_4, pygame.Rect(separation_space, H * 0.7, 2, 0))

    screen.blit(guide_text_5, pygame.Rect(right_text_width, H * 0.4, 2, 0))
    screen.blit(guide_text_6, pygame.Rect(right_text_width, H * 0.5, 2, 0))
    screen.blit(guide_text_7, pygame.Rect(right_text_width, H * 0.6, 2, 0))
    screen.blit(guide_text_8, pygame.Rect(right_text_width, H * 0.7, 2, 0))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            game_state.match = "running"
            play_music('Alone Against Enemy.ogg')

        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
            game_state.match = "quit"
