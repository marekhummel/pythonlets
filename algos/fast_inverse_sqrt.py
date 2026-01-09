# ruff: noqa: E501

import struct
from math import sqrt

"""
float Q_rsqrt( float number )
{
    long i;
    float x2, y;
    const float threehalfs = 1.5F;

    x2 = number * 0.5F;
    y  = number;
    i  = * ( long * ) &y;                       // evil floating point bit level hacking
    i  = 0x5f3759df - ( i >> 1 );               // what the fuck?
    y  = * ( float * ) &i;
    y  = y * ( threehalfs - ( x2 * y * y ) );   // 1st iteration
//  y  = y * ( threehalfs - ( x2 * y * y ) );   // 2nd iteration, this can be removed

    return y;
}
"""


def inv_sqrt(x: float, newton_iter: int) -> float:
    x = float(x)
    # 32 bit float: 0 00000000 00000000000000000000000
    #               0 EEEEEEEE MMMMMMMMMMMMMMMMMMMMMMM
    # x = 2^(E_x-127) * (1 + M_x/2^23)

    xhalf = 0.5 * x

    i = struct.unpack("l", struct.pack("f", x))[0]
    # 32 bit int: 00000000 00000000 00000000 00000000
    #             0EEEEEEE EMMMMMMM MMMMMMMM MMMMMMMM
    # i = 2^23 * E_x + M_x

    j = 0x5F3759DF - (i >> 1)
    # log2(1 / sqrt(x)) = log2(1 / x^0.5) = log2(x^-0.5) = -0.5 * log2(x)
    #
    # log2(x) = log2(2^(E_x-127) * (1 + M_x/2^23))
    #         = (E_x-127) + log2(1 + M_x/2^23)          | log(1 + x) ≈ x + eps
    #         ≈ (E_x-127) + M_x/2^23 + eps
    #         = (2^23 * E_x + M_x) / 2^23 + eps - 127
    #         = 1 / 2^23 * i + eps - 127
    # => i ≈ 2^23 * (log2(x) + 127 - eps)
    #
    # y := 1 / sqrt(x)
    # => log2(y) = log2(1 / sqrt(x))
    # => log2(y) = -0.5 * log2(x)
    # ≈> 1/2^23 * (2^23 * E_y + M_y) + eps - 127 = -0.5 * (1/2^23 * (2^23 * E_x + M_x)  + eps - 127)
    # => 1/2^23 * (2^23 * E_y + M_y) + eps - 127 = -0.5 * 1/2^23 * i + -0.5 * (eps - 127)
    # => 1/2^23 * (2^23 * E_y + M_y)             = -0.5 * 1/2^23 * i + -1.5 * (eps - 127)
    # =>          (2^23 * E_y + M_y)             = -0.5 * i + -1.5 * (eps - 127) * 2^23
    # => j                                       = -1.5 * (eps - 127) * 2^23 - (i >> 1)
    # => j                                       =  1.5 * (127 - eps) * 2^23 - (i >> 1)
    #
    # eps = 0.0450465 => int(-1.5 * (eps - 127) * 2^23) = 1597463007 => hex(1597463007) = 0x5F3759DF

    y = struct.unpack("f", struct.pack("l", j))[0]
    # j = 2^23 * E_y + M_y
    # y = 2^(E_y-127) * (1 + M_y/2^23)

    for _ in range(newton_iter):
        y = y * (1.5 - xhalf * y * y)
    # f(z) := 1 / z^2 - x  =>  z = 1/sqrt(x) is root of f
    # f'(z) = -2 * 1/z^3
    # Newton Iteration:
    # y_new = y - f(y) / f'(y) = y - (1 / y^2 - x) / (-2 * 1/y^3)
    #                          = y - (1 / y^2 - x) * (y^3 / -2)
    #                          = y - (-y / 2 + y^3 / 2 * x)
    #                          = 3/2 * y - y^3 / 2 * x
    #                          = y * (3/2 - x/2 * y * y)

    return y


x = 23.6
s = 1 / sqrt(x)
print(f"{x=}")
print(f"Actual: {s}\n")

for newton_iter in range(4):
    y = inv_sqrt(x, newton_iter)
    print(f"Inv Sqrt ({newton_iter} newton_iter): {y}")
    print(round(abs(y - s) / y * 100, 10), "% error")
