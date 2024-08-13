import pygame

from src.config import screen, color_white, H, W, color_black, number_sprites, life_blue


class Ui:
    @staticmethod
    def display(player):
        font = pygame.font.SysFont(None, 40)

        name_text = font.render(player.name + ":", False, color_white)
        score_text = font.render("Score: ", False, color_white)

        screen.fill(color_white, pygame.Rect(0, H, W, H * 0.01))
        screen.fill(color_black, pygame.Rect(0, H * 1.01, W, H))

        screen.blit(score_text, pygame.Rect(W * 0.01, H * 1.03, W * 0.1, H * 0.1))
        score_position = W * 0.1

        for number in str(player.score):
            screen.blit(number_sprites[number], (score_position, H * 1.038))
            width, _ = number_sprites[number].get_size()
            score_position += width

        width, _ = name_text.get_size()
        life_position = W * 0.90
        screen.blit(name_text, pygame.Rect(life_position - (width + W * 0.01), H * 1.03, W * 0.1, H * 0.1))
        for _ in range(player.lives):
            screen.blit(life_blue, (life_position, H * 1.03))
            width, _ = life_blue.get_size()
            life_position += width
