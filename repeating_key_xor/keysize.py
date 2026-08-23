from itertools import combinations

""" Key-size analysis for repeating-key XOR. """

def hamming_distance(blockA: bytes, blockB: bytes) -> int:
    return sum(
        (x ^ y).bit_count()
        for x, y in zip(blockA, blockB)
    )

def normalize_distance(ciphertxt: bytes) -> list[tuple[int, float]]:
    scores = []

    for keysize in range(2, 41): # assumed scenario..

        blocks = [
            ciphertxt[idx : idx + keysize]
            for idx in range(
                0,
                len(ciphertxt),
                keysize
            )
            if len(ciphertxt[idx : idx + keysize]) == keysize
        ][:8]

        if len(blocks) < 2:
            continue

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