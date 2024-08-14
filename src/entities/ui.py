import math

import pygame

from src.config import screen, color_white, usable_screen_height, usable_screen_width, color_black, number_sprites, life_blue, clock


class Ui:
    @staticmethod
    def display(player):
        font = pygame.font.SysFont(None, 40)

        name_text = font.render("Lives: ", False, color_white)
        score_text = font.render("Score: ", False, color_white)

        screen.fill(color_white, pygame.Rect(0, usable_screen_height, usable_screen_width, usable_screen_height * 0.01))
        screen.fill(color_black, pygame.Rect(0, usable_screen_height * 1.01, usable_screen_width, usable_screen_height))

        screen.blit(score_text, pygame.Rect(usable_screen_width * 0.01, usable_screen_height * 1.03, usable_screen_width * 0.1, usable_screen_height * 0.1))
        score_position = usable_screen_width * 0.1

        for number in str(player.score):
            screen.blit(number_sprites[number], (score_position, usable_screen_height * 1.038))
            width, _ = number_sprites[number].get_size()
            score_position += width

        width, _ = name_text.get_size()
        life_position = usable_screen_width * 0.90
        screen.blit(name_text, pygame.Rect(life_position - (width + usable_screen_width * 0.01), usable_screen_height * 1.03, usable_screen_width * 0.1, usable_screen_height * 0.1))
        for _ in range(player.lives):
            screen.blit(life_blue, (life_position, usable_screen_height * 1.03))
            width, _ = life_blue.get_size()
            life_position += width

        fps_text = font.render(f"FPS: {math.trunc(clock.get_fps())}", False, color_white)
        screen.blit(fps_text, pygame.Rect(usable_screen_width * 0.20, usable_screen_height * 1.03, usable_screen_width * 0.1, usable_screen_height * 0.1))

        cannons = player.extra_cannons * 2 + 1
        if player.extra_cannons == player.max_extra_cannons:
            cannons = f"{player.extra_cannons * 2 + 1} (MAX)"
        extra_cannons_text = font.render(f"CANNONS: {cannons}", False, color_white)
        screen.blit(extra_cannons_text, pygame.Rect(usable_screen_width * 0.30, usable_screen_height * 1.03, usable_screen_width * 0.1, usable_screen_height * 0.1))

        shield = "ACTIVE" if player.shield else "INACTIVE"
        shield_text = font.render(f"SHIELD: {shield}", False, color_white)
        screen.blit(shield_text, pygame.Rect(usable_screen_width * 0.55, usable_screen_height * 1.03, usable_screen_width * 0.1, usable_screen_height * 0.1))
