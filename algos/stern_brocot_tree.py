# https://mathworld.wolfram.com/Stern-BrocotTree.html


def approximate(x, max_deno):
    low = (0, 1)
    high = (1, 0)
    mid = (0, 0)

    while True:
        if low[1] + high[1] > max_deno:
            return mid

        mid = (low[0] + high[0], low[1] + high[1])

        val = mid[0] / mid[1]
        if val < x:
            low = mid
        elif val > x:
            high = mid
        else:
            return mid


x = 0.345345345345345345345345
approx = approximate(x, 100000)
print(x)
print(approx, approx[0] / approx[1])
