# Long division to get decimal digits of number (16 bit max)
# https://youtu.be/v3-a-zqKfgA?t=658

BIT_LEN = 16
CARRY_BIT = 1 << BIT_LEN
LOW_MASK = (1 << BIT_LEN) - 1
FULL_MASK = (1 << (2 * BIT_LEN)) - 1


def get_digits(n):
    digits = []
    val = n
    while True:
        d, val = longdiv(val, 10)
        digits.insert(0, d)
        if val == 0:
            return digits


def longdiv(n, div):
    value = n

    for _ in range(BIT_LEN):
        value = rot(value)
        # print(f'{i+1:2}', split(value), sep='\t')

        diff = subc(value >> BIT_LEN, div)
        # print(f'\t{(diff&CARRY_BIT) >> BIT_LEN} {diff&LOW_MASK:016b}')

        if diff & CARRY_BIT:
            value = (diff << BIT_LEN) | (value & LOW_MASK)

    digit = (value >> BIT_LEN) & LOW_MASK
    remainder = rot(value) & LOW_MASK
    return (digit, remainder)


def rot(n):
    return ((n << 1) & FULL_MASK) | ((n >> (2 * BIT_LEN)) & FULL_MASK)


def subc(n, sub):
    n = n & LOW_MASK | CARRY_BIT
    return n - sub


def split(n):
    carry = ((n >> BIT_LEN) & CARRY_BIT) >> BIT_LEN
    high = (n >> BIT_LEN) & LOW_MASK
    low = n & LOW_MASK
    return f"{carry} {high:016b}|{low:016b}"


n = 34532
print(get_digits(n))
