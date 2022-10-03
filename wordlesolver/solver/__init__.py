"""
Import file including argument parsing utils

Classes:
    ValidateSolver

Misc variables:
    solvers: Dict[str, Solver]
"""

from argparse import Action, ArgumentParser, Namespace

from .maximise_matches_solver import MaximiseMatchesSolver
from .solver import Solver

solvers = {"MaximiseMatchesSolver": MaximiseMatchesSolver}


class ValidateSolver(Action):
    """
    Class handling parsing for Solvers
    """

    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        value: str,
        option_string=None,
    ):
        if value not in solvers:
            parser.error(
                f"""Please enter a valid solver. Got: {value}
                Expected one of: {list(solvers.keys())}"""
            )
        setattr(namespace, self.dest, solvers[value])
