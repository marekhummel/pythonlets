from math import log


def frog(n):
    return sum(1.0 / n * (1 + frog(n - i)) for i in range(1, n))


def frog2(n):
    return 1 + sum(1.0 / n * frog2(i) for i in range(1, n))


def frog3(n):
    return sum(1.0 / i for i in range(1, n + 1))


n = 10

print(frog(n))
print(frog2(n))
print(frog3(n))
print(1 + log(n - 1))
