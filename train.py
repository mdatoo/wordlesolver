"""
File for training solvers.

Functions:
    parse_arguments() -> Namespace
"""

# pylint: disable=duplicate-code; similar to main file

from argparse import ArgumentParser, Namespace
from logging import INFO, basicConfig

from wordlesolver.generator import FakeGenerator
from wordlesolver.solver import ValidateSolver


def parse_arguments() -> Namespace:
    """
    Parse command line arguments.

    Returns:
        Namespace: Parsed args
    """
    parser = ArgumentParser()
    parser.add_argument(
        "solver",
        action=ValidateSolver,
        help="Wordle solver to use",
    )

    return parser.parse_args()


if __name__ == "__main__":
    basicConfig(level=INFO)
    args = parse_arguments()

    generator = FakeGenerator()
    solver = args.solver.train()

    solver.train()
