"""
File containing int wrapper.

Classes:
    IntWrapper(ActionObservationWrapper)
"""

from typing import List, Optional, Tuple

import numpy as np
import numpy.typing as npt
from gym import spaces

from ...data import DICTIONARY, DICTIONARY_LENGTH, LetterValidity, WordFilter
from ..generator import Generator
from .action_observation_wrapper import ActionObservationWrapper


class IntWrapper(ActionObservationWrapper):
    """
    Int wrapper.

    ...

    Attributes
    ----------
    action_space : spaces.Box
        Actions allowed
    observation_space : spaces.Box
        Possible observations

    Methods
    -------
    reset(self) -> Any
        Reset the environment
    observation(self, observation: Tuple[Optional[str], Optional[List[LetterValidity]]]) -> npt.NDArray[np.uint8]
        Return observation as numpy array
    action(self, action: npt.NDArray[np.uint8]) -> str
        Return action as string
    """

    def __init__(self, env: Generator) -> None:
        """Initialise object."""
        super().__init__(env)

        self.action_space: spaces.Box = spaces.Discrete(DICTIONARY_LENGTH)
        self.observation_space: spaces.Box = spaces.MultiBinary(DICTIONARY_LENGTH)
        self._word_filter = WordFilter()

    def reset(self) -> npt.NDArray[np.uint8]:
        """
        Reset the environment.

        Returns
        -------
        npt.NDArray[np.uint8]
        """
        self._word_filter = WordFilter()

        return super().reset()  # type: ignore[no-any-return]

    def observation(self, observation: Tuple[Optional[str], Optional[List[LetterValidity]]]) -> npt.NDArray[np.uint8]:
        """
        Return observation as numpy array.

        Parameters
        ----------
        observation : Tuple[Optional[str], Optional[List[LetterValidity]]]
            Environment state

        Returns
        -------
        npt.NDArray[np.uint8]
        """
        self._word_filter.filter(*observation)

        return np.array([(1 if word in self._word_filter.possible_words else 0) for word in DICTIONARY])

    def action(self, action: npt.NDArray[np.uint8]) -> str:
        """
        Return action as string.

        Parameters
        ----------
        action : npt.NDArray[np.uint8]
            Action to perform

        Returns
        -------
        str
        """
        return DICTIONARY[action]
