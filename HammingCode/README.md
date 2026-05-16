# Hamming Code (16, 11)
In general this explores the Extended Hamming Code (16, 11).
This specific configuration is designed for SECDEC (Single Error 
Correction + Double Error Detection).
It’s important to note that any corruption involving three or 
more bits is beyond the mathematical scope of this code and 
will result in random error locations.

I started with this as an entry into the "Linear Codes" and "PQC"
world. Showing the basics of error correction in an easy way.
So we are using logic to find errors after that it is about 
the connection to "Linear Codes" and "PQC". And the conncetion
is Matrices. Before we are using Matrices we manually broke
bits to test the system but in PQC the breaking of the bits
is part of the encryption.

Efficiency 11/16 = 68,75% (actual data)
## By Hand
This logic is based on the first steps used when 
learning Hamming codes on paper. It treats the 16-bit block
as a 4x4 grid and identifies errors by comparing specific 
columns and rows. By checking if the sum of certain areas
is even or uneven, you can manually pinpoint an error at a
specific section.
## Binary XOR
This implementation evolves the manual logic into a more 
efficient programmatic form. Instead of hard-coding rows and
columns, it uses the binary representation of the bit indices
(Index 3 is 0011, Index 4 is 0100, ...). By XORing the 
indices of all bits set to 1, we calculate the "Syndrome". 
This achieves the exact same result as the column/row checks
but in a much more compact way. It highlights how the 
binary "address" of a bit actually determines which parity 
bits it contributes to.
## Matrix
In martix form the concept can be even be more compact and powerful.
We still have the data bits and the parity bits that are getting calculated
using XOR now with martix operations and the basic of multiplication being
the "logical AND" and addition representing the "logical XOR".

Generator Matrix G maps messages to a higher dimensional codeword.

If Parity-Check Matrix H acts on valid codeword we get zero vector as output.
## Source
[Hamming Code by Hand](https://www.youtube.com/watch?v=X8jsijhllIA)

[Hamming Code "Binary XOR"](https://www.youtube.com/watch?v=b3NxrZOu_CE)

[Hamming Code "Binary XOR" (Additional Explanation)](https://www.ece.unb.ca/tervo/ee4253/hamming.shtml)

[Hamming Code by Matrix](https://www.youtube.com/watch?v=eixCGqdlGxQ&list=PLJHszsWbB6hqkOyFCQOAlQtfzC1G9sf2_&index=1)

[Hamming Code by Matrix (Additional Explanation)](https://www.ece.unb.ca/tervo/ee4253/hamming2.shtml)

[Hamming Code by Matrix (Code Inspiration)](https://github.com/christiansiegel/coding-theory-algorithms/blob/master/LinearBlockCode.py)
