# BBP Formula

import math
from decimal import Decimal, getcontext

getcontext().prec = 100

pi_exact = Decimal(
    "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
)

pi = Decimal(0)

for n in range(50):
    t1 = Decimal(4) / (8 * n + 1)
    t2 = Decimal(2) / (8 * n + 4)
    t3 = Decimal(1) / (8 * n + 5)
    t4 = Decimal(1) / (8 * n + 6)
    s = (Decimal(1) / Decimal(16)) ** n

    pi += (t1 - t2 - t3 - t4) * s

    prec = math.ceil(math.log10(abs(pi - pi_exact) / pi_exact))
    print(n, round(pi, -prec + 1), prec)
