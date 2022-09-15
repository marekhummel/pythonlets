from math import prod

from decimal import Decimal, getcontext


def chudnovsky(prec):
    getcontext().prec = prec + 1

    it = int(prec / 14) + 1
    val = Decimal(0)

    for k in range(it + 1):
        dk = Decimal(k)

        sign = Decimal(1) if k & 1 == 0 else Decimal(-1)  # (-1) ** k
        fact = Decimal(prod(range(3 * k + 1, 6 * k + 1)))
        fact_cubed = Decimal(prod(range(2, k + 1)) ** 3)
        linear = 545140134 * dk + 13591409
        exp = Decimal(640320 ** (3 * dk + Decimal(1.5)))

        val += sign * fact * linear / (fact_cubed * exp)

    val *= 12
    return 1 / val


print(chudnovsky(51))
