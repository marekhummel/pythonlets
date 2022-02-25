import struct
from math import sqrt


def ieee754(intval):
    ieeestr = f'{intval:b}'.zfill(32)

    sign_bit, exp_bin, significand_bin = ieeestr[0], ieeestr[1:9], ieeestr[9:]
    bias = (1 << (len(exp_bin)-1)) - 1

    sign = -1.0 if sign_bit == '1' else 1.0
    exp = int(exp_bin, 2) - bias
    significand = 1 + sum(int(x) * (2 ** (-i-1)) for i, x in enumerate(significand_bin))

    return sign * (2 ** exp) * significand


def inv_sqrt(x):
    xhalf = 0.5 * x
    i = int(f"{struct.unpack('!i', struct.pack('!f', x))[0]:b}")
    i = 0x5f3759df - (i >> 1)

    x = ieee754(i)
    x = x * (1.5 - xhalf * x * x)
    return x



x = 16
print(x)
print(1 / sqrt(x))
print(inv_sqrt(x))
