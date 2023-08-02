# https://www.youtube.com/watch?v=q6L06pyt9CA

from itertools import count


# s is the amount of sides (square would be s = 4)
# n is sort of the side length
def polygonalNumber(s, n):
    return (s - 2) * (n) * (n - 1) // 2 + n


for s in [4, 6, 8, 31265]:
    for n in count(1):
        p = polygonalNumber(s, n)

        sum = 0
        for h in range(1, n):
            sum += polygonalNumber(s, h)
            if sum == p:
                # total of p cannon balls as an s-gon can be stack to a pyramid
                # with a s-gon as base with height h
                print("Sides: {:<6}\tn = {:<5}\tsum = {:<12}\theight = {:<4}".format(s, n, p, h))
                break
        else:
            continue

        break
