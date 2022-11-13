"""
File containing wordle solver abstract class.

Classes:
    Solver(ABC)
"""

from abc import ABC, abstractmethod

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

    @abstractmethod
    def run(self) -> None:
        """Run the game."""
        raise NotImplementedError
