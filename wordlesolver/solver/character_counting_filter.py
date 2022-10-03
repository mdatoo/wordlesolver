"""
File containing character counting filter decorator

Classes:
    CharacterCountingFilter
"""

from collections import defaultdict
from typing import Dict, List

from ..response import LetterValidity
from .filter import Filter


class CharacterCountingFilter(Filter):
    """
    Character counting filter decorator

    ...

    Attributes
    ----------
    character_to_possible_words : Dict[str, List[str]]
        Mapping from character to words in possible_words containing that character

    Methods
    -------
    filter_possible_words(guess : str, word_validity : List[LetterValidity])
        Filters possible_words list given a guess and resulting validity
    """

    def __init__(self) -> None:
        super().__init__()

        self._character_to_possible_words = (
            self._calculate_character_to_possible_words()
        )

    @property
    def character_to_possible_words(self) -> Dict[str, List[str]]:
        """
        Mapping from character to words in possible_words containing that character
        """

        return self._character_to_possible_words

    def filter_possible_words(
        self, guess: str, word_validity: List[LetterValidity]
    ) -> None:
        """
        Filters possible_words list given a guess and resulting validity

        Args:
            guess (str): Guessed word
            word_validity (List[LetterValidity]): Resulting validity
        """

        super().filter_possible_words(guess, word_validity)

        self._character_to_possible_words = (
            self._calculate_character_to_possible_words()
        )

    def _calculate_character_to_possible_words(self) -> Dict[str, List[str]]:
        character_to_possible_words = defaultdict(set)

        for word in self.possible_words:
            for character in word:
                character_to_possible_words[character].add(word)

        return character_to_possible_words
