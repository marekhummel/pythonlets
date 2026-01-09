# Methods for permutations


def lexico(a, i, n):
    if i == n - 1:
        yield a
    else:
        for j in range(i, n):
            a[i], a[j] = a[j], a[i]
            yield from lexico(a, i + 1, n)
        for j in range(i + 1, n):
            a[j - 1], a[j] = a[j], a[j - 1]


def next_iter(a):
    for i in range(len(a) - 2, -1, -1):
        if a[i] < a[i + 1]:
            break

    r = -1
    for j in range(i + 1, len(a)):
        if a[j] > a[i]:
            if r == -1 or a[j] < a[r]:
                r = j

    a[i], a[r] = a[r], a[i]

    max_s = (len(a) - i) // 2
    for j in range(max_s):
        a[i + 1 + j], a[-(j + 1)] = (
            a[-(j + 1)],
            a[i + 1 + j],
        )

    return a


print(list(lexico([1, 2, 3, 4], 0, 4)))
print()
print(next_iter([8, 2, 9, 5, 4, 7, 6, 3, 1]))
