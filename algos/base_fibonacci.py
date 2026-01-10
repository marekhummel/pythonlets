# https://www.youtube.com/watch?v=S5FTe5KP2Cw
# Theorem of Zeckendorf


def generate_fibonacci_up_to(n: int):
    if n < 1:
        return []

    fibs = [1, 2]
    while fibs[-1] < n:
        fibs.append(fibs[-1] + fibs[-2])

    if fibs[-1] > n:
        fibs.pop()

    return fibs


def zeckendorf(n):
    if n <= 0:
        return ("0", [])

    fibs = generate_fibonacci_up_to(n)
    result = []
    remainder = n

    for fib in reversed(fibs):
        if fib <= remainder:
            result.append(fib)
            remainder -= fib
            if remainder == 0:
                break

    binary = ""
    for fib in reversed(fibs):
        binary += "1" if fib in result else "0"

    return (binary, result)


if __name__ == "__main__":
    # n = 72
    # binary, decomp = zeckendorf(n)
    # print(f"{n} = {' + '.join(map(str, decomp))}")
    # print(f"Binary: {binary}")

    n = 100
    fibs = generate_fibonacci_up_to(n)
    rows: dict[int, list[int]] = {f: [] for f in fibs}
    for i in range(1, n + 1):
        _, decomp = zeckendorf(i)
        for f in decomp:
            rows[f].append(i)

    for r in sorted(rows):
        print(f"{rows[r]}")
