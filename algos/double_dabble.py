"""Double Dabble Algorithm Implementation (Binary to BCD Conversion)"""


def double_dabble(n):
    # Data is a register that holdss the BCDs (4 bits per digit) plus the binary number
    # For example: N = 162 -> Data = 0000 0000 0000 | 1010 0010
    bits = n.bit_length()
    data = n

    for _ in range(bits):
        # Check each BCD digit (4 bits)
        bcd_count = (data.bit_length() - bits) // 4 + 1
        for i in range(bcd_count):
            bcd = (data >> (bits + i * 4)) & 0xF
            if bcd >= 5:
                data += 3 << (bits + i * 4)

        # Shift left by 1
        data <<= 1

    bcds = []
    bcd_count = (data.bit_length() - bits) // 4 + 1
    for i in range(bcd_count):
        bcd = (data >> (bits + i * 4)) & 0xF
        bcds.append(bcd)
    return list(reversed(bcds))


if __name__ == "__main__":
    n = 162
    result = double_dabble(n)
    print(n, result)
