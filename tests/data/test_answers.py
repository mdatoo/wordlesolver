"""
File containing test for get_answer helper function.

Functions:
    test_get_answer() -> None
"""

from datetime import datetime

from pytest import main

from wordlesolver.data import get_answer


def test_get_answer() -> None:
    """Test get answer for particular day."""
    # Given
    date = datetime(2022, 11, 10)

    # When
    answer = get_answer(date)

    # Then
    assert answer == "unite"


if __name__ == "__main__":
    main()
