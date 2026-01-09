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
    n = 72
    binary, decomp = zeckendorf(n)
    print(f"{n} = {' + '.join(map(str, decomp))}")
    print(f"Binary: {binary}")
