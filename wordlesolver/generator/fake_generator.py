"""
File containing fake word generator class.

Classes:
    FakeGenerator(Generator)
"""

from collections import Counter
from secrets import choice
from typing import List, Optional

from ..data import DICTIONARY, LetterValidity
from .generator import Generator


class FakeGenerator(Generator):
    """Fake generator class."""

    def __init__(self) -> None:
        """Initialise object."""
        super().__init__()

        self._word: str = choice(DICTIONARY)

    def reset(self) -> Optional[List[LetterValidity]]:
        """
        Reset the environment.

        Returns
        -------
        Optional[List[LetterValidity]]
        """
        self._word = choice(DICTIONARY)

        return super().reset()

    def _guess_word(self, guess: str) -> List[LetterValidity]:
        word_validity: List[LetterValidity] = [self._letter_validity(pos, letter) for pos, letter in enumerate(guess)]

        character_frequencies: Counter[str] = Counter(self._word)

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
        if len(letter) != 1:
            raise AssertionError("Expected char, got string")

        if letter == self._word[pos]:
            return LetterValidity.GREEN
        if letter in self._word:
            return LetterValidity.YELLOW
        return LetterValidity.GREY
