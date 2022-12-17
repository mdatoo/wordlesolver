"""
File containing ppo solver class.

Classes:
    PPOSolver(Solver)
"""

from os import makedirs

import numpy as np
import numpy.typing as npt
from stable_baselines3 import PPO  # type:ignore[attr-defined]
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.on_policy_algorithm import OnPolicyAlgorithm

from ..generator import Generator
from ..generator.wrappers import IntWrapper, PreviousActionWrapper
from .save_callback import SaveCallback
from .solver import Solver


class PPOSolver(Solver):
    """
    PPO solver class.

    ...

    Attributes
    ----------
    OUTPUT_FOLDER : str
        Folder to store/load metrics and weights
    EVAL_INTERVAL : int
        Number of episodes to average reward over

    Methods
    -------
    train(self) -> None:
        Train ppo solver
    """

    OUTPUT_FOLDER: str = "out"
    EVAL_INTERVAL: int = 100

    def __init__(self, generator: Generator) -> None:
        """Initialise object."""
        super().__init__(IntWrapper(PreviousActionWrapper(generator)))

        makedirs(self.OUTPUT_FOLDER, exist_ok=True)
        wrapped_generator: Monitor = Monitor(self._generator, self.OUTPUT_FOLDER)
        self.model: OnPolicyAlgorithm = PPO("MlpPolicy", wrapped_generator)

    def _next_guess(self, observation: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
        raise NotImplementedError

    def train(self) -> None:
        """Train ppo solver."""
        self.model.learn(
            10000, callback=SaveCallback(output_folder=self.OUTPUT_FOLDER, eval_interval=self.EVAL_INTERVAL)
        )
