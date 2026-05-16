def to_bin(n):
    """Helper to show 4 bit binary strings"""
    return format(n, '04b')

def to_decimal(n):
    """Helper to show 4 bit binary strings"""
    return int(n, 2)

def get_m_index_from_binary_index(binary_index):
    """Helper to get m index from binary index"""
    index_map = {
        3: 0,
        5: 1,
        6: 2,
        7: 3,
        9: 4,
        10: 5,
        11: 6,
        12: 7,
        13: 8,
        14: 9,
        15: 10
    }

    return index_map[binary_index]