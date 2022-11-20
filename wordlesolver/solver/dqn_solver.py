"""
File containing dqn solver class.

Classes:
    DqnSolver(Solver)

Functions:
    train() -> None
"""

from typing import List

from gym import make

from ..generator import Generator
from .solver import Solver


class DqnSolver(Solver):
    """Dqn solver class."""

    def __init__(self, generator: Generator, weights_file: str) -> None:
        """Initialise object."""
        super().__init__(generator)
        print(weights_file)
        raise NotImplementedError

    def _next_guess(self, possible_words: List[str]) -> str:
        raise NotImplementedError

    @staticmethod
    def train() -> None:
        """Train dqn solver."""
        _ = make("FakeGenerator-v0")
