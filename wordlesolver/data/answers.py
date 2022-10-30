"""
File containing list of answers

Functions:
    get_day_offset() -> int

Misc variables:
    ANSWERS : List[str]
"""

from datetime import datetime


def get_day_offset(date: datetime) -> int:
    """
    Converts date to offset
    """

    return (date - datetime(2021, 6, 19)).days


with open("wordlesolver/data/answers.txt", "r", encoding="utf-8") as file:
    ANSWERS = file.read().replace('"', "").split(", ")
