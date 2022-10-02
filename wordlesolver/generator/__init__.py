"""
Import file

MIsc variables:
    generators: Dict[str, Generator]
"""

from .fake_generator import FakeGenerator
from .real_generator import RealGenerator

generators = {"FakeGenerator": FakeGenerator, "RealGenerator": RealGenerator}
