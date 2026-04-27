# HAMMING CODE (15, 11)
# extended Hamming Code (16, 11)
# extension to code it based on the index into bits and using XOR
# so using Index 3 is 0011; Index 4 is 0100, etc.
#-----------------------------------------------------------------------------------------------------------------------
from functools import reduce

class BinaryHammingCoder:
    def __init__(self, message_bits):
        """Setup => filling the Block with the bits"""
        ## check if 11 bits
        if len(message_bits) != 11:
            raise ValueError("I'm sorry, I can't take this, this needs to be 11 bits.")

        # prepare 16-bit block (i 0-15)
        self.block = [0] * 16
        # the indices we can fill with data = NOT a power of 2 (3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15)
        # i = 3 => (3&(3-1)) => binary => 0011 & 0010 => 0010 != 0
        # i = 4 => (4&(4-1)) => binary => 0100 & 0011 => 0000 = 0 (power of two)
        data_indices = [i for i in range(3, 16) if (i & (i - 1)) != 0]
        for i, bit in enumerate(message_bits):
            self.block[data_indices[i]] = bit

        print(f"Data is set and ready to go. Block is: {self.block}\n")

    def to_bin(self, n):
        """Helper to show 4 bit binary strings"""
        return format(n, '04b')

    def encode(self):
        """Set Parity Bits => setting parity bits and special bit"""
        print("Phase 1: Setting Parity Bits (Q1-Q4)")

        ones_indices = [i for i, bit in enumerate(self.block) if bit == 1]
        print(f"Indices containing a '1': {ones_indices}")

        # DOES THE SAME (using it in verify()): syndrome = reduce(lambda x, y: x ^ y, ones_indices, 0)
        # We start XORing from 0
        current_xor = 0
        for idd in ones_indices:
            prev_xor = current_xor
            current_xor = current_xor ^ idd
            print(
                f"  XOR Step: {self.to_bin(prev_xor)} ^ {self.to_bin(idd)} ({prev_xor} ^ {idd}) = {self.to_bin(current_xor)}")

        syndrome = current_xor
        print(f"Final Syndrome Result: {syndrome} ({self.to_bin(syndrome)})")

        # Set parity bits at 1, 2, 4, 8 based on the syndrome
        for p in [1, 2, 4, 8]:
            # if syndrome and the index != 0000
            print(f"  Checking {self.to_bin(syndrome)} & {self.to_bin(p)} (Parity bit {p}): ")
            if syndrome & p:
                self.block[p] = 1
                print(f"  > Parity bit {p} set to 1")
            else:
                print(f"  > Parity bit {p} is left on 0")
        print("  => we want 0000")

        print("\nPhase 2: Setting Special Bit (Index 0)")
        self.block[0] = sum(self.block[1:]) % 2
        print(f"Index 0 checks indices 1-15 uneven/even? -> Index 0 becomes: {self.block[0]}")

        print(f"Final Encoded Block: {self.block}")
        return self.block

    def verify(self, received_block):
        """Check code block => check if block is correct or not"""
        print("\nPhase 3: Verifying Received Block")
        # XOR every index that contains a 1
        # 'Syndrome': position of the error (if there is just one error)
        ones_indices = [i for i, bit in enumerate(received_block) if bit == 1]
        syndrome = reduce(lambda x, y: x ^ y, ones_indices, 0)

        # check overall parity (special bit)
        is_overall_even = sum(received_block) % 2 == 0

        print(f"Overall Block Parity: {'Even' if is_overall_even else 'Odd'}\n")

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

#-----------------------------------------------------------------------------------------------------------------------
# TRY IT OUT!
my_bits = [1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0] # 11 bits
coder = BinaryHammingCoder(my_bits)
safe_block = coder.encode()
# need a copy because of how memory gets handled so the states get mixed up
received_block = list(sended_block)

# break index 7 manually
received_block[7] = 1 - received_block[7]
received_block[8] = 1 - received_block[8]

# third error = overwhelming system; this hemming code is just for single (+ possible correction) + double error detection
# received_block[9] = 1 - received_block[9]

coder.verify(received_block)
#-----------------------------------------------------------------------------------------------------------------------
