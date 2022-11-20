"""
File containing maximise matches solver class.

Classes:
    MaximiseMatchesSolver(Solver)
"""

from typing import List

from tqdm import tqdm

from .solver import Solver


# pylint: disable=too-few-public-methods; runnable solver
class MaximiseMatchesSolver(Solver):
    """Maximise matches solver class."""

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
