"""Top-level CryptX CLI command group."""

import click

from cryptx import __version__
from cryptx.cli.commands.repeating_key_xor import repeating_key_xor


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    """A modular cryptanalysis toolkit for CTFs and experimentation."""

cli.add_command(repeating_key_xor)
