# Count ways to produce two punds from given coins

coins = [1, 2, 5, 10, 20, 50, 100, 200]


def divide1(target, current, csum):
    if csum == target:
        # print(*current, sep=" + ")
        return 1

    count = 0
    for c in coins:
        if csum + c > target or (len(current) != 0 and current[-1] < c):
            break
        count += divide1(target, current + [c], csum + c)

    return count


def divide2(target, max):
    if target == 0:
        return 1

    count = 0
    for c in coins:
        if c > target or c > max:
            break
        count += divide2(target - c, c)
    return count


print(divide1(200, [], 0))
print(divide2(200, coins[-1]))
