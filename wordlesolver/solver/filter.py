"""
File containing filter class

Classes:
    Filter
"""

from collections import defaultdict
from typing import List

from ..data import POSSIBLE_WORDS
from ..response import LetterValidity


class Filter:
    """
    Filter class

    ...

    Attributes
    --------------
    possible_words : List[str]
        Possible words left in search space

    Methods
    -------
    filter_possible_words(guess : str, word_validity : List[LetterValidity])
        Filters possible_words list given a guess and resulting validity
    """

    def __init__(self) -> None:
        self._possible_words = POSSIBLE_WORDS

    @property
    def possible_words(self) -> List[str]:
        """
        Possible words left in search space
        """

        return self._possible_words

    def filter_possible_words(
        self, guess: str, word_validity: List[LetterValidity]
    ) -> None:
        """
        Filters possible_words list given a guess and resulting validity

        Args:
            guess (str): Guessed word
            word_validity (List[LetterValidity]): Resulting validity
        """

        self._filter_by_matches(guess, word_validity)
        self._filter_by_counts(guess, word_validity)

    def _filter_by_matches(
        self, guess: str, word_validity: List[LetterValidity]
    ) -> None:
        for pos, (character, validity) in enumerate(zip(guess, word_validity)):
            self._filter_by_match(pos, character, validity)

    def _filter_by_match(
        self, pos: int, character: str, validity: LetterValidity
    ) -> None:
        match validity:
            case LetterValidity.GREEN:
                self._filter_by_green_match(pos, character)
            case LetterValidity.YELLOW:
                self._filter_by_yellow_match(pos, character)

    def _filter_by_green_match(self, pos: int, character: str) -> None:
        self._possible_words = [
            word for word in self._possible_words if word[pos] == character
        ]

    def _filter_by_yellow_match(self, pos: int, character: str) -> None:
        self._possible_words = [
            word
            for word in self._possible_words
            if word[pos] != character and character in word
        ]

    def _filter_by_no_match(self, character: str) -> None:
        self._possible_words = [
            word for word in self._possible_words if character not in word
        ]

    def _filter_by_counts(
        self, guess: str, word_validity: List[LetterValidity]
    ) -> None:
        character_idxs = defaultdict(lambda: defaultdict(int))

        for character, letter_validity in zip(guess, word_validity):
            character_idxs[character][letter_validity] += 1

        for character, validities in character_idxs.items():
            if LetterValidity.GREEN and LetterValidity.YELLOW in validities:
                self._filter_by_at_least_count(
                    validities[LetterValidity.GREEN] + 1, character
                )
            elif LetterValidity.GREEN and LetterValidity.GREY in validities:
                self._filter_by_exact_count(validities[LetterValidity.GREEN], character)
            elif (
                LetterValidity.GREY in validities
                and LetterValidity.YELLOW not in validities
            ):
                self._filter_by_no_count(character)

    def _filter_by_at_least_count(self, count: int, character: str) -> None:
        self._possible_words = [
            word for word in self._possible_words if word.count(character) >= count
        ]

    def _filter_by_exact_count(self, count: int, character: str) -> None:
        self._possible_words = [
            word for word in self._possible_words if word.count(character) == count
        ]

    def _filter_by_no_count(self, character: str) -> None:
        self._filter_by_exact_count(0, character)
