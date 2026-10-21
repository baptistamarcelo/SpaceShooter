"""Simple particle system for explosion effects.

The :class:`Particle` class represents a very small, short‑lived visual
effect.  It is deliberately lightweight to keep the engine fast.  The
particle is rendered as a small circle that fades out over its lifespan.
"""

from __future__ import annotations

import math
import random
import pygame
from src.config import screen, color_white


class Particle:
    """A single particle used for explosions.

    Parameters
    ----------
    pos_x, pos_y:
        Starting position of the particle.
    velocity:
        Tuple of (x, y) velocity components.
    lifespan:
        Number of frames the particle will live.
    radius:
        Radius of the particle circle.
    color:
        RGB tuple.  Defaults to white.
    """

    def __init__(self, pos_x: float, pos_y: float, velocity: tuple[float, float], lifespan: int = 30, radius: int = 3, color: tuple[int, int, int] = (255, 255, 255)):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x, self.vel_y = velocity
        self.lifespan = lifespan
        self.radius = radius
        self.color = color
        self.alpha = 255

    def update(self) -> None:
        """Move the particle and fade it out."""
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self.lifespan -= 1
        # Fade out
        self.alpha = max(0, int(255 * (self.lifespan / 30)))

    def draw(self) -> None:
        """Render the particle to the screen with current alpha."""
        if self.lifespan <= 0:
            return
        surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, self.alpha), (self.radius, self.radius), self.radius)
        screen.blit(surf, (self.pos_x - self.radius, self.pos_y - self.radius))
