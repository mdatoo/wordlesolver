"""
File containing dqn solver class.

Classes:
    DqnSolver(Solver)
"""

from gym import make

# pylint: disable=unused-import; environment registration
from wordlesolver import generator

if __name__ == "__main__":
    env = make("FakeGenerator-v0")
