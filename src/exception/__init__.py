"""Exception subpackage.

This file allows the ``src.exception`` package to be imported.
It re‑exports the custom exception classes for convenient access.
"""

from .InvalidGameStateMatchException import InvalidGameStateMatchException

__all__ = ["InvalidGameStateMatchException"]
