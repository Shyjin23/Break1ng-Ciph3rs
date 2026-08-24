"""
############################
| Break repeating-key XOR. | 
############################

Attack flow:

    Step 1:
        Find probable key sizes using normalized
        Hamming distance.

    Step 2:
        Transpose the ciphertext according to each
        probable key size.

    Step 3:
        Treat every transposed column as a
        single-byte XOR ciphertext and brute-force
        all 256 possible keys.

    Step 4:
        Select the highest-scoring key byte from
        each column and reconstruct the repeating key.
"""

import click
import base64

from pathlib import Path

from .keysize import normalize_distance
from .operations import rank_single_byte_keys, transpose_ciphertext

""" driver code """

DEFAULT_CIPHERTEXT = (
    Path(__file__).resolve().parent / "data" / "ciphertext.txt"
)

@click.command()
@click.option(
    "-ciphertext",
    "-c",
    type=click.Path(
        exists=True,
        path_type=Path
    ),
    default=DEFAULT_CIPHERTEXT,
    help="Path to the ciphertext file.",
)
def break_repeating_key_xor(ciphertext: Path) -> None:
    # The ciphertext is expected to be Base64-encoded.
    # If the ciphertext is provided in another format, update the decoding logic below accordingly before processing it further.
    ciphertxt = base64.b64decode(
        ciphertext 
        .read_text()
        .strip()
    )

    # Step 1: Find probable key sizes

    keysize_scores = normalize_distance(ciphertxt)

    print("\n=== KEY SIZE CANDIDATES ===\n")

    for keysize, score in keysize_scores:
        print(f'{keysize=}, {score=}')

    # Try the best few keysizes
    probable_keysizes = [
        keysize
        for keysize, _ in keysize_scores[:5]
    ]

    for keysize in probable_keysizes:

        # Step 2: Solve each possible keysize

        print(
            f"\n{'=' * 20}"
            f"\nTesting keysize: {keysize}\n"
            f"{'=' * 20}"
        )

        single_key_xor_cipher_bytes = transpose_ciphertext(
            ciphertxt,
            keysize
        )

        # Step 3: Solve every transposed column (single-byte XOR brute-force..)

        key_bytes = []

        for column_no, cipher in enumerate(single_key_xor_cipher_bytes):

            candidates = rank_single_byte_keys(cipher)

            print(
                f"\nColumn {column_no}: "
                f"{len(cipher)} bytes"
            )

            for key, score, txt in candidates:

                print(
                    f"{key=} "
                    f"{score=} "
                    f"plaintext={txt!r}"
                )

            key_bytes.append(
                candidates[0][0]
            )

        # Step 4: Reconstruct the repeating key

        key = bytes(key_bytes)

        print(f"\nRecovered key bytes: {key}")