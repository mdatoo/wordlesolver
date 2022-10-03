"""
File containing fake word generator class

Classes:
    FakeGenerator(Generator)
"""

from collections import Counter
from functools import cached_property
from random import choice
from typing import List

from ..data import POSSIBLE_WORDS
from ..response import LetterValidity
from .generator import Generator


class FakeGenerator(Generator):
    """
    Fake word generator class
    """

    @cached_property
    def _word(self) -> str:
        return choice(POSSIBLE_WORDS)

    def _word_validity(self, guess: str) -> List[LetterValidity]:
        word_validity = [
            self._letter_validity(pos, letter) for pos, letter in enumerate(guess)
        ]

        character_frequencies = Counter(self._word)
        for character, validity in zip(guess, word_validity):
            if validity == LetterValidity.GREEN:
                character_frequencies[character] -= 1
        for pos, (character, validity) in enumerate(zip(guess, word_validity)):
            if validity == LetterValidity.YELLOW:
                if character_frequencies[character] <= 0:
                    word_validity[pos] = LetterValidity.GREY
                else:
                    character_frequencies[character] -= 1

        return word_validity

    def _letter_validity(self, pos: int, letter: str) -> LetterValidity:
        assert len(letter) == 1, "Expected char, got string"

        if letter == self._word[pos]:
            return LetterValidity.GREEN
        if letter in self._word:
            return LetterValidity.YELLOW
        return LetterValidity.GREY
