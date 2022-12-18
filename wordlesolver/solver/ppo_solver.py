"""
File containing ppo solver class.

Classes:
    PPOSolver(Solver)
"""

from os import makedirs, path

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
    WEIGHTS_FILE : str
        File to store/load weights
    EVAL_INTERVAL : int
        Number of episodes to average reward over

    Methods
    -------
    train(self) -> None:
        Train ppo solver
    """

    OUTPUT_FOLDER: str = "out"
    WEIGHTS_FILE: str = "ppo_weights.hdf5"
    EVAL_INTERVAL: int = 100

    def __init__(self, generator: Generator) -> None:
        """Initialise object."""
        super().__init__(IntWrapper(PreviousActionWrapper(generator)))

        makedirs(self.OUTPUT_FOLDER, exist_ok=True)
        wrapped_generator: Monitor = Monitor(self._generator, self.OUTPUT_FOLDER)
        self.model: OnPolicyAlgorithm = PPO("MlpPolicy", wrapped_generator)
        if path.exists(self.OUTPUT_FOLDER):
            self.model.load(path.join(self.OUTPUT_FOLDER, self.WEIGHTS_FILE))

    def _next_guess(self, observation: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
        return self.model.predict(observation, deterministic=True)[0]

    def train(self) -> None:
        """Train ppo solver."""
        self.model.learn(10000, callback=SaveCallback(self.OUTPUT_FOLDER, self.WEIGHTS_FILE, self.EVAL_INTERVAL))
