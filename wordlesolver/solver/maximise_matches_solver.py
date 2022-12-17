"""
File containing maximise matches solver class.

Classes:
    MaximiseMatchesSolver(Solver)
"""

from typing import List, Optional, Set, Tuple

from tqdm import tqdm

from ..data import LetterValidity, WordFilter
from ..generator import Generator
from ..generator.wrappers import PreviousActionWrapper
from .solver import Solver


class MaximiseMatchesSolver(Solver):
    """Maximise matches solver class."""

    def __init__(self, generator: Generator) -> None:
        """Initialise object."""
        super().__init__(PreviousActionWrapper(generator))

        self.word_filter: WordFilter = WordFilter()

    def _next_guess(self, observation: Tuple[Optional[str], Optional[List[LetterValidity]]]) -> str:
        self.word_filter.filter(*observation)

        return str(
            max(
                tqdm(self.word_filter.possible_words),
                key=self._count_matches,
            )
        )

    def _count_matches(self, guess: str) -> int:
        matching_chars: Set[str] = set()

        for word in self.word_filter.possible_words:
            for char_0, char_1 in zip(guess, word):
                if char_0 == char_1:
                    matching_chars.add(char_0)
        return len(matching_chars)

    def train(self) -> None:
        """[NOT IMPLEMENTED] Train maximise matches solver."""
        raise NotImplementedError("Maximise matches solver cannot be trained")
