"""
File containing fake word generator class

Classes:
    FakeGenerator(Generator)
"""

from functools import cached_property
from random import choice
from typing import List

from ..response import LetterValidity
from .generator import Generator


class FakeGenerator(Generator):
    """
    Fake word generator class

    ...

    Attributes
    ----------
    POSSIBLE_WORDS : List[str]
        List of possible words to choose from
    """

    with open("data/words.txt", "r", encoding="utf-8") as file:
        POSSIBLE_WORDS = file.readlines()

    @cached_property
    def _word(self) -> str:
        return choice(self.POSSIBLE_WORDS)

    def _word_validity(self, guess: str) -> List[LetterValidity]:
        return [self._letter_validity(pos, letter) for pos, letter in enumerate(guess)]

    def _letter_validity(self, pos: int, letter: str) -> LetterValidity:
        assert len(letter) == 1, "Expected char, got string"

        if letter == self._word[pos]:
            return LetterValidity.GREEN
        if letter in self._word:
            return LetterValidity.YELLOW
        return LetterValidity.GREY
