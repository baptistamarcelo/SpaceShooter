import pygame

from src.config import color_white, screen, usable_screen_width, usable_screen_height, color_black, game_state, font


def display():
    menu_text = font.render("Space Shooter", False, color_white)

    guide_text_1 = font.render("Arrow keys to move", False, color_white)
    guide_text_2 = font.render("Space to shoot", False, color_white)
    guide_text_3 = font.render("Enter to begin", False, color_white)
    guide_text_4 = font.render("ESC to quit", False, color_white)

    guide_text_5 = font.render("You start with 3 lives", False, color_white)
    guide_text_6 = font.render("Shields absorb damage", False, color_white)
    guide_text_7 = font.render("Power ups grant 2 cannons", False, color_white)
    guide_text_8 = font.render("Bosses will appear depending on your score", False, color_white)

    separation_space = usable_screen_width * 0.1
    right_text_width = usable_screen_width - separation_space / 2 - guide_text_8.get_width()  # the lengthiest of the texts

    screen.fill(color_black, pygame.Rect(0, usable_screen_height * 0.1, usable_screen_width, usable_screen_height * 0.7))
    screen.blit(menu_text, pygame.Rect(usable_screen_width / 2 - menu_text.get_width() / 2, usable_screen_height * 0.2, 0, 0))

    screen.blit(guide_text_1, pygame.Rect(separation_space, usable_screen_height * 0.4, 2, 0))
    screen.blit(guide_text_2, pygame.Rect(separation_space, usable_screen_height * 0.5, 2, 0))
    screen.blit(guide_text_3, pygame.Rect(separation_space, usable_screen_height * 0.6, 2, 0))
    screen.blit(guide_text_4, pygame.Rect(separation_space, usable_screen_height * 0.7, 2, 0))

    screen.blit(guide_text_5, pygame.Rect(right_text_width, usable_screen_height * 0.4, 2, 0))
    screen.blit(guide_text_6, pygame.Rect(right_text_width, usable_screen_height * 0.5, 2, 0))
    screen.blit(guide_text_7, pygame.Rect(right_text_width, usable_screen_height * 0.6, 2, 0))
    screen.blit(guide_text_8, pygame.Rect(right_text_width, usable_screen_height * 0.7, 2, 0))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            game_state.set_match_state("running")

        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
            game_state.set_match_state("quit")
