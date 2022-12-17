"""
File containing list of possible words.

Misc variables:
    DICTIONARY : List[str]
    DICTIONARY_LENGTH : int
    WORD_LENGTH : int
    LETTERS : List[str]
    LETTERS_COUNT : int
"""

from string import ascii_lowercase
from typing import List

with open("wordlesolver/data/words.txt", "r", encoding="utf-8") as file:
    DICTIONARY: List[str] = file.read().replace('"', "").split(", ")

DICTIONARY_LENGTH: int = len(DICTIONARY)
WORD_LENGTH: int = len(DICTIONARY[0])
LETTERS: List[str] = list(ascii_lowercase)
LETTERS_COUNT: int = len(LETTERS)
