"""Solve repeating-key XOR ciphertext."""

import base64

from pathlib import Path
from dataclasses import dataclass

from .keysize import KeySizeScore, normalize_distance
from .operations import SingleByteCandidate, rank_single_byte_keys, transpose_ciphertext


TOP_KEYSIZE_CANDIDATES = 5


DEFAULT_CIPHERTEXT = (
    Path(__file__).resolve().parent / "data" / "ciphertext.txt"
)


@dataclass
class RepeatingXORAnalysis:
    """Complete analysis results for a repeating-key XOR ciphertext."""
    
    keysize_scores: list[KeySizeScore]
    results: list[RepeatingXORResult]


@dataclass
class RepeatingXORResult:
    """Results from analyzing a repeating-key XOR ciphertext."""

    keysize: int
    keysize_score: float
    column_candidates: list[list[SingleByteCandidate]]
    key: bytes


def break_repeating_key_xor(ciphertext: Path) -> RepeatingXORAnalysis:
    """Analyze a repeating-key XOR ciphertext and return candidate keys."""

    # the input ciphertext is expected to be base64-encoded.
    encoded_ciphertext = "".join(ciphertext.read_text().split())
    ciphertext_bytes = base64.b64decode(
        encoded_ciphertext, 
        validate=True
    )

    # Step 1: find probable key sizes.
    keysize_scores = normalize_distance(ciphertext_bytes)
    # only solve the most promising key sizes in detail.
    probable_keysizes = keysize_scores[:TOP_KEYSIZE_CANDIDATES]

    results: list[RepeatingXORResult] = []

    for keysize, keysize_score in probable_keysizes:
        # Step 2: transpose the ciphertext according to the keysize. 
        columns = transpose_ciphertext(
            ciphertext_bytes,
            keysize
        )

        # Step 3: solve each transposed column as a single-byte XOR cipher.
        column_candidates: list[SingleByteCandidate] = []
        key_bytes = []

        for column in columns:
            candidates = rank_single_byte_keys(column)

            column_candidates.append(candidates)
            key_bytes.append(candidates[0][0])

        # Step 4: reconstruct the key.
        key = bytes(key_bytes)

        results.append(
            RepeatingXORResult(
                keysize=keysize,
                keysize_score=keysize_score,
                column_candidates=column_candidates,
                key=key,
            )
        )

    return RepeatingXORAnalysis(
        keysize_scores=keysize_scores,
        results=results,
    )
