"""
Main file

Classes:
    ValidateGenerator

Functions:
    parse_arguments() -> Namespace
"""

from argparse import Action, ArgumentParser, Namespace

from wordlesolver.generator import generators


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
            parser.error(f"Please enter a valid generator. Got: {value}")
        setattr(namespace, self.dest, generators[value])


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

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    generator = args.generator()
    print(generator.guess("argue"))
