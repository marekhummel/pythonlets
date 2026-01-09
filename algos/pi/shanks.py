# https://www.youtube.com/watch?v=dtiLxLrzjOQ

# pi / 4 = 4 * arctan(1/5) - arctan(1/239)
# arctan(1 / x) = 1/x - 1/(3x^3) + 1/(5x^5) - 1/(7x^7) ...

from decimal import Decimal, getcontext

getcontext().prec = 150
SERIES_LENGTH = 100


def series_arctan(factor, x):
    dx = Decimal(x)

    # Calc chain of 1/x^i for odd i
    first_term = Decimal(factor) / dx
    chain = [first_term]
    for _ in range(SERIES_LENGTH):
        chain.append(chain[-1] / (dx * dx))

    # Scale denominator to get 1/(i*x^i)
    scaled_chain = [
        c / (Decimal(2) * Decimal(i) + Decimal(1)) for i, c in enumerate(chain)
    ]

    # Split into positives and negatives
    positives = scaled_chain[::2]
    negatives = scaled_chain[1::2]

    # Sum respectively
    sum_pos = sum(positives)
    sum_neg = sum(negatives)

    # Return total
    return sum_pos - sum_neg


arctan5 = series_arctan(16, 5)
arctan239 = series_arctan(4, 239)

pi = arctan5 - arctan239
print(pi)
