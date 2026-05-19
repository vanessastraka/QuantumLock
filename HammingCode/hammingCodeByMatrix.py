# HAMMING CODE (15, 11)
# Extended (16,11)
#-----------------------------------------------------------------------------------------------------------------------
import numpy as np
import binaryHelper

class MatrixHammingCoder:
    def __init__(self, message_bits):
        """Setup => filling the Block with the bits"""
        ## check if 11 bits
        if len(message_bits) != 11:
            raise ValueError("I'm sorry, I can't take this, this needs to be 11 bits.")

        # prepare 11-bit block (i 0-10)
        self.block = [0] * 11

        # prepare parity matrix
        self.parity = np.empty([11,4])
        self.calculate_paritybits()

        for i, bit in enumerate(message_bits):
            self.block[i] = bit

        print(f"Data is set and ready to go. Block is: {self.block}\n")

    def calculate_paritybits(self):
        """Set parity bits"""
        data_indices = [i for i in range(3, 16) if (i & (i - 1)) != 0]
        print(f"Indices that are not parity bits: {data_indices}\n")

        x = 0
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
        print(f"Parity Matrix: \n{self.parity}\n")

    def generate_g(self):
        """
        Generator Matrix G => creating G
        transform a dimensional space into another dimensional space
        G =[I (11x11),P (11x4)]
        Extended => G =[I (11x11),P (11x5)]

        2^15 = 32.768 possible 15-bit vectors
        2^11 = 2.048 of them are valid codewords
        """
        print("Start Creation Generator Matrix G\n")
        print("G =[I,P]\n")
        I = np.identity(11)
        print(f"Identity Matrix: \n{I}\n")

        G = np.hstack((I, self.parity))
        print(f"G: \n{G}\n")

        print("Extended Matrix G\n")
        print("G =[I,P,EP]\n")
        EP = (np.empty([11, 1]))

        for i in range(len(G)):
            w = sum([[x != 0].count(True) for x in G[i]])
            if w % 2 == 0:
                EP[i] = 0
            else:
                EP[i] = 1

        print(f"Extended Parity Bits:\nSet to one if not even in the row.\n{EP}\n");
        G = np.hstack((G, EP))

        print(f"Extended G:\n{G}\n")

        return G

    def encode(self, g):
        """encode message m into codeword c => c = m * G"""
        print("Encode Message\n")
        print("c = m * G\n")

        dot_product = np.dot(self.block, g)

        c = dot_product % 2

        print(f"Codeword:\n{c}\n")

        #calcualting weight (1's)
        w = sum([[x!=0].count(True) for x in c])
        print(f"Hamming weight w:\n{w}\n")

        return c

    def generate_h(self):
        """
        Parity-Check Matrix H => creating H
        get Matrix to check c for errors

        H = [P^T (4x11), I(4x4)]

        Extended H
        extra column at the end => 0s
        extra row at the end => 1s
        H = [P^TE (5x11), IE(5x5)]

        """
        print("Start Creation Parity-Check Matrix H\n")
        print("H =[P^T,I]\n")
        p_t = np.transpose(self.parity)
        print(f"Transposed Parity Matrix: \n{p_t}\n")
        I = np.identity(4)

        H = np.hstack((p_t, I))
        print(f"H: \n{H}\n")

        print("Extended Parity-Check Matrix H\n")
        ones_row = [1] * 11
        p_t_e = np.vstack([p_t, ones_row])
        IE = np.identity(5)

        zw = np.hstack((p_t_e, IE))
        zw[4] = [1] * 16
        H = zw

        print(f"Extended H:\n{H}\n");

        return H

    def check(self, H, c):
        """check if codeword c valid"""
        print("Check Codeword\n")
        print("0 = H*c^T\n")

        print(f"Codeword:\n{c}\n")
        #ERROR!
        #c[1] = 1 - c[1]
        #c[4] = 1 - c[4]
        #c[11] = 1 - c[11] # error in parity bit
        #c[15] = 1 - c[15] # error in master parity bit
        print(f"Error Codeword:\n{c}\n")

        c_t = np.transpose(c)
        dot_product = np.dot(H, c_t)
        c_check = dot_product % 2

        # Split 5-bit check vector for std syndrome and master parity for double error detection
        standard_syndrome_bits = c_check[0:4]
        master_parity = c_check[4]

        print(f"Master Parity: {master_parity}")
        print(f"{standard_syndrome_bits} = \n{H}\n*\n{c_t[:, None]}\n")

        if np.any(standard_syndrome_bits):
            if master_parity == 1:
                print("Codeword contains one error!\n")
                print(f"Error: \n{standard_syndrome_bits}\n")
                error_binary_position = "".join(str(int(num)) for num in standard_syndrome_bits)
                print(f"Syndrome: \n{error_binary_position}\n")
                try:
                    error_m_position = binaryHelper.get_m_index_from_binary_index(binaryHelper.to_decimal(error_binary_position))
                    print(f"Error-Message-Index position: \n{error_m_position}\n")
                except: # if broken bit is parity bit so index 1,2,4,8 => are in the codeword index 11 - 14
                    print("Codeword contains error in parity bits!\n")
                return binaryHelper.to_decimal(error_binary_position)
            else:
                print("Codeword does contain double error! No fix possible!\n")
                return -1
        else:
            if master_parity == 1:
                print(f"Master Parity Bit is broken!\n")
                return 15
            else:
                print(f"Codeword does not contain error!\n")
                return 0

    def decode(self, index, c):
        """
        decode codeword c into message m
        first 11 bits of c are the m if check is valid
        """
        print("Decode Message")

        if index > 0:
            c[index] = 1 - c[index]
            print(f"Single error is fixed at position {index}\n")

        m = c[0:11]
        message = "".join(str(int(num)) for num in m)
        print(f"Message m: {message}")
        print(f"Comparison m from beginning: {self.block}")

#-----------------------------------------------------------------------------------------------------------------------
my_bits = [1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0] # 11 bits
coder = MatrixHammingCoder(my_bits)
G = coder.generate_g()
c = coder.encode(G)
H = coder.generate_h()
check = coder.check(H, c)
coder.decode(check, c)