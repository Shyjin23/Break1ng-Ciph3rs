import string

""" English language scoring """

LETTER_FREQUENCY = {
    'a': 8.17,
    'b': 1.49,
    'c': 2.78,
    'd': 4.25,
    'e': 12.70,
    'f': 2.23,
    'g': 2.02,
    'h': 6.09,
    'i': 6.97,
    'j': 0.15,
    'k': 0.77,
    'l': 4.03,
    'm': 2.41,
    'n': 6.75,
    'o': 7.51,
    'p': 1.93,
    'q': 0.10,
    'r': 5.99,
    's': 6.33,
    't': 9.06,
    'u': 2.76,
    'v': 0.98,
    'w': 2.36,
    'x': 0.15,
    'y': 1.97,
    'z': 0.07,
}

COMMON_BIGRAMS = {
    "th", "he", "in", "er", "an",
    "re", "on", "at", "en", "nd",
    "ti", "es", "or", "te", "of",
    "ed", "is", "it", "al", "ar",
    "st", "to", "nt", "ng", "se",
    "ha", "as", "ou", "io", "le",
    "ve", "co", "me", "de", "hi",
    "ri", "ro", "ic", "ne", "ea",
}

COMMON_TRIGRAMS = {
    "the", "and", "ing", "ion",
    "tio", "ent", "her", "for",
    "tha", "nth", "int", "ere",
    "ter", "est", "ers", "ati",
    "hat", "ate", "all", "eth",
    "hes", "ver", "his", "oft",
}

""" Score how much a plaintext looks like English """

def english_score(text: str) -> float:
    txt = text.lower()

    score = 0.0

    # character frequency
    for char in txt:
        if char in LETTER_FREQUENCY:
            score += LETTER_FREQUENCY[char]

        elif char in " \t\r\n":
            score += 13.0

        elif char in string.punctuation:
            score += 0.5

        elif 32 <= ord(char) <= 126:
            score -= 3.0

        else:
            score -= 20.0

    # common bigrams
    for bigram in COMMON_BIGRAMS:
        score += txt.count(bigram) * 5.0

    # common trigrams
    for trigram in COMMON_TRIGRAMS:
        score += txt.count(trigram) * 10.0

    return score