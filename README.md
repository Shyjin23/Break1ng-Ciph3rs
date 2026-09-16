# Break1ng-Ciph3rs

A modular cryptanalysis toolkit for CTFs and experimentation. Each module
focuses on one cipher or attack technique, so you can explore a topic from its
data and implementation through to the explanation of why it works.

## Explore the modules

| Module | What you will learn |
| --- | --- |
| [Repeating-Key XOR](README.md#repeating-key-xor) | How key reuse lets a repeating XOR cipher be broken with Hamming distance, transposition, and frequency analysis. |

## Getting started

Install the project and its development dependencies from the repository root:

```powershell
python -m pip install --editable ".[dev]"
```

Modules are exposed as `cryptx` subcommands:

```powershell
cryptx repeating-xor --help
```

## A module-first project

Every module is intentionally self-contained:

```text
module-name/
├── README.md     # Concept, attack flow, assumptions, and usage
├── source files  # The implementation for that one topic
├── data/         # Input used by the exercise
└── tests/        # Behaviour verified for that module
```

This keeps each topic easy to study on its own. As the project grows, new modules can sit alongside the existing ones.

## Scope

These examples are for learning cryptography and cryptanalysis. They explain why legacy or incorrectly used encryption schemes fail; they are not a guide to securing production data.

## Project layout

```text
src/cryptx/
├── cli/                         # The `cryptx` command and subcommands
│   └── commands/repeating_xor.py
└── attacks/
    └── repeating_xor/           # Self-contained attack implementation
        ├── solver.py
        ├── keysize.py
        ├── operations.py
        ├── scoring.py
        └── data/ciphertext.txt

tests/                           # CLI and attack behaviour tests
```

Future attacks such as AES-ECB and single-byte XOR will be added as sibling
packages under `cryptx.attacks` and registered as CLI commands. Shared code is
intentionally not extracted until multiple attacks genuinely need it.

## Repeating-key XOR

Repeating-key XOR encrypts bytes with a short key that repeats. CryptX finds
likely key sizes by comparing normalized Hamming distances between ciphertext
blocks. For each likely size, it transposes the ciphertext so every column was
encrypted by one key byte, then ranks all 256 single-byte XOR possibilities by
how English-like they appear. The resulting key candidates are printed.

Run the bundled Base64 ciphertext:

```powershell
cryptx repeating-xor
```

Or provide your own readable Base64 ciphertext file:

```powershell
cryptx repeating-xor --file cipher.txt
```

The bundled ciphertext is loaded from the installed package, rather than the
current working directory.

## Tests

Run the focused test suite with:

```powershell
pytest
```
