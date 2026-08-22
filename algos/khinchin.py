# Khinchins constant is (limit of ) geometric mean of continued fraction of almost any irrational number
# https://www.youtube.com/watch?v=-mXaU3N9e8Y

from collections.abc import Iterator
from math import exp, modf, pi, sqrt, e, log, trunc
from itertools import islice

# x = 2 ** (1 / 3)
x = exp(2 * pi)


def cont_frac(x) -> Iterator[int]:
    while True:
        f, i = modf(x)
        yield int(i)
        x = 1.0 / f


def geo_mean(ns):
    return exp(sum(log(n) for n in ns) / len(ns))


ns = list(islice(cont_frac(x), 1000000))
print(geo_mean(ns))
