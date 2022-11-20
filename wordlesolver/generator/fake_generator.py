"""
File containing fake word generator class.

Classes:
    FakeGenerator(Generator)
"""

from collections import Counter
from secrets import choice
from typing import List

from ..data import POSSIBLE_WORDS
from ..response import LetterValidity
from .generator import Generator


class FakeGenerator(Generator):
    """
    Fake word generator class.

    ...

    Attributes
    ----------
    GUESSES : int
        Number of guesses allowed
    ACTION_SPACE : spaces.Discrete
        Actions allowed
    OBSERVATION_SPACE : spaces.Discrete
        Possible observations

    Properties
    ----------
    done : bool
        Whether the game has ended
    guesses_remaining : int
        Remaining guesses

    Methods
    -------
    reset(self) -> None
        Reset the environment
    step(self, action: int) -> Tuple[List[int], float, bool, dict]
        Perform given action
    observe(self) -> List[int]
        Observe current state
    """

    def __init__(self) -> None:
        """Initialise object."""
        super().__init__()

        self._word = choice(POSSIBLE_WORDS)

    def reset(self) -> List[int]:  # type: ignore # gym has bad types
        """
        Reset the environment.

        Returns
        -------
        List[int]
        """
        self._word = choice(POSSIBLE_WORDS)

        return super().reset()

    def _guess_word(self, guess: str) -> List[LetterValidity]:
        word_validity = [self._letter_validity(pos, letter) for pos, letter in enumerate(guess)]

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

    def render(self, _: str = "human") -> None:
        """[NOT IMPLEMENTED] Render current state."""
        raise NotImplementedError("Rendering has not been implemented for this environment")
