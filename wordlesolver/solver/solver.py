"""
File containing wordle solver abstract class

Classes:
    Solver(ABC)
"""

from abc import ABC, abstractmethod
from logging import info
from typing import Optional

from ..generator import Generator
from ..response import GameStatus, Response


# pylint: disable=too-few-public-methods; abstract class
class Solver(ABC):
    """
    Solver abstract class

    ...

    Methods
    -------
    run() -> None
        Run the game
    """

    def __init__(self, generator: Generator) -> None:
        self._generator = generator

    def run(self) -> None:
        """
        Run the game
        """

        response = None

        while True:
            next_guess = self._next_guess(response)
            response = self._generator.guess(next_guess)

            info(f"Guessed {next_guess}, got {response.word_validity}")

            if response.game_status != GameStatus.RUNNING:
                break

        info(f"Finished game with result {response.game_status}")

    @abstractmethod
    def _next_guess(self, previous_response: Optional[Response]) -> str:
        raise NotImplementedError
