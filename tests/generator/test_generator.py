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

from wordlesolver.data import DICTIONARY_LENGTH, POSSIBLE_WORDS, get_answer
from wordlesolver.generator import FakeGenerator, Generator, RealGenerator
from wordlesolver.response import LetterValidity

test_data = [
    # pylint: disable=protected-access; need to guess the answer
    (FakeGenerator, lambda fake_generator: fake_generator._word),
    (RealGenerator, lambda _: get_answer(datetime.now())),
]
test_data_names = ["fake_generator", "real_generator"]


@mark.parametrize(
    "generator_type, generator_to_actual_word", test_data, ids=test_data_names
)
def test_won_game(
    generator_type: Type[Generator],
    generator_to_actual_word: Callable[[Type[Generator]], str],
) -> None:
    """Test where agent guesses correctly."""
    # Given
    generator = generator_type()
    generator.reset()
    actual_word = generator_to_actual_word(generator)
    actual_word_id = POSSIBLE_WORDS.index(actual_word)

    # When
    observation, reward, done, extra_data = generator.step(actual_word_id)

    # Then
    assert observation == [1 if word == actual_word else 0 for word in POSSIBLE_WORDS]
    assert reward == 30
    assert done
    assert set(extra_data.keys()) == {"possible_words", "word_validity"}
    assert extra_data["possible_words"] == [actual_word]
    assert extra_data["word_validity"] == [LetterValidity.GREEN] * 5

    with raises(AssertionError) as exc_info:
        generator.step(actual_word_id)
    assert str(exc_info.value) == "Cannot perform an action when game ended"


@mark.parametrize(
    "generator_type, generator_to_actual_word", test_data, ids=test_data_names
)
def test_lost_game(
    generator_type: Type[Generator],
    generator_to_actual_word: Callable[[Type[Generator]], str],
) -> None:
    """Test where agent fails to guess the correct answer."""
    # Given
    generator = generator_type()
    generator.reset()
    actual_word = generator_to_actual_word(generator)
    guessed_word = "guess" if actual_word != "guess" else "point"
    guessed_word_id = POSSIBLE_WORDS.index(guessed_word)

    # When
    for _ in range(generator.GUESSES):
        observation, reward, done, extra_data = generator.step(guessed_word_id)

    # Then
    assert observation.count(1) > 1
    assert reward < 5
    assert done
    assert set(extra_data.keys()) == {"possible_words", "word_validity"}
    assert len(extra_data["possible_words"]) > 1
    assert extra_data["word_validity"] != [LetterValidity.GREEN] * 5

    with raises(AssertionError) as exc_info:
        generator.step(guessed_word_id)
    assert str(exc_info.value) == "Cannot perform an action when game ended"


@mark.parametrize("generator_type, _", test_data, ids=test_data_names)
def test_invalid_guess(
    generator_type: Type[Generator], _: Callable[[Type[Generator]], str]
) -> None:
    """Test where agent submits an invalid guess."""
    # Given
    generator = generator_type()
    generator.reset()
    guessed_word_id = -1

    # Then
    with raises(AssertionError) as exc_info:
        generator.step(guessed_word_id)
    assert (
        str(exc_info.value)
        == f"Invalid action {guessed_word_id} specified, must be in range [0..{DICTIONARY_LENGTH}]"
    )


if __name__ == "__main__":
    main()
