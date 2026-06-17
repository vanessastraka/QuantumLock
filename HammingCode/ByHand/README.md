# Hamming Code (16, 11) By Hand
Welcome to the By Hand implementation. This part of the project replicates the classic, on-paper method of learning Hamming codes. Instead of starting with heavy linear algebra, I treat a 16-bit block of data as a simple 4x4 grid to find and fix errors.

Good to know for now: how to count to 15, and the difference between even and odd numbers! :)
## The Start
We start with an 11-bit message from the user terminal. 
To protect it from getting corrupted, we stretch it into a 16-bit block (indices 0 to 15).

The extra 5 bits we added are Parity Bits (redundancy bits).
Instead of just blindly copying data, these bits act as security guards.
They look at specific groups of data bits and change themselves to ensure that the total number of 1s in that group is always even.

* **Message:** `m-array = 11 bits`
* **Codeblock:** `c-array = 16 bits`

## Why are Parity Bits placed at powers of two?
Because powers of two have a great trait in binary: they only contain a single 1.

| Position | 1    | 2 | 4    | 8    |
|----------|------|------|------|------|
| Binary   | 0001 | 0010 | 0100 | 1000 |
| Parity   | P1   | P2 | P3   | P4   |

By placing them here, we ensure that the parity bits don't accidentally calculate parity for each other. Every data index (like 3, 5, 6, 7...) is a combination of these positions, meaning multiple parity guards are watching over it.

## The Grid
If we arrange our 16-bit array into a 4x4 grid, it looks like this:

| -     | Col1 | Col2 | Col3 | Col4 |
|-------|------|------|------|------|
| Row 1 | Index 0 (Special) | Index 1 (Q1) | Index 2 (Q2) | Index 3 (Data) |
| Row 2 | Index 4 (Q3)   | Index 5 (Data)   | Index 6 (Data)   | Index 7 (Data)   |
| Row 3 | Index 8 (Q4)   | Index 9 (Data)   | Index 10 (Data)   | Index 11 (Data)   |
| Row 4 | Index 12 (Data)   | Index 13 (Data)   | Index 14 (Data)   | Index 15 (Data)   |

## Encoding
To calculate the values of our parity bits, we ask 4 specific questions about the columns and rows of our grid. If the sum of the data bits in these zones is odd, the parity bit turns into a 1 to force the sum to be even.
* **Q1** guards Columns 2 and 4: It checks indices ```[5, 9, 13]``` and ```[3, 7, 11, 15]```
* **Q2** guards Columns 3 and 4: It checks indices ```[6, 10, 14]``` and ```[3, 7, 11, 15]```
* **Q3** guards Rows 2 and 4: It checks indices ```[5, 6, 7]``` and ```[12, 13, 14, 15]```
* **Q4** guards Rows 3 and 4: It checks indices ```[9, 10, 11]``` and ```[12, 13, 14, 15]```
```python
# We set parity bits (i: 1, 2, 4, 8) based on the grid rules
self.block[1] = self.calculate_q_bit(COL2 + COL4, "Q1")
self.block[2] = self.calculate_q_bit(COL3 + COL4, "Q2")
self.block[4] = self.calculate_q_bit(ROW2 + ROW4, "Q3")
self.block[8] = self.calculate_q_bit(ROW3 + ROW4, "Q4")
```
```python
# If sum of bits is odd, we need a 1 to make it even
is_uneven = sum(bits) % 2 != 0
return 1 if is_uneven else 0
```
### Special Parity Bit - Index 0
Once Q1 - Q4 are calculated, we look at Index 0. 
This is our Special Parity Bit. 
It runs a parity check over the entire block (indices 1 through 15). 
Its job is to make sure the count of 1s across the entire grid is even.
```python
# sum everything from index 1 to 15
total_data_sum = sum(self.block[1:])
# check if uneven and add 1 if so
self.block[0] = 1 if total_data_sum % 2 != 0 else 0
```
## Finding Error
When a block is received, we run the exact same column and row checks again. 
We calculate a **Syndrome** value by adding up the failed checks:

```Syndrome = Q1 + (Q2 * 2) + (Q3 * 4) + (Q4 * 8)```

In that way it is just turning the 4-bit Syndrome into a decimal index.
That index is then used to point to the position of the error in the received codeword.
```python
syndrome = v1 + (v2 * 2) + (v3 * 4) + (v4 * 8)
# check overall parity (special bit)
is_overall_even = sum(received_block) % 2 == 0
```
The possible cases:
```python
if syndrome == 0:
    if is_overall_even:
        print("Result: Clean!")
    else:
        print("Result: Error in index 0!")
else:
    if not is_overall_even:
        print(f"Result: Single error at {syndrome}!")
    else:
        print("Result: DOUBLE ERROR! (Can't fix sorry)")
```