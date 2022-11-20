"""
Import file including argument parsing utils.

Classes:
    ValidateSolver

Misc variables:
    solvers: Dict[str, Solver]
"""

from argparse import Action, ArgumentParser, Namespace
from typing import Any, Optional, Sequence, Union

from .dqn_solver import DqnSolver
from .maximise_matches_solver import MaximiseMatchesSolver
from .solver import Solver

solvers = {
    "dqn_solver.py": DqnSolver,
    "maximise_matches_solver.py": MaximiseMatchesSolver,
}


class ValidateSolver(Action):
    """Class handling parsing for Solvers."""

    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        value: Union[str, Sequence[Any], None],
        _: Optional[Any] = None,
    ) -> None:
        """Override to validate and construct solver."""
        if not isinstance(value, str) or value not in solvers:
            parser.error(
                f"""Please enter a valid solver. Got: {value}
                Expected one of: {list(solvers.keys())}"""
            )
        setattr(namespace, self.dest, solvers[value])


__all__ = ["Solver", "DqnSolver", "MaximiseMatchesSolver", "ValidateSolver"]
