# HAMMING CODE (15, 11)
# extended Hamming Code (16, 11)
#-----------------------------------------------------------------------------------------------------------------------

class SimpleHammingCoder:
    def __init__(self, message_bits):
        """Setup => filling the Block with the bits"""
        ## check if 11 bits
        if len(message_bits) != 11:
            raise ValueError("I'm sorry, I can't take this, this needs to be 11 bits.")

        # prepare 16-bit block (i 0-15)
        self.block = [0] * 16

        print("\n---------------------Message---------------------\n")
        print(f"Message: {message_bits}")
        for x in range(len(message_bits)):
            print(f"Bit in m at index {x}: {message_bits[x]}")
            x+=1

        print(f"\nPreparation. Block is: {self.block}")

        # the indices we can fill with data = NOT a power of 2 (3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15)
        # i = 3 => (3&(3-1)) => binary => 0011 & 0010 => 0010 != 0
        # i = 4 => (4&(4-1)) => binary => 0100 & 0011 => 0000 = 0 (power of two)
        data_indices = [i for i in range(3, 16) if (i & (i - 1)) != 0]
        print(f"Data Indices in the Codeblock that are the Message bits. Indices: {data_indices}")

        for i, bit in enumerate(message_bits):
            self.block[data_indices[i]] = bit

        print(f"Data is set and ready to go. Block is: {self.block}\n")

    def calculate_q_bit(self, indices, label):
        """Helper => manual math for any Q check"""
        # getting the bits
        bits = [self.block[i] for i in indices]
        # If sum of bits is odd, we need a 1 to make it even
        is_uneven = sum(bits) % 2 != 0
        print(f"Checking {label} (indices {indices}): Bits are {bits} -> Sum is {sum(bits)} -> Needs 1? {is_uneven}")
        return 1 if is_uneven else 0

    def encode(self):
        """Set Parity Bits => setting parity bits and special bit"""
        print("---------------------Phase 1: Setting Parity Bits (Q1-Q4)---------------------\n")

        COL2 = [5, 9, 13]
        COL3 = [6, 10, 14]
        COL4 = [3, 7, 11, 15]
        ROW2 = [5, 6, 7]
        ROW3 = [9, 10, 11]
        ROW4 = [12, 13, 14, 15]

        # We set parity bits (i: 1, 2, 4, 8) based on the grid rules
        self.block[1] = self.calculate_q_bit(COL2 + COL4, "Q1")
        self.block[2] = self.calculate_q_bit(COL3 + COL4, "Q2")
        self.block[4] = self.calculate_q_bit(ROW2 + ROW4, "Q3")
        self.block[8] = self.calculate_q_bit(ROW3 + ROW4, "Q4")

        print("\n---------------------Phase 2: Setting Special Bit (Index 0)---------------------\n")
        # sum everything from index 1 to 15
        total_data_sum = sum(self.block[1:])
        # check if uneven and add 1 if so
        self.block[0] = 1 if total_data_sum % 2 != 0 else 0
        print(f"Index 0 checks indices 1-15. Sum is {total_data_sum} -> Index 0 becomes: {self.block[0]}")

        print(f"Final Encoded Block: {self.block}")
        return self.block

    def verify(self, received_block):
        """Check code block => check if block is correct or not"""
        print("\n---------------------Phase 3: Verifying Received Block---------------------\n")
        # receiving block
        self.block = received_block

        # running the same checks
        v1 = self.calculate_q_bit([1, 3, 5, 7, 9, 11, 13, 15], "Check Q1")
        v2 = self.calculate_q_bit([2, 3, 6, 7, 10, 11, 14, 15], "Check Q2")
        v3 = self.calculate_q_bit([4, 5, 6, 7, 12, 13, 14, 15], "Check Q3")
        v4 = self.calculate_q_bit([8, 9, 10, 11, 12, 13, 14, 15], "Check Q4")

        # 'Syndrome': position of the error (if there is just one error)
        # adds the column and row position so we get the exact index
        # v's are 1 or 0 and then multiply with the row/column index
        syndrome = v1 + (v2 * 2) + (v3 * 4) + (v4 * 8)

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
coder = SimpleHammingCoder(my_bits)
send_block = coder.encode()
# need a copy because of how memory gets handled so the states get mixed up
received_block = list(send_block)

# break index 7 manually
received_block[7] = 1 - received_block[7]
received_block[8] = 1 - received_block[8]

# third error = overwhelming system; this hemming code is just for single (+ possible correction) + double error detection
# received_block[9] = 1 - received_block[9]

coder.verify(received_block)
#-----------------------------------------------------------------------------------------------------------------------
