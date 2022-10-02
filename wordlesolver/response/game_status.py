"""
File containing enum describing current game status

Classes:
    GameStatus(Enum)
"""

from enum import Enum


class GameStatus(Enum):
    """
    Enum describing current game status
    """

    LOST = 0
    RUNNING = 1
    WON = 2
