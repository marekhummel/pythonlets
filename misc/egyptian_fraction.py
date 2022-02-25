# Find sequence a_i so that x / y == Sum(1 / a_i)

import math


def fibonacci(x, y):
    yx = math.ceil(y / x)
    yield yx

    num = -y % x
    if num != 0:
        yield from fibonacci(num, y * yx)


def printfrac(x, y):
    print(x, '/', y)

    print('  corr', x / y)

    fib = list(fibonacci(x, y))
    valfib = sum([1 / x for x in fib])
    print('  fibo', valfib)
    print('  denos', fib)
    print()


printfrac(7, 15)
printfrac(5, 121)
printfrac(31, 311)
