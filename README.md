# Break1ng-Ciph3rs

A modular collection of cryptanalysis exercises for learning, experimentation, and CTF practice.

The project brings together implementations of classical ciphers, cryptanalytic techniques, and practical attacks in small, focused modules. Each module is designed to be studied and used independently, with its own implementation, supporting data, tests, and documentation.

## What This Project Covers?

Break1ng-Ciph3rs focuses on understanding **how cryptographic systems can be analyzed and broken when their design or usage introduces weaknesses**.

Topics include:

* Repeating-key XOR
* Other classical ciphers and cryptanalysis techniques (soon)

New topics are added as self-contained attack modules rather than being forced into a common framework.

## Getting Started 

Install the project and development dependencies from the repository root:

```powershell
python -m pip install --editable ".[dev]"
```

The project provides a `cryptx` command-line interface:

```powershell
cryptx --help
```

Individual attacks are exposed as subcommands. For example:

```powershell
cryptx repeating-key-xor --help
```

## Project Structure

```text
src/
└── cryptx/
    ├── cli/
    │   └── commands/            # CLI commands for individual attacks
    │
    └── attacks/
        ├── repeating_key_xor/   # Repeating-key XOR attack
        │   ├── attack.py
        │   ├── keysize.py
        │   ├── operations.py
        │   ├── scoring.py
        │   └── data/
        │
        └── ...                  # Future attacks

tests/
└── attacks/                     # Tests for individual attack modules
```

The code is intentionally organized around the attack being studied. Shared abstractions are introduced only when multiple modules genuinely need the same functionality.

## Module-First Approach

Each attack is intended to remain understandable on its own. This keeps the implementation close to the concept being studied while allowing the project to grow naturally as more attacks are added.

More detailed documentation for the attack is provided in its module README.

## Tests

The project uses `pytest` for automated testing.

Run the complete test suite from the repository root:

```powershell
pytest
```

For verbose output:

```powershell
pytest -v
```

Tests cover cryptanalysis behaviour, input validation, and the public CLI.

## Purpose

This is primarily a **learning and experimentation project**. The implementations favour clarity and inspectability so that the underlying cryptanalytic techniques can be understood rather than hidden behind large abstractions.

The techniques demonstrated here are intended for educational use, CTFs, and authorized experimentation.
