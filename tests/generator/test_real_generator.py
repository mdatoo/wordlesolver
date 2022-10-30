"""
File containing tests for real generator

Functions:
    test_won_gmae() -> None
    test_lost_game() -> None
    test_invalid_guess() -> None
"""

from datetime import datetime

from pytest import main, raises

from wordlesolver.data import ANSWERS, get_day_offset
from wordlesolver.generator import RealGenerator
from wordlesolver.response import GameStatus, LetterValidity


def test_won_game() -> None:
    """
    Test where agent guesses correctly
    """

    # Given
    real_generator = RealGenerator()
    actual_word = ANSWERS[get_day_offset(datetime.now())]

    # When
    response = real_generator.guess(actual_word)

    # Then
    assert response.game_status == GameStatus.WON
    assert response.guess == actual_word
    assert response.word_validity == [LetterValidity.GREEN] * 5

    with raises(AssertionError) as exc_info:
        real_generator.guess(actual_word)
    assert str(exc_info.value) == "Cannot guess when game ended"


def test_lost_game() -> None:
    """
    Test where agent fails to guess the correct answer
    """

    # Given
    real_generator = RealGenerator()
    actual_word = ANSWERS[get_day_offset(datetime.now())]
    guessed_word = "guess" if actual_word != "guess" else "point"

    # When
    for _ in range(real_generator.GUESSES):
        response = real_generator.guess(guessed_word)

    # Then
    assert response.game_status == GameStatus.LOST
    assert response.guess == guessed_word

    with raises(AssertionError) as exc_info:
        real_generator.guess(guessed_word)
    assert str(exc_info.value) == "Cannot guess when game ended"


def test_invalid_guess() -> None:
    """
    Test where agent submits an invalid guess
    """

    # Given
    real_generator = RealGenerator()
    guessed_word = "abcde"

    # Then
    with raises(AssertionError) as exc_info:
        real_generator.guess(guessed_word)
    assert str(exc_info.value) == f"Guess {guessed_word} not in accepted words"


if __name__ == "__main__":
    main()
