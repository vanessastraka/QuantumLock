# Welcome to QuantumLock ("Wahlfachprojekt")

> **"First steps to post-quantum cryptography: practical replication of a simple algorithm using easily readable tutorials/sources"**

This repository serves as an educational exploration into the foundational concepts of Post-Quantum Cryptography (PQC), specifically focusing on code-based cryptography. It provides a practical implementation of the Extended Hamming(16, 11) error-correcting code, demonstrating the principles from basic logic to more abstract matrix operations.

## Overview 
As quantum computers evolve, they pose a massive threat to current cryptographic standards. PQC aims to develop new algorithms that are secure against attacks from both classical and quantum computers.
### What is Post-Quantum-Cryptography (PQC) and why is it important?
Right now, full-scale quantum computers don’t really exist yet, they only exist in small, unstable forms within strictly controlled scientific environments.

Current encryption algorithms are based on mathematical problems that a classical computer takes an extremely long time to solve. For a quantum computer, these problems would be computationally easy and much faster to crack.

We have to consider this today because of the "Harvest Now, Decrypt Later" strategy. Attackers are already collecting encrypted data today. Once functional quantum computers drop in a few years, they will use them to decrypt everything they stole.
### Current development of PQC
Governments and standardization organizations are rapidly pushing for PQC evolution. Some standards are already set, and institutions handling critical data (like banks) are beginning to implement early PQC. One of the biggest players in this standardization process right now is the National Institute of Standards and Technology (NIST).
## Coding Theory Definitions
### Code-based cryptography
Cryptosystems that rely on error-correcting codes. An error-correcting code is a technique used to control and fix data transmission errors over noisy communication channels (also called forward error correction (FEC) or channel coding).
### Mathematical Coding
Translating mathematical formulas, structures, and algorithms into actual computer code, often using languages like Python.
### Coding theory vs Cryptography
Coding theory is the study of encoding information into different symbols. The difference: In coding theory, we ignore the question of who has access to the code and how secret it is. Instead, our primary concern is our ability to detect and correct errors in the data.
### Linear Code
A type of error-correcting code where codewords are formed as linear combinations of message bits (typically vectors over a finite field). A linear combination of codewords is also a valid codeword.

## Efficiency & SECDEC (Single Error Correction, Double Error Detection)
### Code Efficiency
```11/16 = 68.75% ```

(68.75% of our transmitted block is actual message data, while the rest is security overhead).
### SECDEC
Now if two bits get corrupted during transmission, it can't point to two errors. This is where the Extended part of the Hamming code comes in.

If the Syndrome says there is an error, AND Index 0 (Special bit) says the overall parity is ODD. It is a  single Error. We know where it is, and we can fix it.

If the Syndrome says there is an error, BUT Index 0 (Special bit) says the overall parity is STILL EVEN: DOUBLE ERROR DETECTED! Two errors flipped the bits in a way that tricked the grid into pointing to a random single index, but Index 0's overall block check is noticing it. We can't fix it, but we can throw a warning instead of reading corrupted data.
## The Hamming(16, 11) Code Implementation
This repository takes these concepts and implements the Extended Hamming(16, 11) code in three distinct ways, each building upon the last in terms of abstraction and efficiency:

1. **By Hand**: Located in ```HammingCode/ByHand/```,  this logic mirrors the classic, on-paper method of learning Hamming codes. It treats the 16-bit block as a 4x4 grid and identifies errors by comparing specific columns and rows. By checking if the sum of certain areas is even or uneven, you can manually pinpoint an error at a specific coordinate. It’s highly intuitive and good for understanding the foundational logic.


2. **By XOR**: Found in ```HammingCode/ByXOR/```, this version evolves the manual logic into a more efficient, programmatic form. Instead of hardcoding rows and columns, it uses the binary representation of the bit indices (Index 3 is 0011, Index 4 is 0100, etc.). By XORing the indices of all bits set to 1, we calculate the "Syndrome". This achieves the exact same result as the column/row checks but in a much more compact way, highlighting how a bit's binary "address" determines its role in parity.


3. **By Matrix**: Located in ```HammingCode/ByMatrix/```, the concept becomes compact and powerful, directly connecting to the linear algebra principles used in real PQC. We still handle data bits and parity bits, but we compute them using matrix operations. In this setup, matrix multiplication acts as a "logical AND" and addition represents a "logical XOR".
   * **Generator Matrix (G):** Maps an 11-bit message to a 16-bit codeword ```(c = m * G)```.
   * **Parity-Check Matrix (H):** Verifies a codeword. For a valid codeword c, the product ```H * c^T``` results in a zero vector. Any non-zero result is the syndrome indicating the error's location.

## Getting Started
### Prerequisites
* Python 3.x
* NumPy
### Installation
1. Clone the repository:
```
git clone https://github.com/vanessastraka/QuantumLock.git
cd QuantumLock
```
2. Install the required dependencies:
```
pip install -r requirements.txt
```
### Running the Implementations
Each implementation is a self-contained script with an example at the end. You can run them directly from your terminal to see them in action.

**By Hand Implementation:**
```
python HammingCode/ByHand/hammingCodeByHand.py
```
**By XOR Implementation:**
```
python HammingCode/ByXOR/hammingCodeByXOR.py
```
**By Matrix Implementation:**
```
python HammingCode/ByMatrix/hammingCodeByMatrix.py
```
Each script is configured to encode a sample message, manually introduce an error into the resulting codeword, and then run the verification and correction process, printing the steps to the console.
> *Note: Detailed technical breakdowns of how each method works can be found in the README files within their respective directories!*
## Project Structure
```
└── QuantumLock/
    ├── README.md               # This README file
    ├── requirements.txt        # Python dependencies
    ├── binaryHelper.py         # Helper functions for binary conversions
    └── HammingCode/
        ├── ByHand/             # Manual, grid-based implementation
        │   └── hammingCodeByHand.py
        │   └── README.md       # Explanation
        ├── ByXOR/              # Index-based XOR implementation
        │   └── hammingCodeByXOR.py
        │   └── README.md       # Explanation
        └── ByMatrix/           # Linear algebra (matrix) implementation
            └── hammingCodeByMatrix.py
            └── README.md       # Explanation
```
## Source
* [Hamming Code by Hand](https://www.youtube.com/watch?v=X8jsijhllIA)
* [Hamming Code "Binary XOR"](https://www.youtube.com/watch?v=b3NxrZOu_CE)
* [Hamming Code "Binary XOR"](https://www.ece.unb.ca/tervo/ee4253/hamming.shtml) (Additional Explanation)
* [Hamming Code by Matrix](https://www.youtube.com/watch?v=eixCGqdlGxQ&list=PLJHszsWbB6hqkOyFCQOAlQtfzC1G9sf2_&index=1)
* [Hamming Code by Matrix](https://www.ece.unb.ca/tervo/ee4253/hamming2.shtml) (Additional Explanation)
* [Hamming Code by Matrix](https://github.com/christiansiegel/coding-theory-algorithms/blob/master/LinearBlockCode.py) (Code Inspiration)