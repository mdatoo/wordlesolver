"""
File containing action observation abstract wrapper.

Classes:
    ActionObservationWrapper(Wrapper)
"""

from abc import abstractmethod
from typing import Any, Tuple

from gym import Wrapper


class ActionObservationWrapper(Wrapper):  # type: ignore[misc] # gym has bad types
    """
    Action observation wrapper.

    ...

    Methods
    -------
    reset(self) -> Any
        Reset the environment using modified observation
    step(self, action: Any) -> Tuple[Any, ...]
        Perform given action using modified action and observation
    observation(self, observation: Any) -> Any
        Override observation
    action(self, action: Any) -> Any:
        Override action
    """

    # pylint: disable=arguments-differ
    def reset(self) -> Any:
        """
        Reset the environment using modified observation.

        Returns
        -------
        Any
        """
        return self.observation(super().reset())

    def step(self, action: Any) -> Tuple[Any, ...]:
        """
        Perform given action using modified action and observation.

        Parameters
        ----------
        action : Any
            Action to perform

        Returns
        -------
        Tuple[Any, ...]
        """
        observation, *rest = super().step(self.action(action))

        return self.observation(observation), *rest

    @abstractmethod
    def observation(self, observation: Any) -> Any:
        """
        Override observation.

        Parameters
        ----------
        observation : Any
            Environment state

        Returns
        -------
        Tuple[Optional[Any], Any]
        """
        raise NotImplementedError

    @abstractmethod
    def action(self, action: Any) -> Any:
        """
        Override action.

        Parameters
        ----------
        action : Any
            Action to perform

        Returns
        -------
        Any
        """
        raise NotImplementedError
