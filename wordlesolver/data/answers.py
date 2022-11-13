"""
File containing helper function for fetching a particular day's answer.

Functions:
    get_answer(date: datetime) -> str
"""

from datetime import datetime
from json import loads

from requests import get


def get_answer(date: datetime) -> str:
    """
    Fetch a particular day's answer.

    Parameters
    ----------
    date : datetime
        Day to get answer for

    Returns
    -------
    str
    """
    return str(
        loads(
            get(
                f"https://www.nytimes.com/svc/wordle/v2/{date.year}-{date.month}-{date.day}.json",
                timeout=10,
            ).content
        )["solution"]
    )
