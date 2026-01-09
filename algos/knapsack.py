# ruff: noqa: N803, N806 # lowercase


def knapsack_ads(items, B):
    max_profit = sum(item[1] for item in items)
    A = [[0 for _ in range(max_profit)] for _ in items]

    for t in range(max_profit):
        if t == 0:
            A[0][t] = ([], 0)
        elif t == items[0][1]:
            A[0][t] = ([0], items[0][0])
        else:
            A[0][t] = ([], B + 1)

    for i in range(1, len(items)):
        wi, pi = items[i]
        for t in range(max_profit):
            if t < pi:
                A[i][t] = A[i - 1][t]
            else:
                possible = A[i - 1][t - pi][1] + wi
                if A[i - 1][t][1] < possible:
                    A[i][t] = A[i - 1][t]
                else:
                    lastis, lastw = A[i - 1][t - pi]
                    A[i][t] = (lastis + [i], possible)

    lasti = len(items) - 1
    return next(
        ((t, *A[lasti][t]) for t in range(max_profit - 1, -1, -1) if A[lasti][t][1] != B + 1),
        -1,
    )


# pairs of (w, p)
items = [
    (6, 10),
    (4, 4),
    (1, 5),
    (1, 4),
    (3, 1),
    (2, 2),
    (2, 1),
    (5, 5),
    (2, 4),
    (1, 2),
    (3, 5),
]

sol = knapsack_ads(items, 20)
print(f"Items: {[items[i] for i in sol[1]]}")
print(f"Weight: {sol[2]}")
print(f"Value:  {sol[0]}")
