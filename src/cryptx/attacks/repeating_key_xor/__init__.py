"""
###################################
# Repeating-Key XOR Cryptanalysis #
###################################

A small educational implementation for breaking repeating-key XOR
ciphertext using key-size analysis, ciphertext transposition, 
single-byte XOR brute force, and English-language scoring.

Attack flow:

    Step 1:
        Find probable key sizes using normalized
        Hamming distance.

    Step 2:
        Transpose the ciphertext according to each
        probable key size.

    Step 3:
        Treat every transposed column as a
        single-byte XOR ciphertext and brute-force
        all 256 possible keys.

    Step 4:
        Select the highest-scoring key byte from
        each column and reconstruct the repeating key.
"""
