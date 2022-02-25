from math import log


def frog(n):
    sum = 0
    for i in range(1, n):
        sum += 1.0 / n * (1 + frog(n-i))
    return sum


def frog2(n):
    sum = 1
    for i in range(1, n):
        sum += 1.0 / n * frog2(i)
    return sum


def frog3(n):
    sum = 0
    for i in range(1, n+1):
        sum += 1.0 / i
    return sum


n = 10

print(frog(n))
print(frog2(n))
print(frog3(n))
print(1 + log(n-1))
