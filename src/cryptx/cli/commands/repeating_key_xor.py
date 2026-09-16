"""CLI command for the repeating-key XOR attack."""

import click
import binascii

from pathlib import Path

from cryptx.attacks.repeating_key_xor.attack import (
    DEFAULT_CIPHERTEXT,
    break_repeating_key_xor,
)


@click.command(name="repeating-key-xor")
@click.option(
    "-f",
    "--file",
    "ciphertext_file",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        path_type=Path,
    ),
    default=None,
    help="Base64-encoded ciphertext file. Uses the bundled sample by default.",
)
def repeating_key_xor(ciphertext_file: Path | None) -> None:
    """Find likely keys for a repeating-key XOR ciphertext."""

    try:
        analysis = break_repeating_key_xor(
            ciphertext_file or DEFAULT_CIPHERTEXT
        )
    except (binascii.Error, UnicodeError) as error:
        raise click.ClickException(
            f"Ciphertext must contain valid Base64 text: {error}"
        ) from error

    click.echo("\n=== KEY SIZE CANDIDATES ===\n")

    # display ALL key-size candidates.
    for keysize, score in analysis.keysize_scores:
        click.echo(
            f"keysize={keysize}, score={score:.4f}"
        )

    # display detailed analysis for only the top key sizes.
    for result in analysis.results:
        click.echo(
            f"\n{'=' * 20}"
            f"\nTesting keysize: {result.keysize}"
            f"\n{'=' * 20}"
        )

        for column_no, candidates in enumerate(result.column_candidates):
            click.echo(
                f"\nColumn {column_no}:"
                f"{len(candidates[0][2])} bytes"
            )

            for key, score, plaintext in candidates:
                click.echo(
                    f"key={key} "
                    f"score={score:.4f} "
                    f"plaintext={plaintext!r}"
                )

        click.echo(f"\nRecovered key bytes: {result.key!r}")
