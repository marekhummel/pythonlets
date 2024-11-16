# https://www.youtube.com/watch?v=q6L06pyt9CA

from itertools import count


# s is the amount of sides (square would be s = 4)
# n is sort of the side length
def polygonal_number(s, n):
    return (s - 2) * (n) * (n - 1) // 2 + n


for s in [4, 6, 8, 31265]:
    for n in count(1):
        p = polygonal_number(s, n)

        sum = 0
        for h in range(1, n):
            sum += polygonal_number(s, h)
            if sum == p:
                # total of p cannon balls as an s-gon can be stack to a pyramid
                # with a s-gon as base with height h
                print(f"Sides: {s:<6}\tn = {n:<5}\tsum = {p:<12}\theight = {h:<4}")
                break
        else:
            continue

        break
