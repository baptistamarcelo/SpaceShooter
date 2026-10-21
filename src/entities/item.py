import random
import pygame
from src.config import (
    usable_screen_height,
    screen,
    game_state,
    available_items,
)


class Item:
    def __init__(self, pos_x: float, pos_y: float, speed: float | None = None):
        """Create a new item at ``(pos_x, pos_y)``.

        Parameters
        ----------
        pos_x, pos_y:
            The top‑left coordinates where the item will first appear.
        speed:
            The vertical speed. If omitted it defaults to a fraction of the
            global ``game_state.default_speed`` so that items fall slower than
            meteors.
        """

        if speed is None:
            speed = game_state.default_speed / 8

        # ``available_items`` contains dicts like {"power_up": surface}
        # Choose a random item type and associated surface without mutating the list.
        dict_obj = random.choice(available_items)
        self.type, self.surface = next(iter(dict_obj.items()))

        self.mask = pygame.mask.from_surface(self.surface)
        self.width, self.height = self.surface.get_size()
        self.pos_x = pos_x - self.width / 2  # centre the surface
        self.pos_y = pos_y
        self.speed = speed

    def display(self) -> None:
        """Move the item downwards and draw it.

        The method removes the item from :data:`game_state.items` once it has
        moved past the bottom of the screen to keep the list small.
        """
        self.pos_y += self.speed
        screen.blit(self.surface, (self.pos_x, self.pos_y))
        if self.pos_y > usable_screen_height + self.height:
            try:
                game_state.items.remove(self)
            except ValueError:
                pass
