from .scoring import english_score

""" Single-byte XOR operations. """

def rank_single_byte_keys(ciphertxt: bytes, top_n: int = 5) -> list[tuple[int, float, str]]:
    candidates = []

    for key in range(256):
        plaintxt = bytes(c ^ key for c in ciphertxt)

        text = plaintxt.decode('latin-1')

        score = english_score(text)

        candidates.append(
            (key, score, text)
        )

    # highest score, would be most likely english
    candidates.sort(
        key=lambda candidate: candidate[1],
        reverse=True
    )

    return candidates[:top_n]

""" Transpose ciphertext into blocks for repeating-key XOR analysis. """

def transpose_ciphertext(ciphertxt: bytes, keysize: int) -> list[bytes]:

    # blocks of specified key size
    blocks = [
        ciphertxt[idx : idx + keysize]
        for idx in range(0, len(ciphertxt), keysize)
    ]

    # collect all the bytes xor'd by the same single-byte
    return [
        bytes(
            block[i]
            for block in blocks
            if len(block) > i
        )
        for i in range(keysize)
    ]