"""
File containing maximise matches solver class.

Classes:
    MaximiseMatchesSolver(Solver)
"""

from logging import info
from typing import List

from tqdm import tqdm

from ..data import POSSIBLE_WORDS
from .solver import Solver


# pylint: disable=too-few-public-methods; runnable solver
class MaximiseMatchesSolver(Solver):
    """Maximise matches solver class."""

    def run(self) -> None:
        """Run solver."""
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

    def _next_guess(self, possible_words: List[str]) -> str:
        return str(
            max(
                tqdm(possible_words),
                key=lambda guess: self._count_matches(guess, possible_words),
            )
        )

    def _count_matches(self, guess: str, possible_words: List[str]) -> int:
        matching_chars = set()

        for word in possible_words:
            for char_0, char_1 in zip(guess, word):
                if char_0 == char_1:
                    matching_chars.add(char_0)
        return len(matching_chars)
