import pygame

from src.config import clock, FPS, bg_pos_y_1, bg_space, game_state
from src.entities.player import Player
from src.entities.ship import Ship
from src.entities.ui import Ui
from src.exception.InvalidGameStateMatchException import InvalidGameStateMatchException
from src.screen import menu, game_over
from src.screen.background import Background
from src.update import Update

pygame.display.set_caption("Space Shooter")

player = Player("Player", Ship())
background = Background(pos_y_1=bg_pos_y_1, pos_x=0, surface=bg_space)
update = Update()

game_state.set_match_state("new")


while game_state.match != "quit":
    background.display()
    if game_state.match == "new":
        menu.display()
    elif game_state.match == "end":
        game_over.display(player)
    elif game_state.match == "restart":
        player.restart()
        game_state.restart()
    elif game_state.match in ["running", "boss"]:
        update.input(player)
        update.meteor()
        update.item()
        update.player(player)
        update.combat(player)  # check passing player to update all the time
        update.enemy()
        if game_state.match != "boss":
            update.check_boss_battle()

        player.display()
    else:
        raise InvalidGameStateMatchException(game_state.match)
    Ui.display(player)

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
quit()
