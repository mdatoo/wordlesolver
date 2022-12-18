"""
Import file including argument parsing utils.

Classes:
    ValidateSolver

Misc variables:
    solvers: Dict[str, Solver]
"""

from argparse import Action, ArgumentParser, Namespace
from typing import Any, Dict, Optional, Sequence, Type, Union

from .maximise_matches_solver import MaximiseMatchesSolver
from .ppo_solver import PPOSolver
from .solver import Solver

solvers: Dict[str, Type[Solver]] = {
    "PPOSolver": PPOSolver,
    "MaximiseMatchesSolver": MaximiseMatchesSolver,
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


__all__ = ["Solver", "PPOSolver", "MaximiseMatchesSolver", "ValidateSolver"]
