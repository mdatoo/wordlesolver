"""
File containing tests for filter class

Functions:
    test_filter_one_green() -> None
    test_filter_two_yellow() -> None
    test_filter_all_grey() -> None
    test_filter_one_green_one_yellow() -> None
"""

from pytest import main

from wordlesolver.data import POSSIBLE_WORDS
from wordlesolver.response import LetterValidity
from wordlesolver.solver.filter import Filter


def test_filter_one_green() -> None:
    """
    Test case where one letter matches in correct position
    """

    # Given
    filterer = Filter()
    word = "eeeee"
    validity = [
        LetterValidity.GREEN,
        LetterValidity.GREY,
        LetterValidity.GREY,
        LetterValidity.GREY,
        LetterValidity.GREY,
    ]

    # When
    filterer.filter_possible_words(word, validity)

    # Then
    for possible_word in POSSIBLE_WORDS:
        if possible_word in filterer.possible_words:
            assert possible_word[0] == "e" and possible_word.count("e") == 1
        else:
            assert not (possible_word[0] == "e" and possible_word.count("e") == 1)


def test_filter_two_yellow() -> None:
    """
    Test case where 2 letters match in wrong position
    """

    # Given
    filterer = Filter()
    word = "eezzz"
    validity = [
        LetterValidity.YELLOW,
        LetterValidity.YELLOW,
        LetterValidity.GREY,
        LetterValidity.GREY,
        LetterValidity.GREY,
    ]

    # When
    filterer.filter_possible_words(word, validity)

    # Then
    for possible_word in POSSIBLE_WORDS:
        if possible_word in filterer.possible_words:
            assert (
                possible_word[0] != "e"
                and possible_word[1] != "e"
                and possible_word.count("e") >= 2
                and possible_word.count("z") == 0
            )
        else:
            assert not (
                possible_word[0] != "e"
                and possible_word[1] != "e"
                and possible_word.count("e") >= 2
                and possible_word.count("z") == 0
            )


def test_filter_one_green_one_yellow() -> None:
    """
    Test case where 2 letters match, one in correct position
    """

    # Given
    filterer = Filter()
    word = "eeezz"
    validity = [
        LetterValidity.GREEN,
        LetterValidity.YELLOW,
        LetterValidity.GREY,
        LetterValidity.GREY,
        LetterValidity.GREY,
    ]

    # When
    filterer.filter_possible_words(word, validity)

    # Then
    for possible_word in POSSIBLE_WORDS:
        if possible_word in filterer.possible_words:
            assert (
                possible_word[0] == "e"
                and possible_word[1] != "e"
                and possible_word[2] != "e"
                and possible_word.count("e") == 2
                and possible_word.count("z") == 0
            )
        else:
            assert not (
                possible_word[0] == "e"
                and possible_word[1] != "e"
                and possible_word[2] != "e"
                and possible_word.count("e") == 2
                and possible_word.count("z") == 0
            )


def test_filter_all_grey() -> None:
    """
    Test case where no letters match
    """

    # Given
    filterer = Filter()
    word = "eeeee"
    validity = [
        LetterValidity.GREY,
        LetterValidity.GREY,
        LetterValidity.GREY,
        LetterValidity.GREY,
        LetterValidity.GREY,
    ]

    # When
    filterer.filter_possible_words(word, validity)

    # Then
    for possible_word in POSSIBLE_WORDS:
        if possible_word in filterer.possible_words:
            assert possible_word.count("e") == 0
        else:
            assert possible_word.count("e") != 0


if __name__ == "__main__":
    main()
