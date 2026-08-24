from itertools import combinations

""" Key-size analysis for repeating-key XOR. """

type KeySizeScore = tuple[int, float]

def hamming_distance(blockA: bytes, blockB: bytes) -> int:
    return sum(
        (x ^ y).bit_count()
        for x, y in zip(blockA, blockB)
    )

def normalize_distance(ciphertxt: bytes) -> list[KeySizeScore]:
    scores = []

    # At least two complete blocks are required for Hamming-distance analysis.
    max_keysize = len(ciphertxt) // 2

    # Test key sizes from 2 through 40, limited by the ciphertext length.
    # Assumes the key length is at most 40 bytes.
    for keysize in range(2, min(41, max_keysize + 1)): 
        # Only use complete blocks and limit the analysis to eight blocks.
        blocks = [
            ciphertxt[idx : idx + keysize]
            for idx in range(0, len(ciphertxt), keysize)
            if len(ciphertxt[idx : idx + keysize]) == keysize
        ][:8]

        distances = [
            hamming_distance(blockA, blockB) / keysize
            for blockA, blockB in combinations(blocks, 2)
        ]

        score = sum(distances) / len(distances)

        scores.append((keysize, score))

    return sorted(
        scores,
        key=lambda x: x[1]
    )