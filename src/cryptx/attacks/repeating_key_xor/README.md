# Repeating-Key XOR Cryptanalysis

An educational implementation for analyzing and breaking **repeating-key XOR** ciphertext.

This module demonstrates how repeating-key XOR can be reduced to multiple **single-byte XOR** problems by identifying probable key sizes, transposing the ciphertext, and scoring possible key bytes using English-language characteristics.

---

## Overview

Repeating-key XOR encrypts each plaintext byte by XORing it with a byte from a repeating key:

```text
Plaintext:   H E L L O W O R L D
Key:         K E Y K E Y K E Y K
             ─────────────────
Ciphertext:  P ? ? ? ? ? ? ? ? ?
```

Because the key repeats, bytes at the same position within each key-sized block are encrypted with the same key byte.

For a key size of `3`:

```text
Ciphertext:

C0 C1 C2 C3 C4 C5 C6 C7 C8
│  │  │  │  │  │  │  │  │
│  │  │  └──┼──┼──└──┼──┼──
│  │  │     │  │     │  │
▼  ▼  ▼
C0 C3 C6    C1 C4 C7    C2 C5 C8

   Column 0     Column 1     Column 2
      │             │             │
      ▼             ▼             ▼
 Single-byte    Single-byte    Single-byte
    XOR            XOR            XOR
```

Each column contains bytes encrypted with the same key byte, allowing each column to be analyzed as an independent single-byte XOR cipher.

---

## Attack Strategy

The attack consists of four main stages:

```text
Repeating-key XOR ciphertext
            │
            ▼
     Find probable key sizes
            │
            ▼
    Transpose the ciphertext
            │
            ▼
  Solve single-byte XOR columns
            │
            ▼
     Reconstruct the key
```

### 1. Find probable key sizes

The implementation tests key sizes from `2` through `40`.

For each candidate size, the ciphertext is divided into complete blocks of that size. Pairwise Hamming distances between the blocks are calculated and normalized by the candidate key size:

```text
normalized distance = Hamming distance / key size
```

The average normalized distance is used as the key-size score.

Lower scores indicate greater similarity between the blocks and make a key size a candidate for further analysis. This is a heuristic signal rather than proof that the key size is correct.

The implementation uses up to the first eight complete blocks for each candidate key size and analyzes the top five candidates in the following stages.

---

### 2. Transpose the ciphertext

For each candidate key size, the ciphertext is divided into blocks of that size and then transposed.

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

Each resulting column contains ciphertext bytes encrypted with the same key byte.

The transposition is implemented by:

```text
transpose_ciphertext()
```

in `operations.py`.

---

### 3. Solve each column as single-byte XOR

Each transposed column is tested against all `256` possible byte values.

For every candidate key byte:

```text
plaintext = ciphertext XOR key
```

The resulting plaintext is scored using a simple English-language scoring function.

The scoring function considers:

* English character frequencies
* Common bigrams
* Common trigrams
* Whitespace
* Punctuation
* Printable characters
* Non-printable characters

The highest-scoring candidates are retained for each column.

---

### 4. Reconstruct the repeating key

The highest-scoring key byte from each column is selected and combined to form the repeating key.

For example:

```text
Column 0 → 0x49
Column 1 → 0x43
Column 2 → 0x45

Recovered key:

b'ICE'
```

The resulting key is then available as part of the attack results.

---

## Project Structure

```text
repeating_key_xor/
│
├── __init__.py
├── attack.py
├── keysize.py
├── operations.py
├── scoring.py
│
├── data/
│   └── ciphertext.txt
│
└── README.md
```

The attack is exposed through the main `cryptx` command-line interface.

Display the command help:

```bash
cryptx repeating-key-xor --help
```

Analyze the bundled ciphertext:

```bash
cryptx repeating-key-xor
```

Analyze a custom Base64-encoded ciphertext file:

```bash
cryptx repeating-key-xor --file cipher.txt
```

---

## Example Output

The attack first displays the calculated key-size candidates:

```text
=== KEY SIZE CANDIDATES ===

keysize=3, score=2.XXX
keysize=6, score=2.XXX
keysize=9, score=2.XXX
...
```

The most promising candidates are then analyzed column by column:

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

The attack retains multiple single-byte candidates for each column, allowing the analysis results to expose more than just the selected key byte.

---

## Why Hamming Distance?

Hamming distance measures how many bits differ between two byte sequences.

For example:

```text
A = 01000001
B = 01000100

A XOR B = 00000101
```

The XOR result contains two `1` bits:

```text
Hamming distance = 2
```

For repeating-key XOR, ciphertext blocks aligned with the repeating key can exhibit statistical similarities.

Dividing the distance by the candidate key size produces a normalized value:

```text
distance / key_size
```

This makes scores from different key sizes easier to compare.

A lower normalized distance makes a key size more interesting to investigate, but it does not guarantee that the key size is correct. Other statistical properties of the ciphertext can also produce low scores.

---

## Concepts Used

This module brings together several useful cryptanalysis concepts:

* XOR and its properties
* Repeating-key XOR
* Single-byte XOR brute force
* Hamming distance
* Normalized Hamming distance
* Frequency analysis
* Bigram and trigram analysis
* Ciphertext transposition
* English-language scoring

The central idea is that repeating-key XOR can be separated into independent single-byte XOR streams once a probable key size has been identified.

---

## Limitations

This implementation is intentionally simple and educational.

The current attack:

* Tests key sizes from `2` to `40`
* Uses up to the first eight complete blocks
* Uses pairwise Hamming distances
* Analyzes the top five key-size candidates
* Brute-forces all `256` possible single-byte keys for each column
* Uses a simple English-language scoring function
* Selects the highest-scoring key byte independently for each column

The scoring system is heuristic, so the highest-scoring candidate is not guaranteed to be correct.

In particular, independently selecting the best byte for each column can produce a plausible-looking key without producing the best overall plaintext.

The approach also assumes that the plaintext has characteristics similar to English text. Ciphertexts containing binary data, compressed data, or other non-English content may not score reliably.

---

## References / Further Reading

Useful topics to study alongside this implementation:

* XOR and its algebraic properties
* Hamming distance
* Frequency analysis
* Single-byte XOR cryptanalysis
* Repeating-key XOR cryptanalysis

The main lesson is that **reusing the XOR key introduces structure into the ciphertext**. Once that structure is identified, the repeating-key XOR problem can be separated into smaller single-byte XOR problems that can be analyzed independently.
