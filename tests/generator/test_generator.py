"""
File containing tests for generator.

Functions:
    test_won_game() -> None
    test_lost_game() -> None
    test_invalid_guess() -> None
"""
from datetime import datetime
from typing import Callable, Type

from pytest import main, mark, raises

from wordlesolver.data import LetterValidity, get_answer
from wordlesolver.generator import FakeGenerator, Generator, RealGenerator

test_data = [
    # pylint: disable=protected-access; need to guess the answer
    (FakeGenerator, lambda fake_generator: fake_generator._word),
    (RealGenerator, lambda _: get_answer(datetime.now())),
]
test_data_names = ["fake_generator", "real_generator"]


@mark.parametrize("generator_type, generator_to_answer", test_data, ids=test_data_names)
def test_won_game(
    generator_type: Type[Generator],
    generator_to_answer: Callable[[Generator], str],
) -> None:
    """Test where agent guesses correctly."""
    # Given
    generator = generator_type()
    generator.reset()
    answer = generator_to_answer(generator)

    # When
    observation, reward, done, extra_data = generator.step(answer)

    # Then
    assert observation == [LetterValidity.GREEN] * 5
    assert reward == 150
    assert done
    assert extra_data == {}

    with raises(AssertionError) as exc_info:
        generator.step(answer)
    assert str(exc_info.value) == "Cannot perform an action when game ended"


@mark.parametrize("generator_type, generator_to_answer", test_data, ids=test_data_names)
def test_lost_game(
    generator_type: Type[Generator],
    generator_to_answer: Callable[[Generator], str],
) -> None:
    """Test where agent fails to guess the correct answer."""
    # Given
    generator = generator_type()
    generator.reset()
    answer = generator_to_answer(generator)
    guess = "guess" if answer != "guess" else "point"

    # When
    for _ in range(generator.GUESSES):
        observation, reward, done, extra_data = generator.step(guess)

    # Then
    assert observation != [LetterValidity.GREEN] * 5
    assert reward < 25
    assert done
    assert extra_data == {}

    with raises(AssertionError) as exc_info:
        generator.step(guess)
    assert str(exc_info.value) == "Cannot perform an action when game ended"


@mark.parametrize("generator_type, _", test_data, ids=test_data_names)
def test_invalid_guess(generator_type: Type[Generator], _: Callable[[Type[Generator]], str]) -> None:
    """Test where agent submits an invalid guess."""
    # Given
    generator = generator_type()
    generator.reset()
    guess = "abcde"

    # When
    observation, reward, done, extra_data = generator.step(guess)

    # Then
    assert observation is None
    assert reward == -150
    assert done
    assert extra_data == {}

    with raises(AssertionError) as exc_info:
        generator.step(guess)
    assert str(exc_info.value) == "Cannot perform an action when game ended"


if __name__ == "__main__":
    main()
