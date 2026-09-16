"""Operations for analyzing repeating-key XOR ciphertext."""

from .scoring import english_score


type SingleByteCandidate = tuple[int, float, str]


def rank_single_byte_keys(ciphertext: bytes, top_n: int = 5) -> list[SingleByteCandidate]:
    """Rank possible single-byte XOR keys by English-language score."""
    
    if top_n < 1:
        raise ValueError("top_n must be at least 1.")

    candidates: list[SingleByteCandidate] = []

    for key in range(256):
        plaintext = bytes(
            byte ^ key 
            for byte in ciphertext
        )

        text = plaintext.decode('latin-1')
        score = english_score(text)

        candidates.append(
            (key, score, text)
        )

    return sorted(
        candidates,
        key=lambda candidate: candidate[1],
        reverse=True
    )[:top_n]


def transpose_ciphertext(ciphertext: bytes, keysize: int) -> list[bytes]:
    """Transpose ciphertext into columns for repeating-key XOR analysis."""

    if keysize < 1:
        raise ValueError("keysize must be at least 1.")

    blocks = [
        ciphertext[idx : idx + keysize]
        for idx in range(0, len(ciphertext), keysize)
    ]

    # group bytes that were encrypted with the same key byte.
    return [
        bytes(
            block[column]
            for block in blocks
            if len(block) > column
        )
        for column in range(keysize)
    ]
