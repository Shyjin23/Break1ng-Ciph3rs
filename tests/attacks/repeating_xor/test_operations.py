"""Tests for ciphertext operations."""

import pytest

from cryptx.attacks.repeating_key_xor.operations import (
    rank_single_byte_keys,
    transpose_ciphertext,
)


def test_transpose_groups_bytes_by_key_position() -> None:
    assert transpose_ciphertext(b"ABCDEFGHIJ", keysize=3) == [
        b"ADGJ",
        b"BEH",
        b"CFI",
    ]


def test_single_byte_xor_ranks_the_correct_key_first() -> None:
    ciphertext = bytes.fromhex(
        "1b37373331363f78151b7f2b783431333d78397828372d36"
        "3c78373e783a393b3736"
    )

    key, _, plaintext = rank_single_byte_keys(
        ciphertext, 
        top_n=1
    )[0]

    assert key == 88
    assert plaintext == "Cooking MC's like a pound of bacon"


def test_operations_reject_invalid_arguments() -> None:
    with pytest.raises(ValueError, match="top_n"):
        rank_single_byte_keys(b"ciphertext", top_n=0)

    with pytest.raises(ValueError, match="keysize"):
        transpose_ciphertext(b"ciphertext", keysize=0)
