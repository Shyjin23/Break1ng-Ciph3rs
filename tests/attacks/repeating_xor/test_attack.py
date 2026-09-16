"""Tests for the repeating-key XOR solver."""

import base64

from cryptx.attacks.repeating_key_xor.attack import break_repeating_key_xor


def test_solver_returns_analysis_results(tmp_path) -> None:
    plaintext = b"This is a simple test message for CryptX."
    key = b"ICE"

    ciphertext = bytes(
        byte ^ key[index % len(key)]
        for index, byte in enumerate(plaintext)
    )

    ciphertext_file = tmp_path / "cipher.txt"
    ciphertext_file.write_text(
        base64.b64encode(ciphertext).decode("ascii"),
        encoding="utf-8",
    )

    analysis = break_repeating_key_xor(ciphertext_file)

    assert analysis.keysize_scores
    assert analysis.results

    for result in analysis.results:
        assert result.keysize > 0
        assert result.keysize_score >= 0
        assert len(result.key) == result.keysize
        assert len(result.column_candidates) == result.keysize
