"""
Import file including argument parsing utils

Classes:
    ValidateGenerator

MIsc variables:
    generators: Dict[str, Generator]
"""

from argparse import Action, ArgumentParser, Namespace

from .fake_generator import FakeGenerator
from .generator import Generator
from .real_generator import RealGenerator

generators = {"FakeGenerator": FakeGenerator, "RealGenerator": RealGenerator}


class ValidateGenerator(Action):
    """
    Class handling parsing for Generators
    """

    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        value: str,
        option_string=None,
    ):
        if value not in generators:
            parser.error(
                f"""Please enter a valid generator. Got: {value}
                Expected one of: {list(generators.keys())}"""
            )
        setattr(namespace, self.dest, generators[value])
