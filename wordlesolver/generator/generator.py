"""
File containing word generator abstract class.

Classes:
    Generator(Env)
"""

from abc import abstractmethod
from logging import warning
from typing import Any, Dict, List, Optional, Tuple

from gym import Env

from ..data import DICTIONARY, WORD_LENGTH, LetterValidity


class Generator(Env):  # type: ignore[misc] # gym has bad types
    """
    Generator abstract class.

    ...

    Attributes
    ----------
    GUESSES : int
        Number of guesses allowed
    YELLOW_VALUE : int
        Reward for guessing a letter in the incorrect place
    GREEN_VALUE : int
        Reward for guessing a letter in the correct place
    UNUSED_TURN_VALUE : int
        Reward for not needing to use a turn
    INVALID_WORD_VALUE : int
        Reward for guessing a word not in the dictionary

    Properties
    ----------
    done : bool
        Whether the game has ended
    guesses_remaining : int
        Remaining guesses
    observation : Optional[List[LetterValidity]]
        Environment state
    won : bool
        Whether the game has been won
    reward : int
        Reward of previous action

    Methods
    -------
    reset(self) -> Optional[List[LetterValidity]]
        Reset the environment
    step(self, action: str) -> Tuple[Optional[List[LetterValidity]], int, bool, Dict[str, Any]]
        Perform given action
    """

    GUESSES: int = 6

    YELLOW_VALUE: int = 1
    GREEN_VALUE: int = YELLOW_VALUE * WORD_LENGTH
    UNUSED_TURN_VALUE: int = GREEN_VALUE * WORD_LENGTH
    INVALID_WORD_VALUE: int = -UNUSED_TURN_VALUE * GUESSES

    def __init__(self) -> None:
        """Initialise object."""
        self._done: bool = False
        self._guesses_remaining: int = self.GUESSES
        self._observation: Optional[List[LetterValidity]] = None

    @property
    def done(self) -> bool:
        """Whether the game has ended."""
        return self._done

    @property
    def guesses_remaining(self) -> int:
        """Remaining guesses."""
        return self._guesses_remaining

    @property
    def observation(self) -> Optional[List[LetterValidity]]:
        """Environment state."""
        return self._observation

    # pylint: disable=arguments-differ
    def reset(self) -> Optional[List[LetterValidity]]:
        """
        Reset the environment.

        Returns
        -------
        Optional[List[LetterValidity]]
        """
        self._done = False
        self._guesses_remaining = self.GUESSES
        self._observation = None

        return self.observation

    # pylint: disable=arguments-differ
    def step(self, action: str) -> Tuple[Optional[List[LetterValidity]], int, bool, Dict[str, Any]]:
        """
        Perform given action.

        Parameters
        ----------
        action : str
            Action to perform

        Returns
        -------
        Tuple[Optional[List[LetterValidity]], float, bool, dict]
        """
        if self.done:
            raise AssertionError("Cannot perform an action when game ended")

        if action not in DICTIONARY:
            self._done = True
            self._observation = None

            return (self.observation, self.INVALID_WORD_VALUE, self.done, {})

        self._observation = self._guess_word(action)
        self._guesses_remaining -= 1
        self._done = self.guesses_remaining <= 0 or self.won

        return (self.observation, self.reward, self.done, {})

    @property
    def won(self) -> bool:
        """Whether the game has been won."""
        if not self.observation:
            return False

        return all(letter_validity == LetterValidity.GREEN for letter_validity in self.observation)

    @property
    def reward(self) -> int:
        """Reward of previous action."""
        if not self.observation:
            raise AssertionError("Cannot get reward of unknown observation")

        green_reward: int = self.observation.count(LetterValidity.GREEN) * self.GREEN_VALUE
        yellow_reward: int = self.observation.count(LetterValidity.YELLOW) * self.YELLOW_VALUE
        unused_turns_reward: int = self.guesses_remaining * self.UNUSED_TURN_VALUE if self.done else 0

        return green_reward + yellow_reward + unused_turns_reward

    @abstractmethod
    def _guess_word(self, guess: str) -> List[LetterValidity]:
        raise NotImplementedError

    def render(self, _: str = "human") -> None:
        """[NOT IMPLEMENTED] Render current state."""
        warning("Rendering has not been implemented for this environment")
