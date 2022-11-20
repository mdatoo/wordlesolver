"""
File containing wordle solver abstract class.

Classes:
    Solver(ABC)
"""

from abc import ABC, abstractmethod
from logging import info
from typing import List

from ..data import POSSIBLE_WORDS
from ..generator import Generator


# pylint: disable=too-few-public-methods; abstract class
class Solver(ABC):
    """
    Solver abstract class.

    ...

    Methods
    -------
    run() -> None
        Run the game
    """

    def __init__(self, generator: Generator) -> None:
        """Initialise object."""
        self._generator = generator

    def run(self) -> None:
        """Run the game."""
        self._generator.reset()

        done = False
        possible_words = POSSIBLE_WORDS

        while not done:
            next_guess = self._next_guess(possible_words)
            _, reward, done, extra_data = self._generator.step(
                POSSIBLE_WORDS.index(next_guess)
            )
            possible_words = extra_data["possible_words"]
            word_validity = extra_data["word_validity"]

            info(
                f"Guessed {next_guess}, got reward {reward}, got word validity {word_validity}"
            )

        info("Finished game")

    @abstractmethod
    def _next_guess(self, possible_words: List[str]) -> str:
        raise NotImplementedError
