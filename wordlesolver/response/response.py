"""
File conntaining dataclass holding a response to a guess

Classes:
    Response
"""

from dataclasses import dataclass
from typing import List

from .game_status import GameStatus
from .letter_validity import LetterValidity


@dataclass
class Response:
    """
    Dataclass holding a response to a guess

    ...

    Attributes
    ----------
    game_status : GameStatus
        Current game status
    word_validity : List[LetterValidity]
        Letter validity for each letter in the guess
    """

    game_status: GameStatus
    word_validity: List[LetterValidity]
