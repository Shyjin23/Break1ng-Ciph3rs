"""Tests for the public CryptX command-line interface."""

from click.testing import CliRunner

from cryptx.cli.main import cli


def test_repeating_key_xor_help_is_available() -> None:
    result = CliRunner().invoke(
        cli,
        ["repeating-key-xor", "--help"],
    )

    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "-f, --file" in result.output


def test_repeating_key_xor_reports_invalid_base64(tmp_path) -> None:
    ciphertext_file = tmp_path / "cipher.txt"
    ciphertext_file.write_text(
        "not valid base64!",
        encoding="utf-8",
    )

    result = CliRunner().invoke(
        cli,
        [
            "repeating-key-xor",
            "--file",
            str(ciphertext_file),
        ],
    )

    assert result.exit_code != 0
    assert "valid Base64" in result.output
