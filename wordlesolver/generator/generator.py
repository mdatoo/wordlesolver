"""
File containing word generator abstract class.

Classes:
    Generator(Env)
"""

from abc import abstractmethod
from typing import Any, Dict, List, Tuple

from gym import Env, spaces

from ..data import DICTIONARY_LENGTH, POSSIBLE_WORDS
from ..response import LetterValidity
from .word_filter import WordFilter


class Generator(Env):  # type: ignore[type-arg] # gym has bad types
    """
    Generator abstract class.

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

    GUESSES = 6

    ACTION_SPACE = spaces.Discrete(DICTIONARY_LENGTH)
    OBSERVATION_SPACE = spaces.MultiBinary(DICTIONARY_LENGTH)

    def __init__(self) -> None:
        """Initialise object."""
        self._done = False
        self._guesses_remaining = self.GUESSES
        self._word_filter = WordFilter()

    @property
    def done(self) -> bool:
        """Whether the game has ended."""
        return self._done

    @property
    def guesses_remaining(self) -> int:
        """Remaining guesses."""
        return self._guesses_remaining

    # pylint: disable=arguments-differ
    def reset(self) -> List[int]:  # type: ignore # gym has bad types
        """
        Reset the environment.

        Returns
        -------
        List[int]
        """
        self._done = False
        self._guesses_remaining = self.GUESSES
        self._word_filter = WordFilter()

        return self.observe()

    # pylint: disable=arguments-differ
    def step(self, action: int) -> Tuple[List[int], float, bool, Dict[str, Any]]:  # type: ignore # gym has bad types
        """
        Perform given action.

        Parameters
        ----------
        action : int
            Action to perform

        Returns
        -------
        Tuple[List[int], float, bool, dict]
        """
        if not self.ACTION_SPACE.contains(action):
            raise AssertionError(f"Invalid action {action} specified, must be in range [0..{DICTIONARY_LENGTH}]")
        if self.done:
            raise AssertionError("Cannot perform an action when game ended")

        guess = POSSIBLE_WORDS[action]
        word_validity = self._guess_word(guess)

        self._guesses_remaining -= 1
        if self.guesses_remaining <= 0 or self._all_green(word_validity):
            self._done = True
        self._word_filter.filter(guess, word_validity)

        return (
            self.observe(),
            self._get_reward(word_validity),
            self.done,
            {
                "possible_words": self._word_filter.possible_words,
                "word_validity": word_validity,
            },
        )

    @abstractmethod
    def _guess_word(self, guess: str) -> List[LetterValidity]:
        raise NotImplementedError

    def _all_green(self, word_validity: List[LetterValidity]) -> bool:
        return all(letter_validity == LetterValidity.GREEN for letter_validity in word_validity)

    def observe(self) -> List[int]:
        """
        Observe current state.

        Returns
        -------
        List[int]
        """
        return [1 if word in self._word_filter.possible_words else 0 for word in POSSIBLE_WORDS]

    def _get_reward(self, word_validity: List[LetterValidity]) -> float:
        green_reward = word_validity.count(LetterValidity.GREEN)
        yellow_reward = word_validity.count(LetterValidity.YELLOW) * 0.1
        unused_turns_reward = self.guesses_remaining * 5 if self.done else 0

        return green_reward + yellow_reward + unused_turns_reward
