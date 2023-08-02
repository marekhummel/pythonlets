# Kaprekars constant 6174


def kaprekar_iter(n: int):
    digits = f"{n:04d}"
    n1 = int("".join(sorted(digits)))
    n2 = int("".join(sorted(digits, reverse=True)))

    return n2 - n1


solus = {}
for n in range(1, 10000):
    if len(set(f"{n:04d}")) == 1:
        continue

    c = n
    i = 1
    while c != 6174:
        c = kaprekar_iter(c)
        i += 1

    solus[n] = i
    # print(n, i)


slowest = sorted(solus.items(), key=lambda item: item[1], reverse=True)
print(slowest[:10])
