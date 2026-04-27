# Hamming Code (16, 11)
In general this explores the Extended Hamming Code (16, 11).
This specific configuration is designed for SECDEC (Single Error 
Correction + Double Error Detection).
It’s important to note that any corruption involving three or 
more bits is beyond the mathematical scope of this code and 
will result in random error locations.
## Hamming Code By Hand
This logic is based on the first steps used when 
learning Hamming codes on paper. It treats the 16-bit block
as a 4x4 grid and identifies errors by comparing specific 
columns and rows. By checking if the sum of certain areas
is even or uneven, you can manually pinpoint an error at a
specific section.
## Haming Code "Binary XOR"
This implementation evolves the manual logic into a more 
efficient programmatic form. Instead of hard-coding rows and
columns, it uses the binary representation of the bit indices
(Index 3 is 0011, Index 4 is 0100, ...). By XORing the 
indices of all bits set to 1, we calculate the "Syndrome". 
This achieves the exact same result as the column/row checks
but in a much more compact way. It highlights how the 
binary "address" of a bit actually determines which parity 
bits it contributes to.
## Base Source
[Hamming Code by Hand](https://www.youtube.com/watch?v=X8jsijhllIA)

[Haming Code "Binary XOR"](https://www.youtube.com/watch?v=b3NxrZOu_CE)