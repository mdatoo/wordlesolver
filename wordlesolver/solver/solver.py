"""
File containing wordle solver abstract class

Classes:
    Solver(ABC)
"""

from abc import ABC, abstractmethod
from logging import info
from typing import Dict, List

from ..generator import Generator
from ..response import GameStatus, LetterValidity


class Solver(ABC):
    """
    Solver abstract class

    ...

    Attributes
    ----------
    responses : Dict[str, List[LetterValidity]]
        Dictionary of guess and word validity pairs

    Methods
    -------
    run() -> None
        Run the game
    """

    def __init__(self, generator: Generator) -> None:
        self._generator = generator
        self._word_validities = {}

    @property
    def responses(self) -> Dict[str, List[LetterValidity]]:
        """
        Dictionary of guess and word validity pairs
        """

        return self._responses

    def run(self) -> None:
        """
        Run the game
        """

        while True:
            next_guess = self.next_guess()
            response = self._generator.guess(next_guess)
            self._responses[next_guess] = response.word_validity

            info(f"Guessed {next_guess}, got {response.word_validity}")

            if response.game_status != GameStatus.RUNNING:
                info(f"Finished game with result {response.game_status}")
                break

    @abstractmethod
    def _next_guess(self) -> str:
        raise NotImplementedError
