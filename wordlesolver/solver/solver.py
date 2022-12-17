"""
File containing wordle solver abstract class.

Classes:
    Solver(ABC)
"""

from abc import ABC, abstractmethod
from logging import info
from typing import Any

from gym import Env


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

    def __init__(self, generator: Env) -> None:
        """Initialise object."""
        self._generator: Env = generator

    def run(self) -> None:
        """Run the game."""
        observation: Any = self._generator.reset()
        done: bool = False

        while not done:
            next_action: Any = self._next_guess(observation)
            observation, reward, done, _ = self._generator.step(next_action)

            info(f"Took action {next_action}, got reward {reward}, got observation {observation}")

        info("Finished game")

    @abstractmethod
    def _next_guess(self, observation: Any) -> Any:
        raise NotImplementedError
