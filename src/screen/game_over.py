import pygame

from src.config import color_white, screen, usable_screen_width, usable_screen_height, color_black, game_state


def display(player):
    screen.fill(
        color_black,
        pygame.Rect(
            usable_screen_width * 0.20,
            usable_screen_height * 0.20,
            usable_screen_width / 1.5,
            usable_screen_height / 1.5
        )
    )
    font = pygame.font.SysFont(None, 40)

    menu_text = font.render("Game Over", False, color_white)
    screen.blit(menu_text, pygame.Rect(usable_screen_width * 0.5, usable_screen_height * 0.2, 0, 0))

    guide_text = font.render(f"Enter to play again. ESC to quit.", False, color_white)
    screen.blit(guide_text, pygame.Rect(usable_screen_width * 0.2, usable_screen_height * 0.4, 2, 0))

    end_text_1 = font.render(f"Player: {player.name}", False, color_white)
    end_text_2 = font.render(f"Score: {player.score}", False, color_white)

    end_text_3 = font.render("Press Enter to return to the main menu", False, color_white)
    end_text_4 = font.render("Press ESC to quit", False, color_white)

    separation_space = usable_screen_width * 0.1

    # the lengthiest of the texts
    right_text_width = usable_screen_width - separation_space / 2 - end_text_3.get_width()

    screen.fill(
        color_black,
        pygame.Rect(0, usable_screen_height * 0.1, usable_screen_width, usable_screen_height * 0.7)
        )
    screen.blit(
        menu_text,
        pygame.Rect(usable_screen_width / 2 - menu_text.get_width() / 2, usable_screen_height * 0.2, 0, 0)
    )

    screen.blit(end_text_1, pygame.Rect(separation_space, usable_screen_height * 0.4, 2, 0))
    screen.blit(end_text_2, pygame.Rect(separation_space, usable_screen_height * 0.5, 2, 0))

    screen.blit(end_text_3, pygame.Rect(right_text_width, usable_screen_height * 0.4, 2, 0))
    screen.blit(end_text_4, pygame.Rect(right_text_width, usable_screen_height * 0.5, 2, 0))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            game_state.set_match_state("restart")
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
            game_state.set_match_state("quit")
