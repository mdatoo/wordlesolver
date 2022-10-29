"""
File containing tests for fake generator

Functions:
    test_won_game() -> None
    test_lost_game() -> None
    test_invalid_guess() -> None
"""

from pytest import main, raises

from wordlesolver.generator import FakeGenerator
from wordlesolver.response import GameStatus, LetterValidity


def test_won_game() -> None:
    """
    Test where agent guesses correctly
    """

    # Given
    fake_generator = FakeGenerator()
    # pylint: disable=protected-access; need to guess the answer
    actual_word = fake_generator._word

    # When
    response = fake_generator.guess(actual_word)

    # Then
    assert response.game_status == GameStatus.WON
    assert response.guess == actual_word
    assert response.word_validity == [LetterValidity.GREEN] * 5

    with raises(AssertionError) as exc_info:
        fake_generator.guess(actual_word)
    assert str(exc_info.value) == "Cannot guess when game ended"


def test_lost_game() -> None:
    """
    Test where agent fails to guess the correct answer
    """

    # Given
    fake_generator = FakeGenerator()
    # pylint: disable=protected-access; need to avoid guessing the answer
    guessed_word = "guess" if fake_generator._word != "guess" else "point"

    # When
    for _ in range(fake_generator.GUESSES):
        response = fake_generator.guess(guessed_word)

    # Then
    assert response.game_status == GameStatus.LOST
    assert response.guess == guessed_word

    with raises(AssertionError) as exc_info:
        fake_generator.guess(guessed_word)
    assert str(exc_info.value) == "Cannot guess when game ended"


def test_invalid_guess() -> None:
    """
    Test where agent submits an invalid guess
    """

    # Given
    fake_generator = FakeGenerator()
    guessed_word = "too_long_a_word"

    # Then
    with raises(AssertionError) as exc_info:
        fake_generator.guess(guessed_word)
    assert str(exc_info.value) == f"Guess {guessed_word} of incorrect length"


if __name__ == "__main__":
    main()
