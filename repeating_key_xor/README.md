# Repeating-Key XOR Cryptanalysis

A small Python implementation for breaking **repeating-key XOR** ciphertext.

The goal of this project is to demonstrate how a repeating-key XOR cipher can be reduced to a collection of **single-byte XOR** problems by first identifying the likely key size and then transposing the ciphertext.

---

## Overview

Repeating-key XOR works by XORing each byte of the plaintext with a repeating key:

```text
Plaintext:   H E L L O W O R L D
Key:         K E Y K E Y K E Y K
             ─────────────────
Ciphertext:  P ? ? ? ? ? ? ? ? ?
```

The same key bytes are reused periodically throughout the ciphertext.

This creates a weakness: if the key size is known, every `n`th byte of the ciphertext was XORed with the same key byte.

For example, with a key size of `3`:

```text
Ciphertext:

C0 C1 C2 C3 C4 C5 C6 C7 C8
│  │  │  │  │  │  │  │  │
│  │  │  └──┼──┼──└──┼──┼── ...
│  │  │     │  │     │  │
▼  ▼  ▼
C0 C3 C6    C1 C4 C7    C2 C5 C8

   Column 0     Column 1     Column 2
      │             │             │
      ▼             ▼             ▼
 Single-byte    Single-byte    Single-byte
    XOR            XOR            XOR
```

Each column can therefore be attacked independently as a single-byte XOR cipher.

---

## Attack Strategy

The solver follows four main steps.

### 1. Determine probable key sizes

For each possible key size from `2` through `40`, the ciphertext is divided into blocks of that size.

The Hamming distance between blocks is calculated and normalized by the key size.

```text
normalized distance =
    Hamming distance / key size
```

The average distance across several blocks is used as the score.

A smaller normalized Hamming distance suggests that the blocks have more similarity than would be expected from random data, making that key size more likely.

The implementation considers the first eight complete blocks for each candidate key size.

---

### 2. Transpose the ciphertext

Once probable key sizes have been identified, the ciphertext is split into blocks of the candidate key size.

The blocks are then transposed so that bytes encrypted with the same key byte are grouped together.

For example:

```text
Ciphertext blocks:

A B C
D E F
G H I
J K L

Transposed:

A D G J
B E H K
C F I L
```

Each resulting column was encrypted using the same single byte of the repeating key.

The transposition is implemented by:

```text
transpose_ciphertext()
```

in `operations.py`.

---

### 3. Solve each column as single-byte XOR

For every transposed column, all `256` possible byte values are tested.

For each candidate key:

```text
plaintext = ciphertext XOR key
```

The resulting plaintext is scored according to how closely it resembles English.

The solver uses:

* English character frequencies
* common bigrams
* common trigrams
* whitespace
* punctuation
* printable characters
* non-printable characters

The highest-scoring candidates are displayed.

---

### 4. Reconstruct the repeating key

The highest-scoring single-byte key from each column is selected.

For example:

```text
Column 0 → key byte 0x49
Column 1 → key byte 0x43
Column 2 → key byte 0x45

Recovered key:

b'ICE'
```

The individual bytes are then combined to reconstruct the repeating XOR key.

---

## Project Structure

```text
repeating_key_xor/
│
├── __init__.py
│
├── solve.py
│
├── scoring.py
│
├── operations.py
│
├── keysize.py
│
├── data/
│   └── ciphertext.txt
│
└── README.md
```

### `solve.py`

Main driver for the attack.

Responsible for:

1. Loading the ciphertext
2. Finding probable key sizes
3. Testing candidate key sizes
4. Transposing the ciphertext
5. Recovering the key bytes
6. Displaying the results

### `scoring.py`

Contains the English-language scoring system.

```text
LETTER_FREQUENCY
COMMON_BIGRAMS
COMMON_TRIGRAMS
english_score()
```

The `english_score()` function evaluates how closely a candidate plaintext resembles English text.

### `operations.py`

Contains the XOR operations used during the attack.

```text
rank_single_byte_keys()
transpose_ciphertext()
```

`rank_single_byte_keys()` brute-forces all `256` possible single-byte keys and ranks the resulting plaintexts using the English-language scoring function.

`transpose_ciphertext()` reorganizes the ciphertext so that bytes encrypted with the same byte of the repeating key are grouped into the same column.

This allows the repeating-key XOR problem to be reduced to multiple single-byte XOR problems.

### `keysize.py`

Contains key-size analysis.

```text
hamming_distance()
normalize_distance()
```

`hamming_distance()` calculates the bit-level difference between two byte sequences.

`normalize_distance()` evaluates candidate key sizes using normalized Hamming distance and ranks them from most to least promising.

---

## Running the Solver

Because the project uses Python package-relative imports, run the solver as a module from the directory containing `repeating_key_xor`.

```bash
python -m repeating_key_xor.solve
```

For example:

```text
Break1ng-Ciph3rs/
└── repeating_key_xor/
    ├── __init__.py
    ├── solve.py
    ├── scoring.py
    ├── operations.py
    ├── keysize.py
    └── data/
        └── ciphertext.txt
```

Run:

```bash
cd Break1ng-Ciph3rs
python -m repeating_key_xor.solve
```

Do **not** run:

```bash
python -m .\repeating_key_xor\solve.py
```

The `-m` option expects a Python module name rather than a filesystem path.

---

## Example Output

The first stage prints the candidate key sizes:

```text
=== KEY SIZE CANDIDATES ===

keysize=3, score=2.XXX
keysize=6, score=2.XXX
keysize=9, score=2.XXX
...
```

The solver then tests the most promising candidates:

```text
====================
Testing keysize: 3
====================

Column 0: XX bytes

key=...
score=...
plaintext='...'

Column 1: XX bytes

key=...
score=...
plaintext='...'

Column 2: XX bytes

key=...
score=...
plaintext='...'

Recovered key bytes: b'...'
```

---

## Concepts Used

This challenge brings together several useful cryptanalysis techniques:

* XOR properties
* Repeating-key XOR
* Single-byte XOR brute force
* Hamming distance
* Normalized Hamming distance
* Frequency analysis
* Bigram/trigram analysis
* Ciphertext transposition
* Known language characteristics

The important observation is that **repeating-key XOR is not fundamentally a single problem**.

Once the key size is known:

```text
Repeating-key XOR
        │
        ▼
Determine key size
        │
        ▼
Transpose ciphertext
        │
        ▼
Multiple single-byte XOR problems
        │
        ▼
English scoring
        │
        ▼
Recover key
```

---

## Why Hamming Distance?

The Hamming distance measures how many bits differ between two byte sequences.

For example:

```text
A = 01000001
B = 01000100

A XOR B = 00000101
```

The result contains two `1` bits, therefore:

```text
Hamming distance = 2
```

For repeating-key XOR, blocks encrypted with the same repeating key pattern can exhibit statistical similarities.

Normalizing the distance by the candidate key size allows key sizes of different lengths to be compared:

```text
distance / key_size
```

The lowest-scoring candidates are investigated first.

---

## Limitations

This implementation is intentionally simple and educational.

The current solver:

* Tests key sizes from `2` to `40`
* Uses the first eight complete blocks
* Uses pairwise Hamming distances
* Brute-forces all `256` single-byte keys
* Uses a simple English-language scoring function
* Selects the highest-scoring key byte independently for each column

The scoring system is heuristic, so the highest-scoring candidate is not guaranteed to be correct.

In particular, independently choosing the best byte for each column can occasionally produce a key that looks plausible but does not produce the best overall plaintext.

---

## References / Further Reading

Useful topics to study alongside this implementation:

* XOR and its algebraic properties
* Hamming distance
* Frequency analysis
* Cryptanalysis of repeating-key XOR

The main lesson is that repeating-key XOR becomes significantly weaker once the key repeats: **the repetition allows the ciphertext to be separated into independent single-byte XOR streams.**