"""Tests for key-size analysis."""

import pytest

from cryptx.attacks.repeating_key_xor.keysize import hamming_distance


def test_hamming_distance_known_vector() -> None:
    assert hamming_distance(b"this is a test", b"wokka wokka!!!") == 37


def test_hamming_distance_rejects_unequal_blocks() -> None:
    with pytest.raises(ValueError, match="equal-length"):
        hamming_distance(b"short", b"longer")
