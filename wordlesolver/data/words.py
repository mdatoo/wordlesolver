"""
File containing list of possible words.

Misc variables:
    POSSIBLE_WORDS : List[str]
    WORD_LENGTH : int
"""

with open("wordlesolver/data/words.txt", "r", encoding="utf-8") as file:
    POSSIBLE_WORDS = file.read().replace('"', "").split(", ")

WORD_LENGTH = len(POSSIBLE_WORDS[0])
DICTIONARY_LENGTH = len(POSSIBLE_WORDS)
