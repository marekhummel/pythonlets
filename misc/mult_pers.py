# https://www.youtube.com/watch?v=Wim9WJeDTHQ
from functools import reduce
import time


# Counts persistency value
def per(n):
    count = 0
    while n >= 10:
        digits = (int(i) for i in str(n))
        n = reduce(lambda x, acc: x * acc, digits, 1)
        count += 1

    return count


# Finds lowest n with persistency value length
# (won't find a solution for l=1 and a wrong one for l=2)
def low(length):
    dl = 1
    while True:
        # print(dl)
        gen = genNum(dl)
        for ds in gen:
            n = sum([d * 10**(len(ds)-i-1) for i, d in enumerate(ds)])
            if per(n) == length:
                return n

        dl += 1


# Generates a list of ascending numbers, which are worth testing
# (i.e skip 25 because it'll lead to 0 in 2 steps)
def genNum(len, curr=[]):
    if len == 0:
        yield curr
        return

    def next(n):
        # Only return numbers where the digits are sorted
        if curr == [] or curr[-1] <= n:
            return list(genNum(len-1, curr + [n]))
        else:
            return []

    lst = []
    if 2 not in curr:   # Multiple 2s could be substituted with a 4
        lst += next(2)

    if 2 not in curr and 3 not in curr:   # 2 and 3 can be subst with 6
        lst += next(3)

    if 2 not in curr:   # 2 and 4 can be subst with 8
        lst += next(4)

    if 2 not in curr and 4 not in curr:   # 5 and even number will lead to a 0
        lst += next(5)

    if 5 not in curr:   # 5 and 6 lead to a 0
        lst += next(6)

    lst += next(7)

    if 5 not in curr:   # 5 and 8 lead to a 0
        lst += next(8)

    lst += next(9)
    for num in lst:
        yield num


# Test
t = time.time()
for length in range(2, 12):
    print(length, low(length))
print(time.time() - t)

# print(12, low(12))
