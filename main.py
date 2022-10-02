"""
Main file

Functions:
    parse_arguments() -> Namespace
"""

from argparse import ArgumentParser, Namespace

from wordlesolver.generator import ValidateGenerator
from wordlesolver.solver import ValidateSolver


def parse_arguments() -> Namespace:
    """
    Parses command line arguments

    Returns:
        Namespace: Parsed args
    """

    parser = ArgumentParser()
    parser.add_argument(
        "generator",
        action=ValidateGenerator,
        help="Word generator to use",
    )
    parser.add_argument(
        "solver",
        action=ValidateSolver,
        help="Wordle solver to use",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    generator = args.generator()
    solver = args.solver(generator)

    solver.run()
