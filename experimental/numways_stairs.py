def numways(n):
    if n == 1:
        return 1

    if n == 2:
        return 1 + numways(1)

    return numways(n-1) + numways(n-2)


def numways2(n, x):
    if n <= 0:
        return 0

    if n in x:
        return 1 + numways2(n, [i for i in x if i != n])

    return sum(numways2(n - i, x) for i in x)
