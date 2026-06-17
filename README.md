# Welcome to QuantumLock ("Wahlfachprojekt")

> **"First steps to post-quantum cryptography: practical replication of a simple algorithm using easily readable tutorials/sources"**

This repository serves as an educational exploration into the foundational concepts of Post-Quantum Cryptography (PQC), specifically focusing on code-based cryptography. It provides a practical implementation of the Extended Hamming(16, 11) error-correcting code, demonstrating the principles from basic logic to more abstract matrix operations.

## Overview 
As quantum computers evolve, they pose a threat to current cryptographic standards. PQC aims to develop new cryptographic algorithms that are secure against attacks from both classical and quantum computers. One of the promising fields in PQC is code-based cryptography, which relies on the difficulty of decoding a message that has been intentionally corrupted with errors.

This project takes a look at these concepts by implementing the Extended Hamming(16, 11) code in three distinct ways, each building upon the last in terms of abstraction and efficiency.

### What is Post-Quantum-Cryptography (PQC) and why is it important?
PQC is a set of cryptographic algorithms that are designed to resist attacks by quantum computers, which will be much more powerful than classical computers. Right now, full-scale quantum computers don’t really exist yet, they only exist in small, unstable forms within strictly scientific environments.

Current algorithms are based on mathematical problems that a classical computer takes an extremely long time to solve, but for a quantum computer, these problems would be computationally easy and much faster to crack. That is why quantum computing could break current cryptography.

It is important to consider this now, even though quantum computers are not fully realized yet and could most likely need another few years to be operational. This is because attackers can start using them to decrypt already collected data, a strategy known as “harvest now, decrypt later.” Therefore, they are already starting to collect data today.
### Current development of PQC
Currently, governments and standardization organizations are initiating a rapid evolution of PQC algorithms. Some standards are already set, and certain institutions handling critical data (like banks, etc.) are starting to implement PQC. However, it is still at the very beginning, and the solutions are still in need of improvement. One of the biggest players in this standardization process right now is the National Institute of Standards and Technology (NIST).
## My Project
My unofficial title is: "First steps to post-quantum cryptography: practical replication of a simple algorithm using easily readable tutorials/sources."

So, I will code a simple algorithm that is based on an already established PQC logic. There are different approaches we can use to categorize these algorithms, and one of them is code-based cryptography, where the underlying theory revolves around "Linear Codes."
### Code-based cryptography
This includes cryptographic systems which rely on error-correcting codes. In computing, telecommunications, information theory, and coding theory, an error-correcting code is a technique used for controlling and fixing errors in data transmission over unreliable or noisy communication channels (also called forward error correction (FEC) or channel coding). In coding theory, a linear code is an error-correcting code for which any linear combination of codewords is also a codeword.
### Mathematical Coding
This refers to translating mathematical formulas, structures, and algorithms into computer code, often using languages like Python.
### Coding theory
This is the study of encoding information into different symbols.
(Difference to Cryptography: In coding theory, we ignore the question of who has access to the code and how secret it may be. Instead, one of our primary concerns becomes our ability to detect and correct errors in the code).
### What is linear codes?
A type of error-correcting code where codewords are formed as linear combinations of message bits (typically vectors over a finite field). A linear combination of codewords is also a codeword.
### SECDEC (Single Error Correction, Double Error Detection)
Now if two bits get corrupted during transmission, it can't point to two errors. This is where the Extended part of the Hamming code comes in.

If the Syndrome says there is an error, AND Index 0 (Special bit) says the overall parity is ODD. It is a  single Error. We know where it is, and we can fix it.

If the Syndrome says there is an error, BUT Index 0 (Special bit) says the overall parity is STILL EVEN: DOUBLE ERROR DETECTED! Two errors flipped the bits in a way that tricked the grid into pointing to a random single index, but Index 0's overall block check is noticing it. We can't fix it, but we can throw a warning instead of reading corrupted data.
## The Hamming(16, 11) Code Implementation
The core of this project is the implementation of the Extended Hamming(16, 11) code, which is designed for Single Error Correction and Double Error Detection (SECDEC). This means it can locate and fix a single-bit error or detect (but not fix) the presence of a two-bit error within a 16-bit block.

The repository explores three different methods to achieve this:

1. **By Hand (SimpleHammingCoder)**: Located in ```HammingCode/ByHand/```, this implementation mirrors the manual, on-paper method of learning Hamming codes. It treats the 16-bit block as a 4x4 grid and uses parity checks on specific rows and columns to identify errors. This approach is highly intuitive and excellent for understanding the fundamental logic.

2. **By XOR (BinaryHammingCoder)**: Found in ```HammingCode/ByXOR/```, this version evolves the manual logic into a more efficient, programmatic form. Instead of hard-coded grid checks, it calculates a "syndrome" by XORing the binary indices of all bits that are set to '1'. This method is more compact and demonstrates how a bit's binary "address" determines its role in parity calculations.

3. **By Matrix (MatrixHammingCoder)**: Located in ```HammingCode/ByMatrix/```, this is the most abstract and powerful implementation, directly connecting to the principles of linear codes used in PQC. It uses linear algebra concepts:
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