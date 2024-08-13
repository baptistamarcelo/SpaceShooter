import pygame

from src.config import color_white, screen, W, H, color_black, game_state


def display(player):
    game_state.match_over = True
    screen.fill(color_black, pygame.Rect(W * 0.20, H * 0.20, W / 1.5, H / 1.5))
    font = pygame.font.SysFont(None, 40)

    menu_text = font.render("Game Over", False, color_white)
    screen.blit(menu_text, pygame.Rect(W * 0.5, H * 0.2, 0, 0))

    guide_text = font.render(f"Player: {player.name} / Score: {player.score}. Press Enter to play again. Press ESC to quit.", False, color_white)
    screen.blit(guide_text, pygame.Rect(W * 0.2, H * 0.4, 2, 0))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            game_state.match = "restart"
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
            game_state.match = "quit"
