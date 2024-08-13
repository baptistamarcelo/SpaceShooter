import pygame

from src.config import color_white, screen, W, H, color_black, game_state, snd_dir
from src.util import play_music


def display(player):
    game_state.match_over = True
    screen.fill(color_black, pygame.Rect(W * 0.20, H * 0.20, W / 1.5, H / 1.5))
    font = pygame.font.SysFont(None, 40)

    menu_text = font.render("Game Over", False, color_white)
    screen.blit(menu_text, pygame.Rect(W * 0.5, H * 0.2, 0, 0))

    guide_text = font.render(f"Enter to play again. ESC to quit.", False, color_white)
    screen.blit(guide_text, pygame.Rect(W * 0.2, H * 0.4, 2, 0))

    end_text_1 = font.render(f"Player: {player.name}", False, color_white)
    end_text_2 = font.render(f"Score: {player.score}", False, color_white)

    end_text_3 = font.render("Press Enter to return to the main menu", False, color_white)
    end_text_4 = font.render("Press ESC to quit", False, color_white)

    separation_space = W * 0.1
    right_text_width = W - separation_space / 2 - end_text_3.get_width()  # the lengthiest of the texts

    screen.fill(color_black, pygame.Rect(0, H * 0.1, W, H * 0.7))
    screen.blit(menu_text, pygame.Rect(W / 2 - menu_text.get_width() / 2, H * 0.2, 0, 0))

    screen.blit(end_text_1, pygame.Rect(separation_space, H * 0.4, 2, 0))
    screen.blit(end_text_2, pygame.Rect(separation_space, H * 0.5, 2, 0))

    screen.blit(end_text_3, pygame.Rect(right_text_width, H * 0.4, 2, 0))
    screen.blit(end_text_4, pygame.Rect(right_text_width, H * 0.5, 2, 0))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            play_music('Space Heroes.ogg')
            game_state.match = "restart"
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
            game_state.match = "quit"
