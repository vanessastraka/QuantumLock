# Hamming Code (16, 11) By Matrix
Welcome to the third and final implementation: By Matrix. 

This is the most abstract version of the project. 
It directly connects the educational look at Hamming codes to the 
high-level linear algebra concepts used in real-world Post-Quantum 
Cryptography (PQC) systems (like the McEliece cryptosystem).

Instead of mapping out a physical 4x4 grid or running bitwise XOR loops 
over active array indexes, we compress all our rules into two mathematical 
structures: 
* Generator Matrix ($G$) 
* Parity-Check Matrix ($H$)

Good to know for here: I use NumPy here to handle the heavy matrix math, 
and everything is reduced modulo 2 ($\% \, 2$) because binary algebra lives 
in a finite field where $1 + 1 = 0$.

## Parity Matrix (Preparation)
Unlike the previous versions where the 11-bit message got stretched across 
a 16-bit block immediately, the matrix approach keeps the 11 message bits 
tucked away cleanly as a standalone vector.

To determine how the data positions relate to the parity checks, 
I build an $11 \times 4$ Parity Matrix ($P$). This matrix maps each of the 
11 data positions to its corresponding 4-bit binary layout.

```python
# to iterate through indices that are not parity bits
for i in data_indices:
    # convert to binary
    num = binaryHelper.to_bin(i)
    # put it into array for single digits
    arr = [int(d) for d in str(num)]
    y = 0
    # iterate through indices of row
    for j in range(4):
        self.parity[x][j] = arr[y]
        y += 1
    x += 1
```

## The Generator Matrix ($G$) (Phase 1 - Encoding)
The Generator Matrix is a mathematical machine designed to transform an 
11-dimensional space (message) into a 16-dimensional space (protected 
codeword).

In standard coding theory, $G$ is constructed by gluing an Identity Matrix ($I$)
and our Parity Matrix ($P$) side-by-side: $G = [I \mid P]$. 
Because we are using an Extended Hamming code, we add one more column at the 
end: an Extended Parity column ($EP$) to track overall block parity.

```G = [ I (11x11) | P (11x4) | EP (11x1) ]  --> Resulting size: 11x16```

```python
I = np.identity(11)
G = np.hstack((I, self.parity))
EP = (np.empty([11, 1]))

for i in range(len(G)):
    w = sum([[x != 0].count(True) for x in G[i]])
    if w % 2 == 0:
        EP[i] = 0
    else:
        EP[i] = 1

G = np.hstack((G, EP))
```
### Encode
Encoding the message vector ($m$) into a valid codeword vector ($c$) 
becomes a single dot product operation!
$$c = (m \cdot G) \pmod 2$$

```python
dot_product = np.dot(self.block, g)
c = dot_product % 2
```
## Parity-Check Matrix ($H$) (Phase 2)
To verify whether a received codeword has been altered, we need a separate 
matrix called the Parity-Check Matrix ($H$).

Mathematically, $H$ is constructed by transposing our original parity matrix 
($P^T$) and attaching a localized Identity Matrix. For the Extended version, 
we attach a row of 1s across the bottom to handle our Master Parity bit (Index 0).
```
H = [ P^T (4x11) | I (4x4)  | 0 (4x1) ]
    [ 1   (1x11) | 0 (1x4)  | 1 (1x1) ] --> Resulting size: 5x16
```
```python
# without extended
p_t = np.transpose(self.parity)
I = np.identity(4)
H = np.hstack((p_t, I))
```
## Check + Fix (Phase 3)
When a codeword $c$ passes through a noisy channel, we test it by multiplying
it with our Parity-Check Matrix. If the codeword is perfectly healthy and
contains zero errors, the product will result in an empty zero vector:
$$H \cdot c^T = \vec{0}$$

If a bit is broken, the product outputs a 5-bit vector result. 
We split this vector into two components to make our SECDEC decision:
1. Standard Syndrome bits (First 4 bits): Spells out the error location in binary. 
2. Master Parity bit (The 5th bit): Tells us whether the overall block parity is broken.

```python
c_t = np.transpose(c)
dot_product = np.dot(H, c_t)
c_check = dot_product % 2

standard_syndrome_bits = c_check[0:4]
master_parity = c_check[4]
```
Correction Logic:
1. If Syndrome is ```active``` AND Master Parity is ```1```: Single data bit is broken! The 4 syndrome bits get back converted into a decimal number, which points to the index of the error. And after that we flip that bit back to fix it.
2. If Syndrome is ```active``` BUT Master Parity is ```0```: Double error has occurred. Recovery is impossible.
3. If Syndrome is ```clean``` BUT Master Parity is ```1```: Message data is fine, but the Master Parity bit itself got flipped during transmission.

## Decode (Phase 4)
Once the check determines the block is safe (or successfully corrects a single bit), 
decoding is trivial. Since our generator matrix placed our message bits 
squarely at the front of the codeword vector, we just slice the first 11 
bits, and we are done.
```python
m = c[0:11]
```
