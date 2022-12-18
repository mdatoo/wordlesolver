"""
File containing save callback class.

Classes:
    SaveCallback(BaseCallback)
"""

from logging import info
from os import path

import numpy as np
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.results_plotter import (  # type:ignore[attr-defined]
    load_results,
    ts2xy,
)


class SaveCallback(BaseCallback):
    """
    Save callback class.

    ...

    Attributes
    ----------
    output_folder : str
        Folder to store/load weights
    weights_file : str
        File to store/load weights
    eval_interval : int
        Number of episodes to average reward over
    best_reward : float
        Best reward achieved
    """

    def __init__(self, output_folder: str, weights_file: str, eval_interval: int):
        """Initialise object."""
        super().__init__()

        self.output_folder = output_folder
        self.weights_file = weights_file
        self.eval_interval = eval_interval
        self.best_averaged_reward = -np.inf

    def _on_step(self) -> bool:
        if self.num_timesteps > 0 and self.n_calls % self.eval_interval == 0:
            _, rewards = ts2xy(load_results(self.output_folder), "timesteps")
            averaged_reward = np.mean(rewards[-100:])
            info(f"Timestep: {self.num_timesteps}")
            info(f"Averaged reward: {averaged_reward:.2f}, best averaged reward: {self.best_averaged_reward:.2f}")

            if averaged_reward > self.best_averaged_reward:
                info("Updating model")
                self.best_averaged_reward = averaged_reward
                if self.model:
                    self.model.save(path.join(self.output_folder, self.weights_file))

        return True
