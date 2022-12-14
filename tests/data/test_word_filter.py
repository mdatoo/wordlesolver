"""
File containing tests for word filter class.

Functions:
    test_filter_one_green() -> None
    test_filter_two_yellow() -> None
    test_filter_all_grey() -> None
    test_filter_one_green_one_yellow() -> None
"""

from pytest import main

from wordlesolver.data import DICTIONARY, LetterValidity, WordFilter


def test_filter_one_green() -> None:
    """Test case where one letter matches in correct position."""
    # Given
    filterer = WordFilter()
    word = "eeeee"
    validity = [
        LetterValidity.GREEN,
        LetterValidity.GREY,
        LetterValidity.GREY,
        LetterValidity.GREY,
        LetterValidity.GREY,
    ]

    # When
    filterer.filter(word, validity)

    # Then
    for possible_word in DICTIONARY:
        if possible_word in filterer.possible_words:
            assert possible_word[0] == "e" and possible_word.count("e") == 1
        else:
            assert not (possible_word[0] == "e" and possible_word.count("e") == 1)


def test_filter_two_yellow() -> None:
    """Test case where 2 letters match in wrong position."""
    # Given
    filterer = WordFilter()
    word = "eezzz"
    validity = [
        LetterValidity.YELLOW,
        LetterValidity.YELLOW,
        LetterValidity.GREY,
        LetterValidity.GREY,
        LetterValidity.GREY,
    ]

    # When
    filterer.filter(word, validity)

    # Then
    for possible_word in DICTIONARY:
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
    """Test case where 2 letters match, one in correct position."""
    # Given
    filterer = WordFilter()
    word = "eeezz"
    validity = [
        LetterValidity.GREEN,
        LetterValidity.YELLOW,
        LetterValidity.GREY,
        LetterValidity.GREY,
        LetterValidity.GREY,
    ]

    # When
    filterer.filter(word, validity)

    # Then
    for possible_word in DICTIONARY:
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
    """Test case where no letters match."""
    # Given
    filterer = WordFilter()
    word = "eeeee"
    validity = [
        LetterValidity.GREY,
        LetterValidity.GREY,
        LetterValidity.GREY,
        LetterValidity.GREY,
        LetterValidity.GREY,
    ]

    # When
    filterer.filter(word, validity)

    # Then
    for possible_word in DICTIONARY:
        if possible_word in filterer.possible_words:
            assert possible_word.count("e") == 0
        else:
            assert possible_word.count("e") != 0


if __name__ == "__main__":
    main()
