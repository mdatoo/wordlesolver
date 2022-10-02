"""
File containing word generator abstract class

Classes:
    Generator(ABC)
"""

from abc import ABC, abstractmethod
from typing import List

from ..response import GameStatus, LetterValidity, Response


class Generator(ABC):
    """
    Generator abstract class

    ...

    Attributes
    ----------
    GUESSES : int
        Number of guesses allowed
    WORD_LENGTH : int
        Length of words allowed
    game_status : GameStatus
        Current game status
    guesses_taken : int
        Number of guesses taken

    Methods
    -------
    guess(guess: str) -> Response
        Guess a word, receive a response
    """

    GUESSES = 6
    WORD_LENGTH = 5

    def __init__(self) -> None:
        self._game_status = GameStatus.RUNNING
        self._guesses_taken = 0

    @property
    def game_status(self) -> GameStatus:
        """
        Current game status
        """

        return self._game_status

    @property
    def guesses_taken(self) -> int:
        """
        Number of guesses taken
        """

        return self._guesses_taken

    def guess(self, guess: str) -> Response:
        """
        Guess a word, receive a response

        Args:
            guess (str): Word to guess

        Returns:
            Response: Result of guess
        """

        assert len(guess) == self.WORD_LENGTH, f"Guess {guess} of incorrect length"
        assert self.game_status == GameStatus.RUNNING, "Cannot guess when game ended"

        word_validity = self._word_validity(guess)
        self._guesses_taken += 1

        if self._all_green(word_validity):
            self._game_status = GameStatus.WON
        elif self.guesses_taken >= 6:
            self._game_status = GameStatus.LOST

        return Response(self.game_status, word_validity)

    @abstractmethod
    def _word_validity(self, guess: str) -> List[LetterValidity]:
        raise NotImplementedError

    def _all_green(self, word_validity: List[LetterValidity]) -> bool:
        return all(
            letter_validity == LetterValidity.GREEN for letter_validity in word_validity
        )
