import struct
from math import log2, sqrt

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


def inv_sqrt(x):
    x = float(x)
    xhalf = 0.5 * x

    i = struct.unpack("l", struct.pack("f", x))[0]
    i = 0x5F3759DF - (i >> 1)
    x = struct.unpack("f", struct.pack("l", i))[0]
    x = x * (1.5 - xhalf * x * x)
    # x = x * (1.5 - xhalf * x * x)
    return x


x = 23.6
print(f"{x=}")
print(f"{1 / sqrt(x)=}")
print(f"{2 ** (-0.5 * log2(x))=}")
print(f"{inv_sqrt(x)=}")
