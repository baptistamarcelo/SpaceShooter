"""Core engine placeholder.

This module provides a minimal ``GameEngine`` class that encapsulates the
main game loop.  The full implementation is beyond the scope of the current
task, but the class offers a public ``run`` method that can be expanded
later to include physics, AI, and rendering.
"""

from __future__ import annotations

import time
from typing import Iterable

from src.entities.ship import Ship
from src.entities.enemy import Enemy
from src.entities.boss import Boss


class GameEngine:
    """Very small stub of the main game engine.

    The real engine would coordinate updates for all entities, handle
    collision detection, render to the screen, and manage game state.
    """

    def __init__(self, ship: Ship, enemies: Iterable[Enemy] = (), bosses: Iterable[Boss] = ()):
        self.ship = ship
        self.enemies = list(enemies)
        self.bosses = list(bosses)
        self.running = False

    def run(self, frame_limit: int | None = None) -> None:
        """Run the engine for a limited number of frames or until ``self.running`` is False.

        Parameters
        ----------
        frame_limit: int | None
            Optional number of frames to run.  If ``None`` the loop continues
            indefinitely until :pyattr:`running` is set to ``False``.
        """

        self.running = True
        frame = 0
        while self.running and (frame_limit is None or frame < frame_limit):
            # Placeholder for update logic
            frame += 1
            time.sleep(1 / 60)  # simulate 60 FPS
            print(f"[GameEngine] Frame {frame}")
