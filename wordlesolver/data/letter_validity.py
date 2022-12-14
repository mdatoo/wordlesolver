"""
File containing enum describing a letter's validity at a certain position.

Classes:
    LetterValidity(Enum)
"""

from enum import Enum


class LetterValidity(Enum):
    """Enum describing a letter's validity at a certain position."""

    GREY = 0
    YELLOW = 1
    GREEN = 2
