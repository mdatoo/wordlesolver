"""
Import file including argument parsing utils.

Classes:
    ValidateGenerator

Misc variables:
    generators: Dict[str, Generator]
"""

from argparse import Action, ArgumentParser, Namespace
from typing import Any, Optional, Sequence, Union

from .fake_generator import FakeGenerator
from .generator import Generator
from .real_generator import RealGenerator

generators = {"FakeGenerator": FakeGenerator, "RealGenerator": RealGenerator}


class ValidateGenerator(Action):
    """Class handling parsing for Generators."""

    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        value: Union[str, Sequence[Any], None],
        _: Optional[Any] = None,
    ) -> None:
        """Override to validate and construct generator."""
        if not isinstance(value, str) or value not in generators:
            parser.error(
                f"""Please enter a valid generator. Got: {value}
                Expected one of: {list(generators.keys())}"""
            )
        setattr(namespace, self.dest, generators[value])


__all__ = ["Generator", "FakeGenerator", "RealGenerator", "ValidateGenerator"]
