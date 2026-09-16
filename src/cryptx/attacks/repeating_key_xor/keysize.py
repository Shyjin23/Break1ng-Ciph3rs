"""Key-size analysis for repeating-key XOR."""

from itertools import combinations


MAX_BLOCKS = 8
MIN_KEYSIZE = 2
MAX_KEYSIZE = 40


type KeySizeScore = tuple[int, float]


def hamming_distance(block_a: bytes, block_b: bytes) -> int:
    """Return the number of differing bits in two equal-length blocks."""
    
    if len(block_a) != len(block_b):
        raise ValueError("Hamming distance requires equal-length blocks.")

    return sum(
        (x ^ y).bit_count()
        for x, y in zip(block_a, block_b)
    )


def normalize_distance(ciphertext: bytes) -> list[KeySizeScore]:
    """Rank candidate key sizes by normalized block Hamming distance."""
   
    scores: list[KeySizeScore] = []

    # at least two complete blocks are required for Hamming-distance analysis.
    max_keysize = len(ciphertext) // 2

    # test key sizes within the configured range, limited by ciphertext length.
    for keysize in range(MIN_KEYSIZE, min(MAX_KEYSIZE + 1, max_keysize + 1)):
        
        # use complete blocks and limit the analysis to the configured maximum.
        blocks = [
            ciphertext[index : index + keysize]
            for index in range(0, len(ciphertext), keysize)
            if len(ciphertext[index : index + keysize]) == keysize
        ][:MAX_BLOCKS]

        distances = [
            hamming_distance(block_a, block_b) / keysize
            for block_a, block_b in combinations(blocks, 2)
        ]

        normalized_score = sum(distances) / len(distances)
        scores.append((keysize, normalized_score))

    return sorted(
        scores,
        key=lambda score: score[1]
    )
