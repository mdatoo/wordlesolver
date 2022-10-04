"""
File containing maximise matches solver class

Classes:
    MaximiseMatchesSolver(Solver)
"""

from typing import Dict, List, Optional

from tqdm import tqdm

from ..generator import Generator
from ..response import Response
from .filter import Filter
from .solver import Solver


class MaximiseMatchesSolver(Solver):
    """
    Maximise matches solver class

    ...

    Attributes
    ----------
    possible_words : List[str]
        Possible words left in search space
    character_to_possible_words : Dict[str, List[str]]
        Mapping from character to words in possible_words containing that character
    """

    def __init__(self, generator: Generator) -> None:
        super().__init__(generator)

        self._filter = Filter()

    @property
    def possible_words(self) -> List[str]:
        """
        Possible words left in search space
        """

        return self._filter.possible_words

    @property
    def character_to_possible_words(self) -> Dict[str, List[str]]:
        """
        Mapping from character to words in possible_words containing that character
        """

        return self._filter.character_to_possible_words

    def _next_guess(self, previous_response: Optional[Response]) -> str:
        if previous_response:
            self._filter.filter_possible_words(
                previous_response.guess,
                previous_response.word_validity,
            )

        return max(tqdm(self.possible_words), key=self._count_matches)

    def _count_matches(self, guess: str) -> int:
        matching_chars = set()

        for word in self.possible_words:
            for char_0, char_1 in zip(guess, word):
                if char_0 == char_1:
                    matching_chars.add(char_0)
        return len(matching_chars)
