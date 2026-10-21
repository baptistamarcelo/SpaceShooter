"""Level placeholder.

The :class:`Level` class represents a single playable level or map.  The
implementation is intentionally minimal; it can be expanded with tile
management, background scrolling, and entity placement.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from src.entities.ship import Ship
from src.entities.enemy import Enemy
from src.entities.boss import Boss


@dataclass
class Level:
    """A minimal level representation."""

    name: str
    enemies: List[Enemy] = None
    bosses: List[Boss] = None

    def __post_init__(self) -> None:
        self.enemies = self.enemies or []
        self.bosses = self.bosses or []
