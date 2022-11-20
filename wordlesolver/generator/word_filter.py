"""
File containing word filter class.

Classes:
    WordFilter
"""

from collections import defaultdict
from typing import Dict, List

from ..data import POSSIBLE_WORDS
from ..response import LetterValidity


class WordFilter:
    """
    WordFilter class.

    ...

    Properties
    ----------
    possible_words : List[str]
        Possible words left in search space

    Methods
    -------
    filter(self, guess : str, word_validity : List[LetterValidity]) -> None
        Filter possible words list given a guess and corresponding validity
    """

    def __init__(self) -> None:
        """Initialise object."""
        self._possible_words = POSSIBLE_WORDS

    @property
    def possible_words(self) -> List[str]:
        """Possible words left in search space."""
        return self._possible_words

    def filter(self, guess: str, word_validity: List[LetterValidity]) -> None:
        """
        Filter possible words list given a guess and corresponding validity.

        Parameters
        ----------
        guess : str
            Guessed word
        word_validity : List[LetterValidity]
            Corresponding validity
        """
        self._filter_by_matches(guess, word_validity)
        self._filter_by_counts(guess, word_validity)

    def _filter_by_matches(self, guess: str, word_validity: List[LetterValidity]) -> None:
        for pos, (character, validity) in enumerate(zip(guess, word_validity)):
            self._filter_by_match(pos, character, validity)

    def _filter_by_match(self, pos: int, character: str, validity: LetterValidity) -> None:
        match validity:
            case LetterValidity.GREEN:
                self._filter_by_green_match(pos, character)
            case _:
                self._filter_by_non_green_match(pos, character)

    def _filter_by_green_match(self, pos: int, character: str) -> None:
        self._possible_words = [word for word in self._possible_words if word[pos] == character]

    def _filter_by_non_green_match(self, pos: int, character: str) -> None:
        self._possible_words = [word for word in self._possible_words if word[pos] != character]

    def _filter_by_counts(self, guess: str, word_validity: List[LetterValidity]) -> None:
        character_idxs: Dict[str, Dict[LetterValidity, int]] = defaultdict(lambda: defaultdict(int))

        for character, letter_validity in zip(guess, word_validity):
            character_idxs[character][letter_validity] += 1

        for character, validities in character_idxs.items():
            count = validities[LetterValidity.GREEN] + validities[LetterValidity.YELLOW]

            if LetterValidity.GREY in validities:
                self._filter_by_exact_count(count, character)
            else:
                self._filter_by_at_least_count(count, character)

    def _filter_by_at_least_count(self, count: int, character: str) -> None:
        self._possible_words = [word for word in self._possible_words if word.count(character) >= count]

    def _filter_by_exact_count(self, count: int, character: str) -> None:
        self._possible_words = [word for word in self._possible_words if word.count(character) == count]
