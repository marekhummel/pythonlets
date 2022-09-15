# https://www.youtube.com/watch?v=RZBhSi_PwHU
import math
from random import randint

from tqdm import tqdm


def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


dice = 120
max_iter = 10000000
coprimes = 0
for _ in tqdm(range(max_iter)):
    a = randint(1, dice)
    b = randint(1, dice)

    if gcd(a, b) == 1:
        coprimes += 1

empprob = coprimes / max_iter
print("Iterations: {0}".format(max_iter))
print("Coprimes: {0}".format(coprimes))
print("Emp. Probability: {0}".format(empprob))
print("PI Approx.: {0}".format(math.sqrt(6 / empprob)))
