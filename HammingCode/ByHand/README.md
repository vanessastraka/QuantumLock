# Hamming Code (16, 11) By Hand
At the beginning we have the 11 message bits.
Then for the parity bit calculation we need them in 
an array with 16 bits possible.

so we have message (m-arr) = 11 bits

and the "codeblock" (c-arr) = 16 bits

In the c-arr the other 5 bits are the parity bits
that need to be set accordingly. Those 5 bits are
at the indices from the c-array that are a power
of two.

## Why are the Parity Bits at the indices that are a power of two?
| Position | 1    | 2 |
|----------|------|------|
| Binary   | 0001 | 0010 |
| Type     | P1   | P2 |

So we can see that those bits have in common that
they just have one "1" in the binary 
representation, this enables the possibility to
pin point the error location.

