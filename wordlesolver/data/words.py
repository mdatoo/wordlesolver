"""
File containing list of possible words

Misc variables:
    POSSIBLE_WORDS : List[str]
"""

with open("wordlesolver/data/words.txt", "r", encoding="utf-8") as file:
    POSSIBLE_WORDS = file.read().splitlines()

WORD_LENGTH = len(POSSIBLE_WORDS[0])
