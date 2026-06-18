# Hamming Code (16, 11) By XOR
Welcome to the "By XOR" implementation! In the previous "By Hand" method, I mapped out a literal 4x4 grid and used hardcoded arrays to check specific rows and columns. While that is great for learning on paper, a computer doesn't need to look at shapes.

Instead, this version evolves that manual logic into a highly efficient programmatic trick. I use a bit's binary "address" (its index location) and the XOR ```^``` operator to achieve the exact same error detection and correction.

Good to know for now: ```^``` is the bitwise XOR operator in Python, not an exponentiation operator
(gives 1 if the bits are different, gives 0 if the bits are the same)

## The Goal
Our goal is to configure the parity bits so that if every index in the block containing a 1 and XOR all of their binary addresses together, the final result equals 0000.

If a single bit flips during transmission, that perfect 0000 balance is broken. The final XOR sum will change from zero to the exact binary address of the broken bit.

## The Start
Is the same as in ```By Hand```

## Encoding (Phase 1)
When encoding, we look at the message bits we just loaded into the block. We find every index that contains a 1 and calculate a running XOR sum of their indices.
```Python
ones_indices = [i for i, bit in enumerate(self.block) if bit == 1]
```
```Python
for idd in ones_indices:
    prev_xor = current_xor
    current_xor = current_xor ^ idd
```
The final result of this running sum gives out a 4-bit binary string (Syndrome). To force the overall block balance to equal 0000, it needs to be checked which bits are active in the syndrome and turn on the corresponding parity guard bits at positions 1, 2, 4, and 8.
```Python
for p in [1, 2, 4, 8]:
    if syndrome & p:
        self.block[p] = 1
```
### Special Parity Bit - Index 0 (Phase 2)
Is the same as in ```By Hand```

## Finding Error / Verification (Phase 3)
When a block is received, verification is easier than before.
Instead of asking four separate column/row questions, I use a single Python ```reduce``` function to instantly XOR the indices of all bits set to 1:
```Python
# XOR every index that contains a 1
ones_indices = [i for i, bit in enumerate(received_block) if bit == 1]
syndrome = reduce(lambda x, y: x ^ y, ones_indices, 0)
```

## Finding Error / Verification (Phase 4)
Not included in ```By Hand```. It is just needed to flip the bit.
```python
received_block[syndrome] = 1 - received_block[syndrome]
```

## Special: Compare to Brute Force
I implemented a custom recursive Brute Force function to see how the system handles corrections.
* **Single Error Brute Force**: Systematically flips every bit one-by-one until the syndrome returns to 0. It successfully locates single errors every time.
* **Double Error Brute Force**: If two bits are broken, the overall block parity stays Even, which signals a double error. While we know the data is corrupt, attempting a brute-force fix reveals a weakness in standard Hamming codes. Because the output is a False Positive.