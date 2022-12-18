"""
File containing previous action wrapper.

Classes:
    PreviousActionWrapper(ActionObservationWrapper)
"""

from typing import Any, Optional, Tuple

from gym import Env

from .action_observation_wrapper import ActionObservationWrapper


class PreviousActionWrapper(ActionObservationWrapper):
    """
    Previous action wrapper.

    ...

    Attributes
    ----------
    previous_action : Optional[Any]
        Previous action taken

    Methods
    -------
    reset(self) -> Any
        Reset the environment
    observation(self, observation: Any) -> Tuple[Optional[Any], Any]
        Return observation with previous action
    action(self, action: Any) -> Any
        Record previous action
    """

    def __init__(self, env: Env) -> None:
        """Initialise object."""
        super().__init__(env)

        self.previous_action: Optional[Any] = None

    def reset(self) -> Any:
        """
        Reset the environment.

        Returns
        -------
        Any
        """
        self.previous_action = None

        return super().reset()

    def observation(self, observation: Any) -> Tuple[Optional[Any], Any]:
        """
        Return observation with previous action.

        Parameters
        ----------
        observation : Any
            Environment state

        Returns
        -------
        Tuple[Optional[Any], Any]
        """
        return self.previous_action, observation

    def action(self, action: Any) -> Any:
        """
        Record previous action.

        Parameters
        ----------
        action : Any
            Action to perform

        Returns
        -------
        Any
        """
        self.previous_action = action
        return action
